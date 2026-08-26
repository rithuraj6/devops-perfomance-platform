def test_create_product(client):
    response = client.post(
        "/api/products",
        json={
            "name": "Test Laptop",
            "category": "Electronics",
            "price": 50000,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Laptop"
    assert data["category"] == "Electronics"
    assert data["price"] == 50000


def test_get_product(client):
    create_response = client.post(
        "/api/products",
        json={
            "name": "Test Phone",
            "category": "Electronics",
            "price": 45000,
        },
    )

    product_id = create_response.json()["id"]

    response = client.get(
        f"/api/products/{product_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Test Phone"


def test_get_nonexistent_product(client):
    response = client.get("/api/products/99999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Product not found"
    }


def test_list_products(client):
    client.post(
        "/api/products",
        json={
            "name": "Laptop",
            "category": "Electronics",
            "price": 75000,
        },
    )

    client.post(
        "/api/products",
        json={
            "name": "Chair",
            "category": "Furniture",
            "price": 5000,
        },
    )

    response = client.get("/api/products")

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 2


def test_cache_returns_same_products(client):
    client.post(
        "/api/products",
        json={
            "name": "Cached Laptop",
            "category": "Electronics",
            "price": 80000,
        },
    )

    first_response = client.get("/api/products")
    second_response = client.get("/api/products")

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    assert first_response.json() == second_response.json()


def test_product_not_found(client):
    response = client.get("/api/products/999999")

    assert response.status_code == 404
