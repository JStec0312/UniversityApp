"""
Test script to verify model definitions.
Run this with:
    python test_models.py
"""
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
    SuperiorGroup,
    University,
    User
)

# This will validate all model definitions without actually creating tables
def test_model_definitions():
    # Import all models and print their table names to verify they're loaded correctly
    models = [
        Admin, Discount, EventRSVP, Event, Faculty, ForumPost,
        Group, Major, News, Student, SuperiorGroup, University, User
    ]
    
    for model in models:
        print(f"Model: {model.__name__}, Table: {model.__tablename__}")
    
    print("\nAll models imported successfully!")

if __name__ == "__main__":
    test_model_definitions()
