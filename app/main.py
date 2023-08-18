from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import users, auth, dac_generator, update, delete
from app import models
from . import oauth2, models
from.database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/",)
def root():
    return {"message": "Hello"}


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(dac_generator.router)
app.include_router(update.router)
app.include_router(delete.router)
