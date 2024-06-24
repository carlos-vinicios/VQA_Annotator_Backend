from pydantic import BaseModel
from typing import List, Union
from schemas.user import UserBase

class Token(UserBase):
    access_token: str
    refresh_token: Union[str, None] = None
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None