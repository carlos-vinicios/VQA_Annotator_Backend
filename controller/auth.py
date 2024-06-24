from services.context import pwd_context
from datetime import datetime, timedelta
from .user import UserController
import jwt

from env import EnvironmentVariables
BACKEND_ENV = EnvironmentVariables()

class AuthController:

    def __init__(self) -> None:
        self.pwd_context = pwd_context
        self.users = UserController()
        self.access_token_expires = timedelta(minutes=BACKEND_ENV.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    def decode_token(self, credentials):
        return jwt.decode(
            credentials, 
            BACKEND_ENV.SECRET_KEY, 
            algorithms=[BACKEND_ENV.ALGORITHM]
        )

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, email: str, token: str):
        user = self.users.get_user(email)
        if not user:
            return False
        if not token == user.token: #self.verify_password(token, user.hashed_password):
            return False
        return user

    def create_access_token(self, email: str):
        to_encode = {
            "sub": email,
        }
        if self.access_token_expires:
            expire = datetime.utcnow() + self.access_token_expires
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, BACKEND_ENV.SECRET_KEY, algorithm=BACKEND_ENV.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, email: str):
        to_encode = {
            "sub": email, 
            "scopes": "refresh_token"
        }
        if self.access_token_expires:
            expire = datetime.utcnow() + self.access_token_expires + timedelta(hours=24)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, BACKEND_ENV.SECRET_KEY, algorithm=BACKEND_ENV.ALGORITHM)
        
        return encoded_jwt