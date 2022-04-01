from fastapi import APIRouter, Depends, HTTPException, Response, status
from email_validator import validate_email, EmailNotValidError

from app.schemas.schemas import UserInDB, User
from app.services.user_service import UserService
from app.security.jwt_pass import verify_password, get_password_hash

router = APIRouter(prefix='/users')


@router.post('/', response_model=User)
async def create_user(user: UserInDB, response: Response, userservice: UserService = Depends()):
    try:
        validate_email(user.email)
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "detail": "Email is not valid."})

    user.password = get_password_hash(user.password)
    user_save = await userservice.create(user)
    response.status_code = status.HTTP_201_CREATED
    return user_save


@router.get('/')
async def get_user():
    return "fasf"


@router.put('/')
async def update_user():
    return "fasf"


@router.delete('/')
async def delete_user():
    return "fasf"
