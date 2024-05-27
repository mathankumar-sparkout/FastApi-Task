from sqlmodel import SQLModel, create_engine, Session

MYSQL_USER = "root"
MYSQL_PASSWORD = "admin"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "task5"

sql_database_url = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
print(sql_database_url)

engine = create_engine(sql_database_url)
connection = engine.connect()

if connection:
    print("connected")


def get_db():
    db = Session(engine, expire_on_commit=False, autocommit=False)
    try:
        yield db
    finally:
        db.close()
