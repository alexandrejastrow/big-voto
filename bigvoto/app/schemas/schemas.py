from pydantic import BaseModel, EmailStr
from typing import List
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
    is_active: bool
    avathar_url: str | None = None
    is_admin: bool = False
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
    is_active: bool
    avathar_url: str | None = None
    is_admin: bool = False

    def dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "avathar_url": self.avathar_url,
            "is_active": self.is_active,
            "is_admin": self.is_admin
        }


class TokenPayload(BaseModel):
    sub: str | None = None


class EmailSchema(BaseModel):
    email: List[EmailStr]
