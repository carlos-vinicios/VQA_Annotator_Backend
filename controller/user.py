from services.context import pwd_context
from schemas.user import UserAuth
from models.user import User
from controller.queue import AnnotationQueue
from env import EnvironmentVariables

ENV_VARS = EnvironmentVariables()

class UserController:

    def __init__(self) -> None:
        self.pwd_context = pwd_context
        self.annotation_queue = AnnotationQueue(
            ENV_VARS.MONGODB_URI
        )

    def get_user(self, email: str) -> User:
        return User.objects(email=email).first()

    def new_user(self, user: UserAuth):
        """Cria um novo usuário na base dados"""
        user_data = user.model_dump()
        user_data.pop('consent')
        User(**user_data).save()
        
        #atribuindo arquivos para aquele usuário
        self.annotation_queue.add_user_to_queue(user.email)
    