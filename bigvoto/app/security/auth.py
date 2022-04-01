from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import JWTError, jwt

from app.settings.settings import app_settings
from app.security.jwt_pass import verify_password

auth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

TOKEN_EXPIRE_MINUTES = 600


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    try:

        encoded_jwt = jwt.encode(
            to_encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM)
    except JWTError:
        return

    return encoded_jwt


# TODO: get user in Db
def authenicate(email: str, password: str):
    if not email:
        return False
    if not verify_password(password, password):
        return False
    return email
