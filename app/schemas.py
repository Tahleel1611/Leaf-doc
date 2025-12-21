"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# Prediction Schemas
class PredictResponse(BaseModel):
    """Response schema for prediction endpoint."""
    
    id: str
    class_: str = Field(..., alias="class")
    confidence: float = Field(..., ge=0.0, le=1.0)
    tips: str
    heatmap_url: Optional[str] = None
    image_url: str
    created_at: datetime
    
    model_config = {"populate_by_name": True}


# Feedback Schemas
class FeedbackCreate(BaseModel):
    """Request schema for creating feedback."""
    
    id: str = Field(..., description="Prediction ID")
    correct: bool
    true_label: Optional[str] = None


class FeedbackResponse(BaseModel):
    """Embedded feedback in history items."""
    
    correct: bool
    true_label: Optional[str] = None


# History Schemas
class HistoryItem(BaseModel):
    """Response schema for history items."""
    
    id: str
    image_url: str
    pred_label: str
    pred_conf: float = Field(..., ge=0.0, le=1.0)
    heatmap_url: Optional[str] = None
    created_at: datetime
    feedback: Optional[FeedbackResponse] = None


class HistoryResponse(BaseModel):
    """Paginated history response."""
    
    items: list[HistoryItem]
    total: int
    page: int
    limit: int
    pages: int


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    app_name: str
    model_loaded: bool


# Statistics Schemas
class DiseaseStats(BaseModel):
    """Disease distribution statistics."""
    
    disease_name: str
    count: int
    avg_confidence: float = Field(..., ge=0.0, le=1.0)


class TimeSeriesData(BaseModel):
    """Time series data point."""
    
    date: str
    count: int


class StatisticsResponse(BaseModel):
    """Comprehensive statistics response."""
    
    total_predictions: int
    predictions_with_feedback: int
    correct_predictions: int
    accuracy_rate: Optional[float] = None
    avg_confidence: float
    disease_distribution: list[DiseaseStats]
    daily_predictions: list[TimeSeriesData]
    date_range_days: int
    start_date: datetime
    end_date: datetime
