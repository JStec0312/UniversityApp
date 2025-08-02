# conftest.py
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.core.db import Base, get_db

# Import all organized fixtures
from tests.fixtures import *


# 1) Shared in-memory database
@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # <-- everyone uses the same connection
    )
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


# 2) Session wrapped in SAVEPOINT -> rollback after each test
@pytest.fixture(scope="function")
def db_session(engine):
    # Open connection and global transaction
    connection = engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection, expire_on_commit=False)
    session = Session()

    # For each flush/commit, open a sub-SAVEPOINT,
    # so SQLAlchemy doesn't get confused after rollback
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        if trans.nested and not trans._parent.nested:
            sess.begin_nested()

    # Start the first savepoint
    session.begin_nested()

    yield session

    # Cleanup
    session.close()
    transaction.rollback()
    connection.close()


# 3) Override FastAPI dependency with our session
@pytest.fixture(scope="function")
def client(db_session):
    # Configure logging for tests
    import logging
    import sys
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.DEBUG)
    
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    
