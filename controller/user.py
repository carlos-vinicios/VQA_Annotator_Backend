from services.context import pwd_context
from schemas.user import UserBase
from models.user import User
import secrets, string

class UserController:

    def __init__(self) -> None:
        self.pwd_context = pwd_context

    # def __gen_password(self) -> str:
    #     # define the alphabet
    #     letters = string.ascii_letters
    #     digits = string.digits
    #     special_chars = string.punctuation
    #     pwd_length = 6
    #     alphabet = letters + digits + special_chars
    #     pwd = ''
    #     for i in range(pwd_length):
    #         pwd += ''.join(secrets.choice(alphabet))
    #     return pwd

    # def get_password_hash(self, password):
    #     return self.pwd_context.hash(password)
    
    def get_user(self, email: str) -> User:
        return User.objects(email=email).first()
    