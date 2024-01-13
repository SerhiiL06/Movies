import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from .db.config import settings

async_engine = create_async_engine(settings.get_db_config, echo=True)

async_session = async_sessionmaker(
    bind=async_engine, autoflush=False, class_=AsyncSession
)
