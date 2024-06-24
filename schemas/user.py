from pydantic import BaseModel
from typing import Union, List

class UserBase(BaseModel):
    email: str
    stage: str

class UserAuth(UserBase):
    token: str
