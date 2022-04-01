from pydantic import BaseModel
import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str
    avathar_url: str | None = None
    is_admin: bool = False


class User(UserBase):
    id: int
    disabled: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    password: str
