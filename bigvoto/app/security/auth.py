from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import JWTError, jwt

from app.settings.settings import app_settings
from app.security.jwt_pass import verify_password
from app.schemas.schemas import TokenPayload, User
from app.services.user_service import UserService

auth2 = OAuth2PasswordBearer(
    tokenUrl='/api/users/auth',
)
NOT_AUTHORIZED = 0
TOKEN_EXPIRE_MINUTES = 600


async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    try:

        encoded_jwt = jwt.encode(
            to_encode, app_settings.secret_key, algorithm=app_settings.algorithm)
    except JWTError:
        return

    return encoded_jwt


async def authenicate(email: str, password: str) -> User:
    user = await UserService().get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'detail': 'Incorrect username or password'})

    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'detail': 'Incorrect username or password'})
    if user.disabled == NOT_AUTHORIZED:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'detail': 'User is disabled'})
    return user


async def get_user_token(token: str = Depends(auth2)):

    try:
        payload = jwt.decode(token, app_settings.secret_key,
                             algorithms=[app_settings.algorithm])
        token_data = TokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail={
                'detail': 'Ivalid Token'})

    user = await UserService().get_user_by_id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail={
                'detail': 'User not found'})
    return user
