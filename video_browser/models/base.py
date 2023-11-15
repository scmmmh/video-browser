"""Functionality for database access."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from threading import local
from typing import Callable

from video_browser.settings import settings

logger = logging.getLogger(__name__)
local_cache = local()


def get_engine() -> AsyncEngine:
    """Get a thread-local engine."""
    try:
        return local_cache.engine
    except Exception:
        local_cache.engine = create_async_engine(str(settings.dsn))
        return local_cache.engine


def get_session_factory() -> Callable[[], AsyncSession]:
    """Get a thread-local session factory."""
    try:
        return local_cache.session_factory
    except Exception:
        local_cache.session_factory = sessionmaker(bind=get_engine(), expire_on_commit=False, class_=AsyncSession)
        return local_cache.session_factory


async def db_session() -> AsyncSession:
    """Get a database session."""
    db = get_session_factory()()
    try:
        yield db
    finally:
        await db.close()
