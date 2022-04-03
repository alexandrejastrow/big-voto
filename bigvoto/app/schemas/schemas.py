from pydantic import BaseModel
from typing import List, Any
import datetime
from uuid import UUID

# tokens schemas


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TokenPayload(BaseModel):
    sub: str | None = None
# users schemas


class UserBase(BaseModel):
    email: str


class User(UserBase):
    id: UUID
    username: str
    is_active: bool
    avathar_url: str | None = None
    is_admin: bool = False

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

# polls schemas


class PollBase(BaseModel):
    title: str
    description: str


class PollCreate(PollBase):
    start_date: datetime.datetime | None = None
    end_date: datetime.datetime | None = None

    def dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date
        }


class Poll(PollBase):
    id: UUID
    start_date: datetime.datetime
    end_date: datetime.datetime
    is_active: bool
    author: User
    alternatives: List[Any]

    class Config:
        orm_mode = True

# alternatives schemas


class AlternativeBase(BaseModel):
    name: str
    image: str | None = None


class AlternativeCreate(AlternativeBase):

    def dict(self):
        return {
            "name": self.name,
            "image": self.image
        }


class Alternative(AlternativeBase):
    id: UUID
    poll: Poll
    votes: int = 0

    class Config:
        orm_mode = True
