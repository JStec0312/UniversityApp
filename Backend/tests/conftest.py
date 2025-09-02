# tests/conftest.py
import os
import sys
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
os.environ.setdefault("JWT_SECRET", "dev-secret")
os.environ.setdefault("SECURE_COOKIES", "false")
os.environ.setdefault("COOKIE_SAMESITE", "lax")
os.environ.pop("COOKIE_DOMAIN", None)  # host-only cookie dla testserver
from app.main import app
from app.core.db import Base, get_db
from tests.fixtures import *
from tests.fixtures.auth_helpers import Auth

def _enable_sqlite_fk(dbapi_conn, _conn_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

@pytest.fixture(scope="function")
def auth():
    return Auth()

@pytest.fixture(scope="function")
def sqlite_db_path(tmp_path: Path):
    return tmp_path / "test_db.sqlite3"

@pytest.fixture(scope="function")
def engine(sqlite_db_path):
    url = f"sqlite:///{sqlite_db_path}"
    engine = create_engine(url, future=True)
    event.listen(engine, "connect", _enable_sqlite_fk)
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        engine.dispose()
        # opcjonalnie posprzątaj plik
        try:
            os.remove(sqlite_db_path)
        except FileNotFoundError:
            pass

@pytest.fixture(scope="function")
def db_session(engine):
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    # override get_db -> zwracamy TĘ sesję
    def _get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


