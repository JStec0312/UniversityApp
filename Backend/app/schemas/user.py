from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: str 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    display_name: str

    class Config:
        orm_mode = True