from fastapi import APIRouter, Depends, HTTPException, status, Security, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from email_validator import validate_email, EmailNotValidError
from jose import JWTError, jwt

from app.schemas.schemas import UserInDB, User, Token, UserUpdated
from app.services.user_service import UserService
from app.security.jwt_pass import get_password_hash
from app.security.auth import authenicate, create_access_token, get_user_token
from app.settings.settings import app_settings
from app.services.email_service import mail_send
router = APIRouter(tags=["User"])


async def email_validate(email: str):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


@router.post('/')
async def create_user(user: UserInDB, task: BackgroundTasks, user_service: UserService = Depends()):

    if not email_validate(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "detail": "Email is not valid."})

    user.password = get_password_hash(user.password)
    verify_user = await user_service.get_user_by_email(user.email)
    if verify_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'detail': 'User already exists.'})
    user_save = await user_service.create(user)
    if not user_save:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "detail": "User not created."})

    task.add_task(mail_send, user_save.id, user_save.email, user_save.username)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created, verify your email."})


@router.delete('/')
async def delete_user(user: User = Security(get_user_token), user_service: UserService = Depends()):
    user_delete = await user_service.delete_user(user.id)
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
        is_active: bool = True,
        task: BackgroundTasks = BackgroundTasks(),
        user: User = Security(get_user_token),
        user_service: UserService = Depends()):

    if email:
        if not email_validate(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                "detail": "Email is not valid."})
        is_active = False

    if password:
        password = get_password_hash(password)

    new_user = UserUpdated(
        username=username if username else user.username,
        email=email if email else user.email,
        password=password if password else user.password,
        avathar_url=avathar_url if avathar_url else user.avathar_url,
        is_active=is_active
    )

    await user_service.update_user(user.id, **new_user.dict())
    if not is_active:
        task.add_task(mail_send, user.id, email, user.username)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User updated successfully."})


@router.get('/mail/{id}')
async def resend_mail(id: str, task: BackgroundTasks):
    user = await UserService().get_user_by_id(id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "detail": "User not found."})
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "detail": "Active user."})
    task.add_task(mail_send, user.id, user.email, user.username)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "resend mail."})


@router.get('/{id}', response_model=User)
async def get_user(id: str, user_service: UserService = Depends()):
    user = await user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "detail": "User not found."})
    return user


@router.get('/verify/{access_token}')
async def verify(access_token: str, user_service: UserService = Depends()):
    try:
        payload = jwt.decode(
            access_token, app_settings.secret_key, algorithms=['HS256'])
        user = await user_service.get_user_by_id(payload['sub'])
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                "detail": "User not found."})

        if not user.is_active:
            user.is_active = True
            await user_service.update_user(user.id, **user.dict())
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            "detail": "Invalid token."})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Verified user."})
