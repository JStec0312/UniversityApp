from app.core.db import Base, engine
from app.models import (
    Admin,
    Discount,
    EventRSVP,
    Event,
    Faculty,
    ForumPost,
    Group,
    Major,
    News,
    Student,
    University,
    User
)

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")
