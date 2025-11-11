"""Seed script to initialize database with sample data for development."""
import os
import sys
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db import SessionLocal, init_db
from app.models import Prediction, Feedback
from app.services.storage import ensure_storage_dirs
from app.services.inference import CLASSES


def seed_database(num_predictions: int = 10):
    """
    Seed the database with sample predictions.
    
    Args:
        num_predictions: Number of predictions to create
    """
    print("Initializing database...")
    init_db()
    
    print("Ensuring storage directories exist...")
    ensure_storage_dirs()
    
    print(f"Creating {num_predictions} sample predictions...")
    db = SessionLocal()
    
    try:
        # Clear existing data (optional)
        # db.query(Feedback).delete()
        # db.query(Prediction).delete()
        
        created_predictions = []
        
        for i in range(num_predictions):
            # Random disease class
            disease_class = random.choice(CLASSES)
            confidence = random.uniform(0.7, 0.99)
            
            # Create prediction with timestamp spread over last 30 days
            days_ago = random.randint(0, 30)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            prediction = Prediction(
                image_path=f"storage/images/sample_{i}.jpg",
                pred_label=disease_class,
                pred_conf=confidence,
                heatmap_path=f"storage/heatmaps/sample_{i}.jpg" if random.random() > 0.3 else None,
                created_at=created_at
            )
            
            db.add(prediction)
            created_predictions.append(prediction)
        
        db.commit()
        
        print(f"Created {len(created_predictions)} predictions")
        
        # Add feedback to some predictions
        num_feedback = num_predictions // 3
        print(f"Adding feedback to {num_feedback} predictions...")
        
        sample_predictions = random.sample(created_predictions, num_feedback)
        
        for prediction in sample_predictions:
            is_correct = random.random() > 0.3
            
            feedback = Feedback(
                prediction_id=prediction.id,
                correct=is_correct,
                true_label=None if is_correct else random.choice(CLASSES),
                created_at=prediction.created_at + timedelta(hours=random.randint(1, 24))
            )
            
            db.add(feedback)
        
        db.commit()
        print(f"Added {num_feedback} feedback entries")
        
        print("\n✅ Database seeded successfully!")
        print(f"Total predictions: {db.query(Prediction).count()}")
        print(f"Total feedback: {db.query(Feedback).count()}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    seed_database(num)
