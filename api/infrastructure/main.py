import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .db.config import settings

async_engine = create_async_engine(settings.get_db_config)

async_session = sessionmaker(bind=async_engine, autoflush=False, class_=AsyncSession)
