"""Statistics endpoint for analytics and insights."""
import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Prediction, Feedback
from app.schemas import StatisticsResponse, DiseaseStats, TimeSeriesData

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics(
    days: int = Query(default=30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db)
) -> StatisticsResponse:
    """
    Get comprehensive statistics about predictions.
    
    Args:
        days: Number of days to analyze (default: 30)
        db: Database session
    
    Returns:
        Statistics response with analytics data
    """
    logger.info(f"Fetching statistics for last {days} days")
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Total predictions
    total_predictions = db.query(func.count(Prediction.id)).filter(
        Prediction.created_at >= start_date
    ).scalar() or 0
    
    # Predictions with feedback
    predictions_with_feedback = db.query(func.count(Feedback.id)).join(
        Prediction, Prediction.id == Feedback.prediction_id
    ).filter(
        Prediction.created_at >= start_date
    ).scalar() or 0
    
    # Correct predictions (from feedback)
    correct_predictions = db.query(func.count(Feedback.id)).join(
        Prediction, Prediction.id == Feedback.prediction_id
    ).filter(
        Prediction.created_at >= start_date,
        Feedback.correct == True
    ).scalar() or 0
    
    # Average confidence
    avg_confidence = db.query(func.avg(Prediction.pred_conf)).filter(
        Prediction.created_at >= start_date
    ).scalar() or 0.0
    
    # Disease distribution (top diseases)
    disease_distribution = db.query(
        Prediction.pred_label,
        func.count(Prediction.id).label('count'),
        func.avg(Prediction.pred_conf).label('avg_confidence')
    ).filter(
        Prediction.created_at >= start_date
    ).group_by(
        Prediction.pred_label
    ).order_by(
        desc('count')
    ).limit(10).all()
    
    # Daily prediction counts (time series)
    daily_counts = db.query(
        func.date(Prediction.created_at).label('date'),
        func.count(Prediction.id).label('count')
    ).filter(
        Prediction.created_at >= start_date
    ).group_by(
        func.date(Prediction.created_at)
    ).order_by(
        'date'
    ).all()
    
    # Calculate accuracy rate
    accuracy_rate = (
        (correct_predictions / predictions_with_feedback * 100)
        if predictions_with_feedback > 0 else None
    )
    
    # Format disease stats
    disease_stats = [
        DiseaseStats(
            disease_name=disease[0],
            count=disease[1],
            avg_confidence=round(disease[2], 4)
        )
        for disease in disease_distribution
    ]
    
    # Format time series data
    time_series = [
        TimeSeriesData(
            date=str(day[0]),
            count=day[1]
        )
        for day in daily_counts
    ]
    
    logger.info(
        f"Statistics calculated: {total_predictions} total, "
        f"{predictions_with_feedback} with feedback, "
        f"{correct_predictions} correct"
    )
    
    response = StatisticsResponse(
        total_predictions=total_predictions,
        predictions_with_feedback=predictions_with_feedback,
        correct_predictions=correct_predictions,
        accuracy_rate=accuracy_rate,
        avg_confidence=round(avg_confidence, 4),
        disease_distribution=disease_stats,
        daily_predictions=time_series,
        date_range_days=days,
        start_date=start_date,
        end_date=end_date
    )
    
    return response
