from app.schemas.university import UniversityOut
class UniversityService:
    def __init__(self, university_repo):
        self.university_repo = university_repo

    def get_all_universities(self):
        return [
            UniversityOut(id=u.id, name=u.name)
            for u in self.university_repo.get_all_universities()
        ]

