from fastapi import APIRouter, Depends, HTTPException, Response, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from email_validator import validate_email, EmailNotValidError

from app.schemas.schemas import UserInDB, User, Token, UserUpdated
from app.services.user_service import UserService
from app.security.jwt_pass import get_password_hash
from app.security.auth import authenicate, create_access_token, get_user_token
from app.settings.settings import app_settings

router = APIRouter()


async def email_validate(email: str):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


@router.post('/', response_model=User)
async def create_user(user: UserInDB, response: Response, userservice: UserService = Depends()):

    if not email_validate(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "detail": "Email is not valid."})

    user.password = get_password_hash(user.password)
    user_save = await userservice.create(user)
    response.status_code = status.HTTP_201_CREATED
    return user_save


@router.delete('/')
async def delete_user(user: User = Security(get_user_token)):
    user_delete = await UserService().delete_user(user.id)
    if not user_delete:
        user_delete = "User deleted successfully."
    return {"user_delete": user_delete}


@router.post('/auth', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenicate(form_data.username, form_data.password)
    access_token = await create_access_token(
        data={'sub': user.id}, expires_delta=app_settings.access_token_expire_minutes)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.put('/')
async def update_user(
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        avathar_url: str | None = None,
        disabled: int | bool = True,
        is_admin: int | bool = False,
        response: Response = Response,
        user: User = Security(get_user_token)):

    if user.is_admin == 1 or user.is_admin:
        is_admin = True
    if email:
        if not email_validate(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                "detail": "Email is not valid."})
        disabled = False
    if password:
        password = get_password_hash(password)

    new_user = UserUpdated(
        username=username if username else user.username,
        email=email if email else user.email,
        password=password if password else user.password,
        avathar_url=avathar_url if avathar_url else user.avathar_url,
        disabled=disabled,
        is_admin=is_admin
    )

    new_user = await UserService().update_user(user.id, new_user)
    response.status_code = status.HTTP_200_OK
    del new_user.password
    return {'detail': 'User updated successfully.', 'user': new_user}
