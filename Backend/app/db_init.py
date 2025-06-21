from app.core.db import Base, engine
from app.models import (
    User, Student, Admin, News, Event, EventRSVP, Discount, ForumPost
)

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")
