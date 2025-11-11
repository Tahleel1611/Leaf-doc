"""History endpoint for viewing past predictions."""
import logging
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.deps import get_db
from app.models import Prediction, Feedback
from app.schemas import HistoryResponse, HistoryItem, FeedbackResponse
from app.services.storage import get_static_url

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/history", response_model=HistoryResponse)
def get_history(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    label: Optional[str] = Query(None, description="Filter by predicted label"),
    correct: Optional[bool] = Query(None, description="Filter by feedback correctness"),
    from_date: Optional[datetime] = Query(None, alias="from", description="Filter from date"),
    to_date: Optional[datetime] = Query(None, alias="to", description="Filter to date"),
    db: Session = Depends(get_db)
) -> HistoryResponse:
    """
    Get paginated prediction history with optional filters.
    
    Args:
        page: Page number (1-indexed)
        limit: Number of items per page
        label: Filter by predicted label
        correct: Filter by feedback correctness
        from_date: Filter predictions from this date
        to_date: Filter predictions to this date
        db: Database session
        
    Returns:
        Paginated history response
    """
    logger.info(f"Fetching history: page={page}, limit={limit}, label={label}, correct={correct}")
    
    # Build query with filters
    query = db.query(Prediction).outerjoin(Feedback)
    
    # Apply filters
    filters = []
    
    if label:
        filters.append(Prediction.pred_label.ilike(f"%{label}%"))
    
    if correct is not None:
        filters.append(Feedback.correct == correct)
    
    if from_date:
        filters.append(Prediction.created_at >= from_date)
    
    if to_date:
        filters.append(Prediction.created_at <= to_date)
    
    if filters:
        query = query.filter(and_(*filters))
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    offset = (page - 1) * limit
    pages = (total + limit - 1) // limit if total > 0 else 1
    
    # Get paginated results
    predictions = query.order_by(Prediction.created_at.desc()).offset(offset).limit(limit).all()
    
    # Build response items
    items = []
    for prediction in predictions:
        feedback_data = None
        if prediction.feedback:
            feedback_data = FeedbackResponse(
                correct=prediction.feedback.correct,
                true_label=prediction.feedback.true_label
            )
        
        item = HistoryItem(
            id=prediction.id,
            image_url=get_static_url(prediction.image_path),
            pred_label=prediction.pred_label,
            pred_conf=prediction.pred_conf,
            heatmap_url=get_static_url(prediction.heatmap_path) if prediction.heatmap_path else None,
            created_at=prediction.created_at,
            feedback=feedback_data
        )
        items.append(item)
    
    logger.info(f"Returning {len(items)} items out of {total} total")
    
    return HistoryResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )
