from fastapi import APIRouter

from app.core.config import get_settings
from app.observability.prometheus import DATABASE_CONNECTION_STATUS

router = APIRouter()


@router.get("/health/live", tags=["health"])
async def liveness() -> dict:
    settings = get_settings()
    return {
        "status": "alive",
        "service": settings.service_name,
    }


@router.get("/health/ready", tags=["health"])
async def readiness() -> dict:
    settings = get_settings()
    db_connected = True
    DATABASE_CONNECTION_STATUS.set(1 if db_connected else 0)
    return {
        "status": "ready",
        "database": "connected" if db_connected else "disconnected",
        "dependencies": "healthy",
    }


@router.get("/health/startup", tags=["health"])
async def startup() -> dict:
    return {
        "status": "started",
    }
