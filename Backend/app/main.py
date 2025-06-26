from fastapi import FastAPI
from app.api import user_api
from app.api import student_api
from app.api import admin_api
from app.core.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "University Management System API")


# User, Student, and Admin API Routers
app.include_router(user_api.router, prefix="/api/users", tags=["users"])
app.include_router(student_api.router, prefix="/api/users", tags=["students"])
app.include_router(admin_api.router, prefix="/api/users", tags=["admins"])