from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_list_products_returns_active_products() -> None:
    response = client.get("/products")

    assert response.status_code == 200

    payload = response.json()

    assert payload["count"] == 4
    assert len(payload["items"]) == 4
    assert all(product["is_active"] for product in payload["items"])


def test_get_existing_product() -> None:
    response = client.get("/products/1")

    assert response.status_code == 200

    payload = response.json()

    assert payload["id"] == 1
    assert payload["name"] == "Wireless Keyboard"


def test_get_unknown_product_returns_404() -> None:
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product 999 was not found."


def test_get_inactive_product_returns_404() -> None:
    response = client.get("/products/5")

    assert response.status_code == 404


def test_product_list_contains_out_of_stock_product() -> None:
    response = client.get("/products")

    payload = response.json()

    out_of_stock_products = [
        product
        for product in payload["items"]
        if product["stock_quantity"] == 0
    ]

    assert len(out_of_stock_products) == 1
    assert out_of_stock_products[0]["name"] == "Laptop Stand"
