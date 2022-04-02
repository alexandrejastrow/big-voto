from sqlalchemy.future import select
from sqlalchemy import delete, update
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
                avathar_url=user.avathar_url
            )
            session.add(user_db)
            await session.commit()
            await session.refresh(user_db)
            return user_db

    async def get_user_by_email(self, email: str):
        async with database.async_session() as session:
            result = await session.execute(select(models.User).where(models.User.email == email))
            user_db = result.scalar()
            return user_db

    async def get_user_by_id(self, id: int):
        async with database.async_session() as session:
            result = await session.execute(select(models.User).where(models.User.id == id))
            user_db = result.scalar()
            return user_db

    async def delete_user(self, id: str):
        async with database.async_session() as session:
            await session.execute(delete(models.User).where(models.User.id == id))
            result = await session.commit()
            return result

    async def update_user(self, id: str, **args) -> bool:
        async with database.async_session() as session:
            for value in args:
                await session.execute(update(models.User).where(models.User.id == id).values(**{value: args[value]}))
                await session.commit()
        return True
