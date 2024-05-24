from fastapi import FastAPI
from app.models import model
from app.Database.database import engine
from app.routes import user

app = FastAPI()

model.Base.metadata.create_all(engine)

app.include_router(user.router)