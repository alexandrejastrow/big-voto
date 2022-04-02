from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.infra.sqlalchemy.database import Base
import uuid


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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

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
