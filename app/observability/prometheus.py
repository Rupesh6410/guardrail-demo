import time
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST


HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)

HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests currently in progress",
    ["method", "endpoint"],
)

APPLICATION_ERRORS_TOTAL = Counter(
    "application_errors_total",
    "Total application errors",
    ["endpoint", "error_type"],
)

ORDERS_CREATED_TOTAL = Counter(
    "orders_created_total",
    "Total orders created",
)

APPLICATION_UPTIME_SECONDS = Gauge(
    "application_uptime_seconds",
    "Application uptime in seconds",
)

DATABASE_CONNECTION_STATUS = Gauge(
    "database_connection_status",
    "Database connection status (1 = connected, 0 = disconnected)",
)


_start_time = time.time()


def record_uptime() -> None:
    APPLICATION_UPTIME_SECONDS.set(time.time() - _start_time)


def get_metrics_output() -> tuple[str, str]:
    record_uptime()
    return generate_latest().decode("utf-8"), CONTENT_TYPE_LATEST
