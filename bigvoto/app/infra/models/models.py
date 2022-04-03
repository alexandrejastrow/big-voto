from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    avathar_url = Column(String, default="", nullable=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    polls = relationship("Poll", back_populates="author")

    def __str__(self):
        return f'<User(id={self.id}, username={self.username}, is_admin={self.is_admin}, is_active={self.is_active})>'

    def dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "is_active": self.is_active,
            "avathar_url": self.avathar_url,
        }


class Poll(Base):
    __tablename__ = "polls"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    author_id = Column(String, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="polls")

    alternatives = relationship("Alternative", back_populates="poll")

    def __str__(self):
        return f'<Poll(id={self.id}, title={self.title}, start_date={self.start_date}, end_date={self.end_date}, is_active={self.is_active})>'

    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": self.is_active,
            "author": self.author.dict(),
            "alternatives": [a.dict() for a in self.alternatives]
        }


class Alternative(Base):
    __tablename__ = "alternatives"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    image = Column(String, nullable=True, default="")
    votes = Column(Integer, default=0)

    poll_id = Column(String, ForeignKey("polls.id"), nullable=False)

    poll = relationship("Poll", back_populates="alternatives")
