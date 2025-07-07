from pydantic import BaseModel, field_validator, model_validator, EmailStr

class FacultyOut(BaseModel):
    id: int
    name: str
    university_id: int



    @field_validator("university_id")
    def validate_university_id(cls, value):
        if value <= 0:
            raise ValueError("University ID must be a positive integer.")
        return value

    class Config:
        orm_mode = True