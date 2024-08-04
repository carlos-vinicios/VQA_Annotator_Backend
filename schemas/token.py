from pydantic import BaseModel
from typing import Union

class Token(BaseModel):
    email: str
    access_token: str
    refresh_token: Union[str, None] = None

class TokenData(BaseModel):
    email: Union[str, None] = None