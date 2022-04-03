from sqlalchemy.future import select
from sqlalchemy import update
from app.infra.models import models
from app.infra.sqlalchemy import database
from app.schemas.schemas import AlternativeCreate, PollCreate


class PollService:

    async def create(self, poll: PollCreate, author_id: str, is_active: bool = False):
        async with database.async_session() as session:
            poll_db = models.Poll(
                **poll.dict(), author_id=author_id, is_active=is_active)

            session.add(poll_db)
            await session.commit()
            await session.refresh(poll_db)
            return poll_db

    async def get_all(self, is_active: bool | None = None):
        async with database.async_session() as session:
            if is_active is None:
                result = await session.execute(select(models.Poll).order_by(models.Poll.start_date.desc()))
            else:
                result = await session.execute(select(models.Poll).where(models.Poll.is_active == is_active).order_by(models.Poll.start_date.desc()))

            return [dict(row) for row in result]

    async def get_by_id(self, poll_id: str):
        async with database.async_session() as session:
            result = await session.execute(select(models.Poll).where(models.Poll.id == poll_id))
            return result.first()

    async def active_polls(self, poll_id: str, is_active: bool):
        async with database.async_session() as session:
            await session.execute(update(models.Poll).where(models.Poll.id == poll_id).values(is_active=is_active))
            await session.commit()


class AlternativeService:

    async def create(self, alternative: AlternativeCreate, poll_id: str):
        async with database.async_session() as session:
            alternative_db = models.Alternative(
                **alternative.dict(), poll_id=poll_id)

            session.add(alternative_db)
            await session.commit()
            await session.refresh(alternative_db)
            return alternative_db

    async def get_all(self, poll_id: str):
        async with database.async_session() as session:

            result = await session.execute(select(models.Alternative).where(models.Alternative.poll_id == poll_id))
            return [dict(row) for row in result]
