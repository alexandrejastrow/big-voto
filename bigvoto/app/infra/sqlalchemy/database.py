from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.settings.settings import db_settings

if db_settings.DEV_MODE:
    engine = create_async_engine(
        db_settings.DATABASE_URL_DEV, echo=True)
else:
    url = db_settings.DATABASE_URL
    if url and url.startswith("postgres+asyncpg//"):
        url = url.replace("postgres+asyncpg//", "postgresql+asyncpg//")
    engine = create_async_engine(url)


async_session = sessionmaker(engine, class_=AsyncSession)
