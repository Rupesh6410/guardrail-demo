from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_order() -> None:
    payload = {
        "customer_name": "John Doe",
        "item": "Widget",
        "quantity": 2,
        "price": 9.99,
    }
    response = client.post("/api/v1/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["item"] == "Widget"
    assert data["quantity"] == 2
    assert data["price"] == 9.99
    assert data["status"] == "pending"
    assert "id" in data


def test_list_orders() -> None:
    client.post(
        "/api/v1/orders",
        json={"customer_name": "Jane Doe", "item": "Gadget", "quantity": 1, "price": 5.0},
    )
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_order_not_found() -> None:
    response = client.get("/api/v1/orders/nonexistent-id")
    assert response.status_code == 404


def test_delete_order() -> None:
    create_response = client.post(
        "/api/v1/orders",
        json={"customer_name": "Temp", "item": "Thing", "quantity": 1, "price": 1.0},
    )
    order_id = create_response.json()["id"]
    delete_response = client.delete(f"/api/v1/orders/{order_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/orders/{order_id}")
    assert get_response.status_code == 404


def test_create_order_validation_error() -> None:
    payload = {
        "customer_name": "",
        "item": "Widget",
        "quantity": 0,
        "price": -1.0,
    }
    response = client.post("/api/v1/orders", json=payload)
    assert response.status_code == 422
