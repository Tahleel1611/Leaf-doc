"""Prediction endpoint for plant disease detection."""
import logging
from datetime import datetime
from io import BytesIO
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from PIL import Image

from app.deps import get_db
from app.models import Prediction
from app.schemas import PredictResponse
from app.services import inference, storage, gradcam
from app.utils.tips import get_tips

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
async def predict_disease(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> PredictResponse:
    """
    Predict plant disease from uploaded image.
    
    Args:
        file: Uploaded image file
        db: Database session
        
    Returns:
        Prediction response with classification results
        
    Raises:
        HTTPException: If file processing fails
    """
    logger.info(f"Received prediction request for file: {file.filename}")
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        
        # Save original image
        image_path, image_uuid = storage.save_uploaded_image(image)
        logger.info(f"Saved image to {image_path}")
        
        # Run inference
        predicted_class, confidence = inference.predict(image)
        logger.info(f"Prediction: {predicted_class} with confidence {confidence:.4f}")
        
        # Generate Grad-CAM heatmap if model is loaded
        heatmap_path = None
        if inference.is_model_loaded():
            try:
                # Get predicted class index
                predicted_idx = inference.CLASSES.index(predicted_class) if predicted_class in inference.CLASSES else 0
                
                # Generate heatmap
                heatmap_image = gradcam.generate_gradcam_heatmap(image, predicted_idx)
                
                if heatmap_image:
                    heatmap_path = storage.save_heatmap(heatmap_image, image_uuid)
                    logger.info(f"Saved heatmap to {heatmap_path}")
            except Exception as e:
                logger.error(f"Error generating Grad-CAM: {e}")
        
        # Get tips for the predicted disease
        tips = get_tips(predicted_class)
        
        # Create prediction record
        prediction = Prediction(
            id=image_uuid,
            image_path=image_path,
            pred_label=predicted_class,
            pred_conf=confidence,
            heatmap_path=heatmap_path,
            created_at=datetime.utcnow()
        )
        
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        logger.info(f"Saved prediction to database with ID: {prediction.id}")
        
        # Build response
        response = PredictResponse(
            id=prediction.id,
            class_=predicted_class,
            confidence=confidence,
            tips=tips,
            heatmap_url=storage.get_static_url(heatmap_path) if heatmap_path else None,
            image_url=storage.get_static_url(image_path),
            created_at=prediction.created_at
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing prediction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
