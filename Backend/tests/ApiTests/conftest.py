
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import *
from app.main import app
from app.core.db import get_db
from app.core.db import Base

# 🔧 Lokalna baza do testów (np. SQLite lub lokalny PostgreSQL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# lub np. PostgreSQL:
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/testdb"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # tylko SQLite
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_db():
    """Wyczyść bazę danych przed każdym testem."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture(scope= "function")
def test_data():
    db = TestingSessionLocal()

    # Tworzenie rekordów
    university = University(id=1, name="Test University")
    faculty = Faculty(id=1, name="Test Faculty", university_id=1)
    major = Major(id=1, name="Test Major", faculty_id=1)
    group = Group(university_id=1, group_name="Test Group")

    db.add_all([university, faculty, major, group])
    db.commit()

    yield db  # pozwala korzystać z bazy w testach

    db.close()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()

@pytest.fixture(scope="function")
def student_data():
    db = TestingSessionLocal()
    from passlib.hash import bcrypt
    hashed_user_password =  bcrypt.hash("testpassword")
    user = User (
        email = 'test@gmail.com',
        hashed_password = hashed_user_password,
        verified = True,
        display_name = 'Test User',
        university_id = 1
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    university = University(id=1, name="Test University")
    faculty = Faculty(id=1, name="Test Faculty", university_id=1)
    major = Major(id=1, name="Test Major", faculty_id=1)
    group = Group(university_id=1, group_name="Test Group")

    db.add_all([university, faculty, major, group])
    db.commit()



    student = Student(
        user_id = user.id,
        faculty_id = 1,
        major_id = 1
    )
    
    db.add(student)
    db.commit()
    db.refresh(student)

    yield db  # pozwala korzystać z bazy w testach

@pytest.fixture(scope="function")
def admin_data():
    db = TestingSessionLocal()
    from passlib.hash import bcrypt
    hashed_user_password =  bcrypt.hash("testpassword")
    user = User (
        email = 'test@gmail.com',
        hashed_password = hashed_user_password,
        verified = True,
        display_name = 'Test User',
        university_id = 1
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    university = University(id=1, name="Test University")
    faculty = Faculty(id=1, name="Test Faculty", university_id=1)
    major = Major(id=1, name="Test Major", faculty_id=1)
    group = Group(university_id=1, group_name="Test Group")
    db.add_all([university, faculty, major, group])
    db.commit()
    admin = Admin(
        user_id = user.id,
        group_id = 1
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    yield db
    # Cleanup
    db.close()


