from fastapi import FastAPI
from app.api import user_api
from app.core.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "University Management System API")

app.include_router(user_api.router, prefix="/api/users", tags=["users"])
