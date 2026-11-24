# guardrail-demo

Production-style FastAPI microservice acting as the application workload deployed and monitored by the Guardrail platform.

The service generates meaningful traffic, exposes operational metrics, produces structured JSON logs, provides Kubernetes-friendly health checks, and simulates real production failures for demonstrating the complete DevSecOps and SRE lifecycle.

## Project Structure

```text
guardrail-demo/
├── app/
│   ├── main.py                 # FastAPI application entrypoint
│   ├── api/
│   │   └── routes/
│   │       ├── health.py       # /health/* endpoints
│   │       ├── orders.py       # /api/v1/orders endpoints
│   │       └── admin.py        # /admin/* failure simulation (dev only)
│   ├── core/
│   │   ├── config.py           # Pydantic settings
│   │   └── logging.py          # JSON structured logging
│   ├── middleware/
│   │   ├── request_id.py       # X-Request-ID correlation middleware
│   │   └── metrics.py          # Prometheus request instrumentation
│   ├── observability/
│   │   └── prometheus.py       # Prometheus metric definitions
│   ├── services/
│   │   └── order_service.py    # In-memory order CRUD service
│   └── schemas/
│       └── orders.py           # Pydantic order models
├── tests/
│   ├── test_health.py
│   ├── test_orders.py
│   └── test_metrics.py
├── Dockerfile
├── .dockerignore
├── .env.example
├── requirements.txt
└── README.md
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.12 + FastAPI |
| Application Server | Uvicorn |
| Metrics | Prometheus client |
| Logging | Python logging + python-json-logger |
| Testing | Pytest + HTTPX TestClient |
| Containerization | Docker |

## Endpoints

### Health Checks (Kubernetes probes)

| Endpoint | Method | Purpose | Probe Type |
|----------|--------|---------|------------|
| `/health/live` | GET | Is the application process alive? | Liveness |
| `/health/ready` | GET | Can the application serve requests? | Readiness |
| `/health/startup` | GET | Has application initialization completed? | Startup |

Example responses:

**Liveness:**
```json
{"status": "alive", "service": "guardrail-api"}
```

**Readiness:**
```json
{"status": "ready", "database": "connected", "dependencies": "healthy"}
```

**Startup:**
```json
{"status": "started"}
```

### Business API

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/api/v1/orders` | POST | Create an order | `201 Created` |
| `/api/v1/orders` | GET | List all orders | `200 OK` |
| `/api/v1/orders/{id}` | GET | Retrieve an order by ID | `200 OK` / `404` |
| `/api/v1/orders/{id}` | DELETE | Delete an order by ID | `204 No Content` / `404` |

**Create order request body:**
```json
{
  "customer_name": "John Doe",
  "item": "Widget",
  "quantity": 2,
  "price": 9.99
}
```

### Metrics

| Endpoint | Method | Format | Description |
|----------|--------|--------|-------------|
| `/metrics` | GET | Plain text (Prometheus) | All application and process metrics |

Key metrics:
- `http_requests_total` — Counter, labels: method, endpoint, status_code
- `http_request_duration_seconds` — Histogram, labels: method, endpoint
- `http_requests_in_progress` — Gauge, labels: method, endpoint
- `application_errors_total` — Counter, labels: endpoint, error_type
- `orders_created_total` — Counter
- `application_uptime_seconds` — Gauge
- `database_connection_status` — Gauge (1 = connected, 0 = disconnected)

Standard Python process metrics are also exposed automatically.

### Admin / Failure Simulation (development only)

Requires `Authorization: Bearer <ADMIN_TOKEN>` header and `ENABLE_ADMIN_ENDPOINTS=true`.

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/admin/simulate-failure` | POST | Inject a controlled failure scenario |
| `/admin/crash` | POST | Force process exit (Kubernetes liveness restart) |

Supported `failure_type` values: `high_error_rate`, `high_latency`, `dependency_failure`, `cpu_stress`.

## Getting Started

### Local Development

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment example
cp .env.example .env

# 4. Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API documentation is available at `http://localhost:8000/docs` (Swagger UI).

### Verify Endpoints

```bash
# Health checks
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready
curl http://localhost:8000/health/startup

# Metrics
curl http://localhost:8000/metrics

# Create an order
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Jane Doe","item":"Gadget","quantity":1,"price":5.00}'

# List orders
curl http://localhost:8000/api/v1/orders
```

### Run Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

### Docker

```bash
# Build image
docker build -t guardrail-api:latest .

# Run container
docker run -p 8000:8000 -e ENVIRONMENT=production guardrail-api:latest
```

## Configuration

Environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Deployment environment label |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `PORT` | `8000` | Application server port |
| `DEBUG` | `false` | Enable debug mode |
| `ENABLE_ADMIN_ENDPOINTS` | `true` | Enable admin/failure simulation endpoints |
| `ADMIN_TOKEN` | `dev-admin-token` | Bearer token for admin endpoints |

## Logging

Logs are emitted as JSON to stdout. Example:

```json
{
  "timestamp": "2026-11-24T10:30:00Z",
  "level": "INFO",
  "service": "guardrail-api",
  "environment": "production",
  "message": "Application starting up",
  "request_id": null,
  "method": null,
  "endpoint": null,
  "status_code": null,
  "duration_ms": null
}
```

Every incoming request receives a unique `X-Request-ID` correlation header that is propagated through logs and response headers.

## Kubernetes Readiness

The app is designed for Kubernetes deployment with:

- Liveness probe: `GET /health/live`
- Readiness probe: `GET /health/ready`
- Startup probe: `GET /health/startup`
- Prometheus scrape: `GET /metrics` on port 8000
- Container port: 8000

## Next Phases

Per the development roadmap:

1. OpenTelemetry distributed tracing
2. PostgreSQL integration (replace in-memory storage)
3. Kubernetes deployment manifests (Deployment, Service, ConfigMap, Secret, PDB)
4. Prometheus + Grafana + Loki observability stack
5. Blue-green / canary deployment demonstrations
