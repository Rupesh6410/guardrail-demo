import logging
import sys
from typing import Any

from pythonjsonlogger import jsonlogger

from app.core.config import get_settings


class GuardrailJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: dict[str, Any], record: logging.LogRecord, message_dict: dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)
        settings = get_settings()
        log_record.setdefault("service", settings.service_name)
        log_record.setdefault("environment", settings.environment)
        log_record.setdefault("level", record.levelname)
        log_record["logger"] = record.name


def setup_logging() -> None:
    settings = get_settings()
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = GuardrailJsonFormatter(
        "%(timestamp)s %(level)s %(service)s %(environment)s %(message)s %(request_id)s %(method)s %(endpoint)s %(status_code)s %(duration_ms)s"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = [handler]

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
