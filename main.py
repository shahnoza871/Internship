from imports import *
from database_conn import *
from classes import *


# fastapi


app = FastAPI(title="To Do Dictionary")


# get one task by its ID
@app.get(
    "/task/{task_id}",  # path of an endpoint
    status_code=200,  # code that shows that code works successfully
    response_model=Task,  # in FastAPI plays a role of example (in Example Value Schema)
)
async def get_task(task_id: int):
    with db_connection() as conn:  # to connect this FastAPI endpoint with the Database in PostgreSQL
        with conn.cursor(
            row_factory=dict_row
        ) as cursor:  # row_factory turns our list of [name, details, status] into dictionary
            cursor.execute(
                "SELECT name, details, status FROM tasks WHERE id = %s;",
                (
                    task_id,
                ),  # since it's tuple don't forget "," ; in case of list : [task_id]
            )
            result = (
                cursor.fetchone()
            )  # fetchONE since there is one row (i.e. one dictionary) to return
    return result


# get several/all task by its status
@app.get("/task/", status_code=200)
async def task_by_status(status: Optional[Status] = None):
    with db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            if status:
                cursor.execute(
                    "SELECT name, details, status FROM tasks WHERE status=%s;",
                    (status,),
                )
                result = cursor.fetchall()
                conn.commit()
                return result

            if not status:
                cursor.execute("SELECT * FROM tasks;")
                result = cursor.fetchall()
                conn.commit()
                return result


# # get task info by its name
# @app.get("/taskname/", status_code=200)
# async def task_by_name(name: str):
#     with db_connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT id, name, details, status FROM tasks WHERE name = %s", (name,))
#             result = cursor.fetchone()
#             return result


# add new task
@app.post("/task/", status_code=201)
async def new_task(task: Task):
    # result = None
    with db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                INSERT INTO tasks(name, details, status)
                VALUES(%s, %s, %s)
                RETURNING *;
                """,
                (task.name, task.details, task.status),
            )
            result = cursor.fetchone()
    return result


# update existing task
@app.patch("/task/{task_id}", status_code=200)
async def update(task_id: int, task: Task):
    # result = None
    with db_connection() as conn:
        with conn.cursor(row_factory=class_row(Task)) as cursor:
            # row_factory=class_row(Task) turns the list task.name, task.details, task.status, task_id into class Task
            result = cursor.execute(
                """
                UPDATE tasks
                SET name=%s, details=%s, status=%s
                WHERE id = %s
                RETURNING *;
                """,
                (task.name, task.details, task.status, task_id),
            ).fetchone()
    return result


# delete existing task
@app.delete("/task/{task_id}", status_code=200, response_model=Task)
async def delete(task_id: int):
    with db_connection() as conn:
        with conn.cursor(row_factory=class_row(Task)) as cursor:
            cursor.execute(
                """
                DELETE FROM tasks WHERE id = %s RETURNING *;
                """,
                (task_id,),
            )
            result = cursor.fetchone()
    return result


# SECURITY AND AUTHENTICATION

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# to generate SECRET_KEY run in terminal: openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# CryptContext: For working with multiple hash formats at once (such a user account table with multiple existing hash formats)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# bcrypt is a specific hashing algorithm


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)  # Bearer is the token to use OAuth2 (used in most cases);
# tokenUrl tell where to retrieve access token

# app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    # checks whether or not hashed entered password matches with hashed version of the password stored in DB


def get_password_hash(password):
    return pwd_context.hash(password)


# returns user's information
def get_user(username: str):
    with db_connection() as conn:
        with conn.cursor(row_factory=class_row(UserInDB)) as cursor:
            cursor.execute(
                """
                SELECT * FROM users WHERE username = %s
                """,
                (username,),
            )
            result = cursor.fetchone()
    return result


def authenticate_user(username: str, password: str):
    user = get_user(username)
    # checkes whether or not there is a user in the DB
    if not user:
        return False
    # checkes whether or not the password is correct (authenticates)
    if not verify_password(password, user.hashed_password):  # user.hashed_password
        return False
    return User(**user.dict())


# this part is for updating token over time (simplified, check documentation to see the full code of this function)
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    # .copy() : creates new path to_encode (data path will remain) but the values will be similar
    expire = datetime.utcnow() + expires_delta
    to_encode.update(
        {"exp": expire}
    )  # here, to_encode will change but data will remain the same
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # encode the HEADER, PAYLOAD and VERIFY SIGNATURE for convinience to send through internet
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # Depends(oauth2_scheme) : model, scheme_name, tokenUrl, flows, scheme_name, ect.
    # oath2_scheme function is gonna parse out the token for us and gives us access to it through token parameter
    credentials_exception = (
        HTTPException(  # will raise this error if we couldn't authenticate the user
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# if disabled = True, the user is not active
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# this is what's gonna be called when we signing in with our username and password
# it's then gonna return us the access_token that we gonna use for access_token_expires period of time (=30 min in this case)
@app.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # OAuth2PasswordRequestForm means that the form_data (the data to generate jwt token) must be a username and password
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # "sub": user.username data that we want to encode
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


# USERS DATABASE


@app.post("/users/")
async def sign_in(user: UserIn):
    with db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            hashed_password = get_password_hash(user.password)
            cursor.execute(
                """
                INSERT INTO users(username, hashed_password)
                VALUES (%s, %s)
                RETURNING *;
                """,
                (user.username, hashed_password),
            )
            result = cursor.fetchone()
    return result


@app.get("/users/", response_model=User)
async def user_get(user_id: int):
    with db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "SELECT username, hashed_password FROM users WHERE id = %s;",
                (user_id,),
            )
            result = cursor.fetchone()
    return result
