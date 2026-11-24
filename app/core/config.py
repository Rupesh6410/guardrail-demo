import os
from functools import lru_cache


class Settings:
    service_name: str = "guardrail-api"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    enable_admin_endpoints: bool = (
        os.getenv("ENABLE_ADMIN_ENDPOINTS", "true").lower() == "true"
    )
    admin_token: str = os.getenv("ADMIN_TOKEN", "dev-admin-token")


@lru_cache
def get_settings() -> Settings:
    return Settings()
