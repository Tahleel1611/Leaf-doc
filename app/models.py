"""SQLAlchemy database models."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


class Prediction(Base):
    """Prediction model storing inference results."""
    
    __tablename__ = "predictions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    image_path = Column(String(500), nullable=False)
    pred_label = Column(String(200), nullable=False)
    pred_conf = Column(Float, nullable=False)
    heatmap_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    feedback = relationship("Feedback", back_populates="prediction", uselist=False)
    
    def __repr__(self) -> str:
        return f"<Prediction(id={self.id}, label={self.pred_label}, conf={self.pred_conf})>"


class Feedback(Base):
    """Feedback model for user corrections."""
    
    __tablename__ = "feedback"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    prediction_id = Column(String(36), ForeignKey("predictions.id"), nullable=False, unique=True)
    correct = Column(Boolean, nullable=False)
    true_label = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    prediction = relationship("Prediction", back_populates="feedback")
    
    def __repr__(self) -> str:
        return f"<Feedback(id={self.id}, prediction_id={self.prediction_id}, correct={self.correct})>"
