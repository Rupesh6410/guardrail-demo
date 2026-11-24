from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app.api.routes.admin import router as admin_router
from app.api.routes.health import router as health_router
from app.api.routes.orders import router as orders_router
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging
from app.middleware.metrics import MetricsMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.observability.prometheus import get_metrics_output

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Application starting up")
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title="Guardrail API",
    description="Production-style FastAPI microservice for the Guardrail platform demo",
    version="0.1.0",
    lifespan=lifespan,
    debug=settings.debug,
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(MetricsMiddleware)

app.include_router(health_router)
app.include_router(orders_router)

if settings.enable_admin_endpoints:
    app.include_router(admin_router)


@app.get("/metrics", response_class=PlainTextResponse, tags=["metrics"])
async def metrics() -> str:
    output, _ = get_metrics_output()
    return output


@app.get("/", tags=["root"])
async def root() -> dict:
    return {
        "service": settings.service_name,
        "version": "0.1.0",
        "environment": settings.environment,
        "status": "running",
    }
