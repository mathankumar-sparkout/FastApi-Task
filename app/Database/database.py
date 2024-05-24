from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:admin@localhost:3306/task5")

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
connection = engine.connect()

if connection:
    print("connected")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
