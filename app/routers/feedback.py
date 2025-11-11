"""Feedback endpoint for user corrections."""
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Prediction, Feedback
from app.schemas import FeedbackCreate, HistoryItem, FeedbackResponse
from app.services.storage import get_static_url

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/feedback", response_model=HistoryItem)
def create_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db)
) -> HistoryItem:
    """
    Create feedback for a prediction.
    
    Args:
        feedback_data: Feedback creation data
        db: Database session
        
    Returns:
        Updated history item with feedback
        
    Raises:
        HTTPException: If prediction not found or feedback already exists
    """
    logger.info(f"Creating feedback for prediction: {feedback_data.id}")
    
    # Validate prediction exists
    prediction = db.query(Prediction).filter(Prediction.id == feedback_data.id).first()
    
    if not prediction:
        logger.warning(f"Prediction not found: {feedback_data.id}")
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    # Check if feedback already exists
    existing_feedback = db.query(Feedback).filter(Feedback.prediction_id == feedback_data.id).first()
    
    if existing_feedback:
        # Update existing feedback
        logger.info(f"Updating existing feedback: {existing_feedback.id}")
        existing_feedback.correct = feedback_data.correct
        existing_feedback.true_label = feedback_data.true_label
        existing_feedback.created_at = datetime.utcnow()
        feedback = existing_feedback
    else:
        # Create new feedback
        feedback = Feedback(
            prediction_id=feedback_data.id,
            correct=feedback_data.correct,
            true_label=feedback_data.true_label,
            created_at=datetime.utcnow()
        )
        db.add(feedback)
    
    db.commit()
    db.refresh(feedback)
    
    logger.info(f"Saved feedback: {feedback.id}")
    
    # Build response with updated feedback
    feedback_response = FeedbackResponse(
        correct=feedback.correct,
        true_label=feedback.true_label
    )
    
    item = HistoryItem(
        id=prediction.id,
        image_url=get_static_url(prediction.image_path),
        pred_label=prediction.pred_label,
        pred_conf=prediction.pred_conf,
        heatmap_url=get_static_url(prediction.heatmap_path) if prediction.heatmap_path else None,
        created_at=prediction.created_at,
        feedback=feedback_response
    )
    
    return item
