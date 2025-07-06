# conftest.py
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.models import User, University, Faculty, Major, Group, Admin, SuperiorGroup, Student
from app.core.db import Base, get_db
from app.main import app
from passlib.hash import bcrypt


# 1) Jedna, współdzielona baza w RAM
@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,           # <-- wszyscy jadą na tym samym connection
    )
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


# 2) Sesja obudowana w SAVEPOINT -> rollback po każdym teście
@pytest.fixture(scope="function")
def db_session(engine):
    # otwieramy połączenie i globalną transakcję
    connection = engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection, expire_on_commit=False)
    session = Session()

    # za każdym flush/commit otwieraj pod-SAVEPOINT,
    # żeby SQLAlchemy nie pogubiło się po rollbacku
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        if trans.nested and not trans._parent.nested:
            sess.begin_nested()

    # start pierwszego savepointu
    session.begin_nested()

    yield session

    # sprzątanie
    session.close()
    transaction.rollback()
    connection.close()


# 3) Podmieniamy zależność FastAPI na naszą sesję
@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def basic_seed(db_session):
    def _seed():
        # Create a university
        university = University(name="Test University")
        db_session.add(university)
        db_session.flush()

        # Create a faculty
        faculty = Faculty(name="Test Faculty", university_id=university.id)
        db_session.add(faculty)
        db_session.flush()

        # Create a major
        major = Major(name="Test Major", faculty_id=faculty.id)
        db_session.add(major)
        db_session.flush()

        # Create  group
        group = Group(group_name="Test Group", university_id=university.id)
        db_session.add(group)
        db_session.flush()

        #  Make previous  group superior
        superior_group = SuperiorGroup(
            university_id=university.id,
            group_id=group.id
        )
        db_session.add(superior_group)
        db_session.flush()
        
        #Create non superior group
        non_superior_group = Group(
            group_name="Non Superior Group",
            university_id=university.id
        )
        db_session.add(non_superior_group)
        db_session.flush()
        

        # Create a verified user
        user_student = User(
            email="user@gmail.com",
            hashed_password=bcrypt.hash("password"),
            verified=True,
            university_id=university.id,
            display_name="Test User"
        )
        user_admin = User(
            email="admin@gmail.com",
            hashed_password=bcrypt.hash("password"),
            verified=True,
            university_id=university.id,
            display_name="Test Admin"
        )

        user_non_superior_amin = User(
            email="nonsuperior@gmail.com",
            hashed_password=bcrypt.hash("password"),
            verified=True,
            university_id=university.id,
            display_name="Test Non Superior Admin"
        )


        db_session.add_all([user_student, user_admin, user_non_superior_amin])
        db_session.flush()
        # Create a student
        student = Student(
            user_id=user_student.id,
            faculty_id=faculty.id,
            major_id=major.id
        )
        admin = Admin(
            user_id=user_admin.id,
            group_id=group.id
        )
        non_superior_admin = Admin(
            user_id=user_non_superior_amin.id,
            group_id=non_superior_group.id
        )

        

        db_session.add_all([student, admin, non_superior_admin])
        db_session.flush()
    return _seed


@pytest.fixture
def seed_admin(db_session):
    def _seed():
        uni = University(name="Test University")
        db_session.add(uni); db_session.flush()

        faculty = Faculty(name="Test Faculty", university_id=uni.id)
        db_session.add(faculty); db_session.flush()

        major = Major(name="Test Major", faculty_id=faculty.id)
        db_session.add(major); db_session.flush()

        group = Group(group_name="Test Group", university_id=uni.id)
        db_session.add(group); db_session.flush()

        user = User(
            email="test@gmail.com",
            hashed_password=bcrypt.hash("testpassword"),
            verified=True,
            university_id=uni.id,
            display_name="Admin User"
        )
        db_session.add(user); db_session.flush()

        admin = Admin(user_id=user.id, group_id=group.id)
        db_session.add(admin); db_session.flush()

        return dict(uni=uni, faculty=faculty, major=major,
                    group=group, user=user, admin=admin)
    return _seed

@pytest.fixture
def group_register_seed(db_session):
    def _seed():
        db = db_session
        university = University(id=1, name="Test University")
        faculty = Faculty(id=1, name="Test Faculty", university_id=1)
        major = Major(id=1, name="Test Major", faculty_id=1)
        group = Group(university_id=1, group_name="Test Group")
        
        db.add_all([university, faculty, major, group])
        db.commit()
        
        # Create superior group
        superior_group = SuperiorGroup(
            university_id=1,
            group_id=1
        )
        
        db.add(superior_group)
        db.commit()
        
        # Create user with hashed password
        hashed_user_password = bcrypt.hash("testpassword")
        user = User(
            email='test@gmail.com',
            hashed_password=hashed_user_password,
            verified=True,
            display_name='Test User',
            university_id=1
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create admin record
        admin = Admin(
            user_id=user.id,
            group_id=1
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        yield db
        db.close()
    return _seed


@pytest.fixture
def student_seed(db_session):
    def _seed():
        db = db_session
        university = University(id=1, name="Test University")
        db.add(university)
        db.flush()  # Ensure the university is added before creating other entities
        faculty = Faculty(id=1, name="Test Faculty", university_id=1)
        db.add(faculty)
        db.flush()  # Ensure the faculty is added before creating major
        major = Major(id=1, name="Test Major", faculty_id=1)
        group = Group(university_id=1, group_name="Test Group")
        db.add_all([university, faculty, major, group])
        db.flush()  # Ensure all entities are added before creating user

        
        # Create user with hashed password
        hashed_user_password = bcrypt.hash("testpassword")
        user = User(
            email='test@gmail.com',
            hashed_password=hashed_user_password,
            verified=True,
            display_name='Test User',
            university_id=1
        )
        db.add(user)
        db.flush()

        # Create student record
        student = Student(
            user_id=user.id,
            faculty_id=1,
            major_id=1
        )
        db.add(student)
        db.flush()


    return _seed


@pytest.fixture
def user_seed(db_session):
    def _seed():
        db = db_session
        university = University(id=1, name="Test University")
        db.add(university)
        db.flush()
        faculty = Faculty(id=1, name="Test Faculty", university_id=1)
        db.add(faculty)
        db.flush()
        major = Major(id=1, name="Test Major", faculty_id=1)
        group = Group(university_id=1, group_name="Test Group")
        db.add_all([university, faculty, major, group])
        db.flush()
    return _seed