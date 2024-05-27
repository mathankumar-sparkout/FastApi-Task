from fastapi import FastAPI
from app.Database.database import engine,Session
from app.models import model
from app.schemas import schemas
from sqlmodel import SQLModel,Session
from app.routes import user

app=FastAPI()

SQLModel.metadata.create_all(engine)
db = Session(engine)


app.include_router(user.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
