from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel,Field,AutoString

class schema_User(SQLModel):
   User_id:int
   User_name:str
   User_email:EmailStr = Field(sa_type=AutoString)
   User_age:int
   User_address:str

