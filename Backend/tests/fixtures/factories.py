# tests/factories.py
from uuid import uuid4
from app.models import University, Faculty, Major, Group, User, Admin, SuperiorAdmin, Event, News, Student
from passlib.hash import bcrypt

def make_university(session, name):
    uni = University(name=name)
    session.add(uni)
    session.flush()
    return uni

def make_faculty(session, university, name):
    faculty = Faculty(name=name, university_id=university.id)
    session.add(faculty)
    session.flush()
    return faculty


def make_major(session, faculty, name):
    major = Major(name=name, faculty_id=faculty.id)
    session.add(major)
    session.flush()
    return major

def make_group(session, university, name):
    group = Group(group_name=name, university_id=university.id)
    session.add(group)
    session.flush()
    return group

def make_user(session, email, password, display_name, university):
    user = User(email=email, hashed_password=bcrypt.hash(password), display_name=display_name, university_id=university.id, verified=True)
    session.add(user)
    session.flush()
    
    return user, password

def make_student(session, user, faculty = None, major=None):
    student = Student(user_id=user.id, faculty_id=faculty.id if faculty else None, major_id=major.id if major else None)
    session.add(student)
    session.flush()
    return student

def make_admin(session, group, user):
    admin = Admin(group_id=group.id, user_id=user.id)
    session.add(admin)
    session.flush()
    return admin

def make_superior_admin(session, university, user):
    superior_admin = SuperiorAdmin(university_id=university.id, user_id=user.id)
    session.add(superior_admin)
    session.flush()
    return superior_admin

def make_event(session, university, title, description, start_date, end_date):
    event = Event(university_id=university.id, title=title, description=description, start_date=start_date, end_date=end_date)
    session.add(event)
    session.flush()
    return event

def make_news(session, university, title, content):
    news = News(university_id=university.id, title=title, content=content)
    session.add(news)
    session.flush()
    return news

