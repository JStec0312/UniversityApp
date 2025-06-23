# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.db import Base
from app.models import (
    user, student, admin, news, event, event_rsvp, discount, forum_post, university, faculty, major, group, superior_group
)

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # baza tylko w RAM → idealne do testów Repo

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Każdy test funkcji będzie miał czystą bazę
@pytest.fixture(scope="function")
def db():
    # Tworzymy świeżą bazę (tabele) na start testu
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Czyścimy bazę po teście
        Base.metadata.drop_all(bind=engine)
