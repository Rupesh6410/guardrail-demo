from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_metrics_endpoint() -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    text = response.text
    assert "http_requests_total" in text
    assert "http_request_duration_seconds" in text
    assert "application_uptime_seconds" in text
