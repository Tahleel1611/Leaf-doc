"""Tests for feedback endpoint."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Prediction


def create_test_prediction(db: Session) -> Prediction:
    """Create a test prediction."""
    prediction = Prediction(
        image_path="storage/images/test.jpg",
        pred_label="test_disease",
        pred_conf=0.95,
        heatmap_path="storage/heatmaps/test.jpg"
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def test_create_feedback_correct(client: TestClient, db: Session):
    """Test creating feedback marking prediction as correct."""
    # Create a prediction
    prediction = create_test_prediction(db)
    
    # Submit feedback
    response = client.post(
        "/api/feedback",
        json={
            "id": prediction.id,
            "correct": True
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == prediction.id
    assert data["feedback"] is not None
    assert data["feedback"]["correct"] is True
    assert data["feedback"]["true_label"] is None


def test_create_feedback_incorrect(client: TestClient, db: Session):
    """Test creating feedback marking prediction as incorrect."""
    # Create a prediction
    prediction = create_test_prediction(db)
    
    # Submit feedback
    response = client.post(
        "/api/feedback",
        json={
            "id": prediction.id,
            "correct": False,
            "true_label": "actual_disease"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == prediction.id
    assert data["feedback"] is not None
    assert data["feedback"]["correct"] is False
    assert data["feedback"]["true_label"] == "actual_disease"


def test_feedback_nonexistent_prediction(client: TestClient):
    """Test creating feedback for non-existent prediction."""
    response = client.post(
        "/api/feedback",
        json={
            "id": "nonexistent-id",
            "correct": True
        }
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_existing_feedback(client: TestClient, db: Session):
    """Test updating existing feedback."""
    # Create a prediction
    prediction = create_test_prediction(db)
    
    # Submit initial feedback
    response1 = client.post(
        "/api/feedback",
        json={
            "id": prediction.id,
            "correct": True
        }
    )
    assert response1.status_code == 200
    
    # Update feedback
    response2 = client.post(
        "/api/feedback",
        json={
            "id": prediction.id,
            "correct": False,
            "true_label": "corrected_disease"
        }
    )
    
    assert response2.status_code == 200
    data = response2.json()
    
    assert data["feedback"]["correct"] is False
    assert data["feedback"]["true_label"] == "corrected_disease"


def test_feedback_validation(client: TestClient, db: Session):
    """Test feedback validation."""
    prediction = create_test_prediction(db)
    
    # Missing required field
    response = client.post(
        "/api/feedback",
        json={"id": prediction.id}
    )
    assert response.status_code == 422
    
    # Invalid ID format (still should be handled)
    response = client.post(
        "/api/feedback",
        json={
            "id": "",
            "correct": True
        }
    )
    assert response.status_code in [404, 422]
