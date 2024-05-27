from sqlmodel import SQLModel,Field, AutoString
from pydantic import EmailStr


class User(SQLModel,table=True):
    __tablename__='usersmodel'
    User_id:int=Field(primary_key=True)
    User_name:str=Field(index=True)
    User_email: EmailStr = Field(sa_type=AutoString)
    User_age:int
    User_address:str
