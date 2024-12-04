import pytest
from app import app

@pytest.fixture
def client():
    """Fixture für Test-Client"""
    with app.test_client() as client:
        yield client

def test_get_items(client):
    """Test für GET /items"""
    response = client.get('/items')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "items" in data
    assert len(data["items"]) > 0

def test_get_item(client):
    """Test für GET /items/<id>"""
    response = client.get('/items/1')
    assert response.status_code == 200
    data = response.get_json()
    assert "id" in data
    assert data["id"] == 1

def test_get_item_not_found(client):
    """Test für GET /items/<id> - Item nicht gefunden"""
    response = client.get('/items/999')
    assert response.status_code == 404
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Item not found"

def test_create_item(client):
    """Test für POST /items"""
    new_item = {"name": "New Item", "description": "This is a new item"}
    response = client.post('/items', json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == "New Item"
    assert data["description"] == "This is a new item"

def test_create_item_invalid_data(client):
    """Test für POST /items - Ungültige Daten"""
    invalid_item = {"name": "Invalid Item"}
    response = client.post('/items', json=invalid_item)
    assert response.status_code == 400
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Invalid data"

def test_update_item(client):
    """Test für PUT /items/<id>"""
    updated_item = {"name": "Updated Item", "description": "Updated description"}
    response = client.put('/items/1', json=updated_item)
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated Item"
    assert data["description"] == "Updated description"

def test_update_item_not_found(client):
    """Test für PUT /items/<id> - Item nicht gefunden"""
    updated_item = {"name": "Updated Item", "description": "Updated description"}
    response = client.put('/items/999', json=updated_item)
    assert response.status_code == 404
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Item not found"

def test_delete_item(client):
    """Test für DELETE /items/<id>"""
    response = client.delete('/items/1')
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Item deleted successfully"

def test_delete_item_not_found(client):
    """Test für DELETE /items/<id> - Item nicht gefunden"""
    response = client.delete('/items/999')
    assert response.status_code == 404
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Item not found"
