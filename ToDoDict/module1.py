# To-Do dict creation & Connection to DB

from enum import Enum
from contextlib import contextmanager
from contextlib import contextmanager

import psycopg
from psycopg import errors as psycopg_errors
from psycopg.rows import dict_row, class_row
from psycopg_pool import ConnectionPool
from psycopg_pool import ConnectionPool

from fastapi import FastAPI, HTTPException, Depends, status
from typing import Optional, Union, Annotated
from pydantic import BaseModel, Field

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


# fastapi
class Status(str, Enum):
    """All possible statuses of a task"""

    todo = "To do"
    in_pr = "In progress"
    done = "Done"


class Task(BaseModel):
    name: str = Field(title="Name of the task")
    details: Union[str, None] = Field(default=None, title="Further details on the task")
    status: Union[Status, None] = Field(
        default=None, title="Current status of the task"
    )

    class Config:
        use_enum_values = True
