from fastapi import FastAPI
from app.api import user_api, student_api, admin_api, university_api, faculty_api, major_api, group_api, event_api, news_api, group_membership_api, me_api
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "University Management System API")

from app.main import app


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# User, Student, and Admin API Routers
app.include_router(user_api.router, prefix="/api/users", tags=["users"])
app.include_router(student_api.router, prefix="/api/users/students", tags=["students"])
app.include_router(admin_api.router, prefix="/api/users/admins", tags=["admins"])

app.include_router(university_api.router, prefix="/api/universities", tags=["universities"])
app.include_router(faculty_api.router, prefix="/api/universities", tags=["faculties"])
app.include_router(major_api.router, prefix="/api/universities", tags=["majors"])

app.include_router(group_api.router, prefix="/api/groups", tags=["groups"])
app.include_router(group_membership_api.router, prefix="/api/groups", tags=["group_memberships"])
app.include_router(event_api.router, prefix="/api/events", tags=["events"])
app.include_router(news_api.router, prefix="/api/news", tags=["news"])
app.include_router(me_api.router, prefix="/api/me", tags=["me"])