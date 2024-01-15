from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from .db.config import settings

async_engine = create_async_engine(settings.get_db_config, echo=True)

async_session = async_sessionmaker(
    bind=async_engine, autoflush=False, class_=AsyncSession
)
