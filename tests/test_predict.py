"""Tests for prediction endpoint."""
import os
from io import BytesIO
from PIL import Image
import pytest
from fastapi.testclient import TestClient


def create_test_image(size=(224, 224), color=(0, 255, 0)) -> BytesIO:
    """Create a test image in memory."""
    image = Image.new("RGB", size, color)
    img_bytes = BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    return img_bytes


def test_predict_endpoint(client: TestClient):
    """Test the prediction endpoint with a valid image."""
    # Create test image
    img_bytes = create_test_image()
    
    # Send request
    response = client.post(
        "/api/predict",
        files={"file": ("test.jpg", img_bytes, "image/jpeg")}
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    
    # Validate response structure
    assert "id" in data
    assert "class" in data
    assert "confidence" in data
    assert "tips" in data
    assert "image_url" in data
    assert "created_at" in data
    
    # Validate data types
    assert isinstance(data["id"], str)
    assert isinstance(data["class"], str)
    assert isinstance(data["confidence"], float)
    assert 0.0 <= data["confidence"] <= 1.0
    assert isinstance(data["tips"], str)
    assert len(data["tips"]) > 0


def test_predict_invalid_file(client: TestClient):
    """Test prediction endpoint with invalid file."""
    # Send non-image file
    response = client.post(
        "/api/predict",
        files={"file": ("test.txt", b"not an image", "text/plain")}
    )
    
    # Should return 400 error
    assert response.status_code == 400
    assert "image" in response.json()["detail"].lower()


def test_predict_no_file(client: TestClient):
    """Test prediction endpoint without file."""
    response = client.post("/api/predict")
    
    # Should return 422 (validation error)
    assert response.status_code == 422


def test_multiple_predictions(client: TestClient):
    """Test multiple predictions."""
    # Make multiple predictions
    predictions = []
    
    for i in range(3):
        img_bytes = create_test_image(color=(i * 50, i * 50, i * 50))
        response = client.post(
            "/api/predict",
            files={"file": (f"test{i}.jpg", img_bytes, "image/jpeg")}
        )
        assert response.status_code == 200
        predictions.append(response.json())
    
    # All predictions should have unique IDs
    ids = [p["id"] for p in predictions]
    assert len(ids) == len(set(ids))


def test_predict_large_image(client: TestClient):
    """Test prediction with a large image."""
    # Create a large image
    img_bytes = create_test_image(size=(2000, 2000))
    
    response = client.post(
        "/api/predict",
        files={"file": ("large.jpg", img_bytes, "image/jpeg")}
    )
    
    # Should still work
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
