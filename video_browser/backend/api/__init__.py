"""API for the frontend video browser."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from video_browser.backend.api import auth, playlists, videos
from video_browser.models import db_session
from video_browser.settings import settings


router = APIRouter(prefix="/api")
router.include_router(auth.router)
router.include_router(playlists.router)
router.include_router(videos.router)


@router.get("/")
async def get_api_config(dbsession: Annotated[AsyncSession, Depends(db_session)]) -> dict:
    """Get the API configuration."""
    return {"video_base_url": settings.video_base_url}
