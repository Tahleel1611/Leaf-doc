"""Tests for history endpoint."""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models import Prediction, Feedback


def create_test_prediction(db: Session, label: str = "test_disease", conf: float = 0.95) -> Prediction:
    """Create a test prediction in the database."""
    prediction = Prediction(
        image_path="storage/images/test.jpg",
        pred_label=label,
        pred_conf=conf,
        heatmap_path="storage/heatmaps/test.jpg",
        created_at=datetime.utcnow()
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def test_get_history_empty(client: TestClient):
    """Test history endpoint with no predictions."""
    response = client.get("/api/history")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["pages"] >= 0


def test_get_history_with_predictions(client: TestClient, db: Session):
    """Test history endpoint with predictions."""
    # Create test predictions
    for i in range(5):
        create_test_prediction(db, label=f"disease_{i}", conf=0.8 + i * 0.02)
    
    response = client.get("/api/history")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 5
    assert data["total"] == 5
    assert data["page"] == 1


def test_history_pagination(client: TestClient, db: Session):
    """Test history pagination."""
    # Create 25 test predictions
    for i in range(25):
        create_test_prediction(db, label=f"disease_{i}")
    
    # Get first page (limit 20)
    response = client.get("/api/history?page=1&limit=20")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 20
    assert data["total"] == 25
    assert data["page"] == 1
    assert data["pages"] == 2
    
    # Get second page
    response = client.get("/api/history?page=2&limit=20")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 5
    assert data["page"] == 2


def test_history_filter_by_label(client: TestClient, db: Session):
    """Test filtering history by label."""
    create_test_prediction(db, label="apple_scab")
    create_test_prediction(db, label="tomato_blight")
    create_test_prediction(db, label="apple_scab")
    
    response = client.get("/api/history?label=apple")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["total"] == 2
    for item in data["items"]:
        assert "apple" in item["pred_label"].lower()


def test_history_with_feedback(client: TestClient, db: Session):
    """Test history with feedback."""
    # Create prediction
    prediction = create_test_prediction(db)
    
    # Add feedback
    feedback = Feedback(
        prediction_id=prediction.id,
        correct=True,
        true_label=None
    )
    db.add(feedback)
    db.commit()
    
    # Get history
    response = client.get("/api/history")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 1
    assert data["items"][0]["feedback"] is not None
    assert data["items"][0]["feedback"]["correct"] is True


def test_history_filter_by_correct(client: TestClient, db: Session):
    """Test filtering by feedback correctness."""
    # Create predictions with different feedback
    pred1 = create_test_prediction(db, label="correct_disease")
    feedback1 = Feedback(prediction_id=pred1.id, correct=True)
    db.add(feedback1)
    
    pred2 = create_test_prediction(db, label="incorrect_disease")
    feedback2 = Feedback(prediction_id=pred2.id, correct=False, true_label="actual_disease")
    db.add(feedback2)
    
    create_test_prediction(db, label="no_feedback")
    
    db.commit()
    
    # Filter for correct predictions
    response = client.get("/api/history?correct=true")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["feedback"]["correct"] is True
    
    # Filter for incorrect predictions
    response = client.get("/api/history?correct=false")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["feedback"]["correct"] is False
