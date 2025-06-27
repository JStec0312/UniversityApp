from app.repositories.repository_factory import RepositoryFactory
from app.models.user import User

def test_get_by_email(db):
    user_repo = RepositoryFactory(db).get_user_repository()
    user = User(email="test@gmail.com", hashed_password="test", display_name="Test User", university_id=0)
    created_user = user_repo.create(user)

    user_repo.verify_user(created_user.id)  # Verify the user first

    
    user_repo.create_student(
        user_id=created_user.id,
        faculty_id=1,
        major_id=1
    )  

    student_repo = RepositoryFactory(db).get_student_repository()
    fetched_user = student_repo.get_by_email("test@gmail.com")

    print("Fetched User:")
    print(fetched_user.__dict__)
    print(fetched_user.user.__dict__)

