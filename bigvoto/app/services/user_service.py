from app.infra.models import models
from app.infra.sqlalchemy import database
from app.schemas.schemas import UserInDB


class UserService:
    async def create(self, user: UserInDB):
        async with database.async_session() as session:
            user_db = models.User(
                username=user.username,
                password=user.password,
                email=user.email,
                is_admin=user.is_admin,
                avathar_url=user.avathar_url
            )
            session.add(user_db)
            await session.commit()
            await session.refresh(user_db)
            return user_db
