# SECURITY AND AUTHENTICATION

from datetime import datetime, timedelta
from typing import Optional, Union, Annotated

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

import psycopg
from psycopg.rows import dict_row, class_row

from module1 import db_connection

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# to generate SECRET_KEY run in terminal: openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    disabled: bool
    created_at: datetime
    full_name: Optional[str] = None


class UserInDB(BaseModel):
    username: str
    disabled: bool
    created_at: datetime
    hashed_password: str


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
