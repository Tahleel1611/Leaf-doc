"""Test for health check endpoint."""
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "model_loaded" in data
    assert isinstance(data["model_loaded"], bool)


def test_root_endpoint(client: TestClient):
    """Test the root endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "name" in data
    assert "version" in data
    assert "docs" in data
