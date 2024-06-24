from fastapi import HTTPException, Depends, Security
from services.router import router
from services.context import security
from schemas.token import Token
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials
)
from controller.user import UserController
from controller.auth import AuthController
import jwt

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    auth = Depends(AuthController)
):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    
    access_token = auth.create_access_token(user.email)
    refresh_token = auth.create_refresh_token(user.email)
    response = user.to_mongo().to_dict()
    response.update({
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer", 
    })

    return response 

@router.post("/refresh_token", response_model=Token)
async def refresh(
    credentials: HTTPAuthorizationCredentials = Security(security),
    auth = Depends(AuthController), 
    users = Depends(UserController)
):
    try:
        payload = auth.decode_token(credentials.credentials)
        if (payload['scopes'] == 'refresh_token'):
            user = users.get_user(payload['sub'])
            access_token = auth.create_access_token(user.email)
            response = user.to_mongo().to_dict()
            response.update({
                "access_token": access_token,
                "token_type": "bearer", 
            })
            return response
        raise HTTPException(status_code=401, detail='O escopo é inválido para o Token')
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='O Refresh Token expirou')
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail='O Refresh Token é inválido')