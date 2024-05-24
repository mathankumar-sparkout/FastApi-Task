from pydantic import BaseModel


class User_schemas(BaseModel):
    User_id: int
    User_name: str
    User_email: str | None = None
    User_age: int
    User_address: str | None = None


class User_Update_schemas(BaseModel):
    User_name: str
    User_email: str | None = None
    User_age: int
    User_address: str | None = None
