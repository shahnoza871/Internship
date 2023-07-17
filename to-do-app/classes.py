# Tasks related classes
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



# Classes used for security and authentification
# for tokens 
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


# for users
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



class UserIn(BaseModel):
    username: str
    password: str
