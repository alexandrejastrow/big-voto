from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.infra.sqlalchemy.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Integer, default=0)
    disabled = Column(Integer, default=0)
    avathar_url = Column(String, default="", nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())
