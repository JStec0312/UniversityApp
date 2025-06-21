
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
