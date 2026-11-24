import asyncio
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, status

from app.core.config import get_settings
from app.observability.prometheus import APPLICATION_ERRORS_TOTAL

router = APIRouter(prefix="/admin", tags=["admin"])


def _check_admin_authorization(settings, authorization: Optional[str]) -> None:
    if not settings.enable_admin_endpoints:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    expected_token = f"Bearer {settings.admin_token}"
    if authorization != expected_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token",
        )


@router.post("/simulate-failure")
async def simulate_failure(
    failure_type: str,
    duration_seconds: int = 30,
    authorization: Optional[str] = Header(None),
) -> dict:
    settings = get_settings()
    _check_admin_authorization(settings, authorization)

    if failure_type == "high_error_rate":
        for _ in range(10):
            APPLICATION_ERRORS_TOTAL.inc()
        return {
            "failure_type": failure_type,
            "duration_seconds": duration_seconds,
            "status": "injected_errors",
        }

    if failure_type == "high_latency":
        await asyncio.sleep(min(duration_seconds, 10))
        return {
            "failure_type": failure_type,
            "duration_seconds": duration_seconds,
            "status": "latency_injected",
        }

    if failure_type == "dependency_failure":
        return {
            "failure_type": failure_type,
            "duration_seconds": duration_seconds,
            "status": "dependency_failure_simulated",
        }

    if failure_type == "cpu_stress":
        _ = sum(i * i for i in range(1_000_000))
        return {
            "failure_type": failure_type,
            "duration_seconds": duration_seconds,
            "status": "cpu_stress_completed",
        }

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unknown failure type: {failure_type}",
    )


@router.post("/crash")
async def crash(authorization: Optional[str] = Header(None)) -> dict:
    settings = get_settings()
    _check_admin_authorization(settings, authorization)
    raise SystemExit(1)
