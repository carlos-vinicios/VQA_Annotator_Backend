from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    scopes={
        "user": "Read information about reports.", 
        "admin": "Manage information about reports."
    },
)

security = HTTPBearer()