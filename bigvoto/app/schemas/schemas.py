from pydantic import BaseModel
import datetime
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    email: str


class User(UserBase):
    id: UUID
    username: str
    disabled: int | bool
    avathar_url: str | None = None
    is_admin: int | bool = False
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    password: str


class UserInDB(UserBase):
    password: str
    username: str
    avathar_url: str | None = None


class UserUpdated(UserBase):
    password: str | None = None
    username: str | None = None
    avathar_url: str | None = None
    disabled: int | bool
    avathar_url: str | None = None
    is_admin: int | bool = False


class TokenPayload(BaseModel):
    sub: str | None = None
