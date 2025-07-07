from pydantic import BaseModel, field_validator, model_validator, EmailStr

class MajorOut(BaseModel):
    id: int
    name: str
    faculty_id: int
    class Config:
        orm_mode = True