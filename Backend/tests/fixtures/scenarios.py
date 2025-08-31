from tests.fixtures.factories import *

def _university_faculty_major(session, university_name = "Test University", faculty_name = "Test Faculty", major_name = "Test Major"):
    university = make_university(session, university_name)
    faculty = make_faculty(session, university, faculty_name)
    major = make_major(session, faculty, major_name)
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

def scenario_with_multiple_groups(session):
    university, faculty, major = _university_faculty_major(session)
    group1 = make_group(session, university, "Test Group 1")
    group2 = make_group(session, university, "Test Group 2")
    group3 = make_group(session, university, "Test Group 3")
    university2, faculty2, major2 =   _university_faculty_major(session, "Test University 2", "Test Faculty 2", "Test Major 2")
    group4 = make_group(session, university2, "Test Group 4")

    user, password = make_user(session, email="superior@example.com", password="password", display_name="Superior User", university=university)
    superior_admin = make_superior_admin(session, university, user)

    return {
        "university1": university,
        "faculty1": faculty,
        "major1": major,
        "university2": university2,
        "faculty2": faculty2,
        "major2": major2,
        "groups_from_university1": [group1, group2, group3],
        "groups_from_university2": [group4],
        "user" : (user, password),
        "superior_admin": superior_admin
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

    user_student, password_student = make_user(session, display_name="Student User", email="studentuser@example.com", password="password", university=university)
    student = make_student(session, user_student, faculty=faculty, major=major)

    user_admin, password_admin = make_user(session, display_name="Admin User", email="adminuser@example.com", password="password", university=university)
    group_member_admin = make_group_member(session, user_admin, group)
    admin = make_admin(session, group, user_admin)

    user_superior_admin, password_superior_admin = make_user(session, display_name="Superior Admin User", email="superioradmin@example.com", password="password", university=university)
    group_member_superior_admin = make_group_member(session, user_superior_admin, group)
    superior_admin = make_superior_admin(session, user_superior_admin, group=group)

    return {
        "university": university,
        "faculty": faculty,
        "major": major,
        "group": group,
        "user_student": (user_student, password_student),
        "student": student,
        "user_admin": (user_admin, password_admin),
        "admin": admin,
        "user_superior_admin": (user_superior_admin, password_superior_admin),
        "superior_admin": superior_admin
    }

