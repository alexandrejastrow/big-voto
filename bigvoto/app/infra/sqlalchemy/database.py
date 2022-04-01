from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.settings.settings import db_settings

if db_settings.dev_mode:
    engine = create_async_engine(
        db_settings.database_url_dev, echo=True)
else:
    url = db_settings.database_url
    if url and url.startswith("postgres+asyncpg//"):
        url = url.replace("postgres+asyncpg//", "postgresql+asyncpg//")
    engine = create_async_engine(db_settings.database_url)


async_session = sessionmaker(engine, class_=AsyncSession)

Base = declarative_base()
