# To-Do dict creation & Connection to DB

from contextlib import contextmanager

from psycopg import errors as psycopg_errors
from psycopg_pool import ConnectionPool
from fastapi import HTTPException

from config import *


# connect db to api
pool = ConnectionPool(
    min_size=5,
    max_size=12,
    conninfo=f"dbname={database} user={username} password={pwd} host={hostname} port={port_id}",
)


# connecting psycopg (i.e. database, postgres) with FastAPI
@contextmanager  # opens and automatically commits and closes
def db_connection():
    try:
        with pool.connection() as conn:
            yield conn
    except psycopg_errors.Error as exc:  # raises error in case one occurs
        detail = None
        if hasattr(exc, "pgresult") and exc.pgresult:
            detail = exc.pgresult.error_message.decode()
            raise HTTPException(status_code=409, detail=detail)


#
