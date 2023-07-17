import random
from enum import Enum
from typing import Optional, Union, Annotated
from datetime import datetime, timedelta


from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext


from psycopg import errors as psycopg_errors
from psycopg.rows import dict_row, class_row
from psycopg_pool import ConnectionPool
from contextlib import contextmanager

import psycopg
from psycopg_pool import ConnectionPool
from contextlib import contextmanager
