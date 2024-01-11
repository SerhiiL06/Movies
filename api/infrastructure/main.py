from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
    AsyncEngine,
)
from .db.config import DatabaseCORE
import logging


async def get_async_engine(settings: DatabaseCORE):
    engine = create_async_engine(settings.get_db_config(), future=True)
    logging.info("Connect to engine")
    yield engine
    await engine.dispose()


async def get_asyns_session(engine: AsyncEngine):
    session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    return session
