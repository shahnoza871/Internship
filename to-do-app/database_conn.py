# TO DO DICTIONARY (connected to database)
hostname = "127.0.0.1"
database = "postgres"
username = "postgres"
pwd = "12345689"
port_id = "5432"
conn = None
cursor = None


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
