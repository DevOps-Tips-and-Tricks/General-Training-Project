def test_create_item(client):
    payload = {
        "name": "Wireless Mouse",
        "description": "Ergonomic 2.4GHz mouse",
        "price": 29.99
    }
    response = client.post("/items/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert "id" in data  # Ensure an ID was generated


def test_read_item(client):
    # First, create an item to read
    create_response = client.post("/items/", json={"name": "Keyboard", "price": 45.00})
    item_id = create_response.json()["id"]

    # Now, read it back
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Keyboard"
    assert response.json()["id"] == item_id


def test_read_item_not_found(client):
    response = client.get("/items/fake-id-123")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_list_items(client):
    # Create two items
    client.post("/items/", json={"name": "Monitor", "price": 199.99})
    client.post("/items/", json={"name": "Cable", "price": 9.99})

    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert type(data) == list


def test_update_item(client):
    # Create an item
    create_response = client.post("/items/", json={"name": "Headphones", "price": 99.00})
    item_id = create_response.json()["id"]

    # Update the item
    update_payload = {
        "name": "Headphones Pro",
        "description": "Noise cancelling",
        "price": 149.00
    }
    response = client.put(f"/items/{item_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Headphones Pro"
    assert data["price"] == 149.00
    assert data["id"] == item_id


def test_delete_item(client):
    # Create an item
    create_response = client.post("/items/", json={"name": "Webcam", "price": 59.99})
    item_id = create_response.json()["id"]

    # Delete the item
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Item deleted successfully"

    # Verify it is gone
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
