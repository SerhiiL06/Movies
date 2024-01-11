from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker
from .db.config import settings
import logging


async_engine = create_async_engine(settings.get_db_config)

async_session = sessionmaker(bind=async_engine, autoflush=False, class_=AsyncSession)
