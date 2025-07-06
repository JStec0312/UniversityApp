from fastapi import FastAPI
from app.api import user_api, student_api, admin_api, superior_group_api
from app.core.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "University Management System API")

from app.main import app


# User, Student, and Admin API Routers
app.include_router(user_api.router, prefix="/api/user", tags=["users"])
app.include_router(student_api.router, prefix="/api/user", tags=["students"])
app.include_router(admin_api.router, prefix="/api/user", tags=["admins"])
app.include_router(superior_group_api.router, prefix = "/api/user/superior-group", tags=["superior-groups"])

