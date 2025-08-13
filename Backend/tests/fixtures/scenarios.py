from tests.fixtures.factories import *

def _university_faculty_major(session):
    university = make_university(session, "Test University")
    faculty = make_faculty(session, university, "Test Faculty")
    major = make_major(session, faculty, "Test Major")
    return university, faculty, major



def scenario_no_users(session):
    university, faculty, major = _university_faculty_major(session)
    group = make_group(session, university, "Test Group")
    return {
        "university": university,
        "faculty": faculty,
        "major": major,
        "group": group,
    }

def scenario_with_non_verified_user(session):
    university, faculty, major = _university_faculty_major(session)
    group = make_group(session, university, "Test Group")
    user, password = make_user(session, email="testuser@example.com", password="password", display_name="Test User", university=university)
    return {
        "university": university,
        "faculty": faculty,
        "major": major,
        "group": group,
        "user": (user, password)
    }


def scenario_with_verified_user_student(session):
    university, faculty, major = _university_faculty_major(session)
    user, password = make_user(session, email="verifiedstudent@example.com", password="password", display_name="Verified Student", university=university)
    student = make_student(session, user, faculty=faculty, major=major)
    return {
        "university": university,
        "faculty": faculty,
        "major": major,
        "user": (user, password),
        "student": student
    }


def scenario_with_student_admin_and_superior_admin(session):
    university, faculty, major = _university_faculty_major(session)
    group = make_group(session, university, "Test Group")
    event = make_event(session, university, "Test Event", "This is a test event.")
    news = make_news(session, university, "Test News", "This is a test news article.")

    user_student, password_student = make_user(session, "Student User", "studentuser@example.com", "password", university=university)
    student = make_student(session, user_student, faculty=faculty, major=major)

    user_admin, password_admin = make_user(session, "Admin User", "adminuser@example.com", "password", university=university)
    admin = make_admin(session, group, user_admin)

    user_superior_admin, password_superior_admin = make_user(session, "Superior Admin User", "superioradmin@example.com", "password", university=university)
    superior_admin = make_superior_admin(session, university, user_superior_admin)

    return {
        "university": university,
        "faculty": faculty,
        "major": major,
        "group": group,
        "event": event,
        "news": news,
        "user_student": (user_student, password_student),
        "student": student,
        "user_admin": (user_admin, password_admin),
        "admin": admin,
        "user_superior_admin": (user_superior_admin, password_superior_admin),
        "superior_admin": superior_admin
    }
