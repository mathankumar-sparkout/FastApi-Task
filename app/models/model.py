from app.Database.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    User_id = Column(Integer, primary_key=True)
    User_name = Column(String(200))
    User_email = Column(String(200))
    User_age=Column(Integer)
    User_address=Column(String(200))