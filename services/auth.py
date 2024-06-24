from fastapi import HTTPException, Depends, Security, status
from services.context import oauth2_scheme
from fastapi.security import SecurityScopes
from pydantic import ValidationError
from schemas.token import TokenData
from env import EnvironmentVariables
from controller.user import UserController
import jwt

async def get_current_user(
    security_scopes: SecurityScopes, 
    token: str = Depends(oauth2_scheme),
    users: UserController = Depends(UserController),
    BACKEND_ENV: EnvironmentVariables = Depends(EnvironmentVariables)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, BACKEND_ENV.SECRET_KEY, algorithms=[BACKEND_ENV.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except (ValidationError, Exception):
        raise credentials_exception
    
    user = users.get_user(token_data.email)
    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(
    current_user = Security(get_current_user, scopes=["user"])
):
    return current_user