from imports import *
from database_conn import *
from classes import *
from security_functions import *


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
