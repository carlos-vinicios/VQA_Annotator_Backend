from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    age: str
    gender: str
    education_level: str
    current_occupation: str
    occupation_description: Optional[str] = None
    email: EmailStr
    consent: bool

class UserAuth(UserBase):
    token: str
