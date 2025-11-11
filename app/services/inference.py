"""Model inference service with TorchScript support."""
import os
import logging
from typing import Tuple, Optional
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from app.config import settings
from app.utils.tips import get_all_classes

logger = logging.getLogger(__name__)

# Global model instance
_model: Optional[torch.jit.ScriptModule] = None
_model_loaded: bool = False

# Class labels - load from classes.json or use defaults
CLASSES = [
    "apple_scab",
    "apple_black_rot",
    "apple_cedar_rust",
    "apple_healthy",
    "corn_cercospora_leaf_spot",
    "corn_common_rust",
    "corn_northern_leaf_blight",
    "corn_healthy",
    "grape_black_rot",
    "grape_esca",
    "grape_leaf_blight",
    "grape_healthy",
    "potato_early_blight",
    "potato_late_blight",
    "potato_healthy",
    "tomato_bacterial_spot",
    "tomato_early_blight",
    "tomato_late_blight",
    "tomato_leaf_mold",
    "tomato_septoria_leaf_spot",
    "tomato_spider_mites",
    "tomato_target_spot",
    "tomato_mosaic_virus",
    "tomato_yellow_leaf_curl",
    "tomato_healthy",
]

# ImageNet normalization
NORMALIZE_MEAN = [0.485, 0.456, 0.406]
NORMALIZE_STD = [0.229, 0.224, 0.225]


def get_transform() -> transforms.Compose:
    """
    Get image preprocessing transform.
    
    Returns:
        Composed transforms for model input
    """
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=NORMALIZE_MEAN, std=NORMALIZE_STD)
    ])


def load_model() -> bool:
    """
    Load TorchScript model from MODEL_PATH.
    
    Returns:
        True if model loaded successfully, False otherwise
    """
    global _model, _model_loaded
    
    if _model_loaded:
        return True
    
    model_path = settings.MODEL_PATH
    
    if not os.path.exists(model_path):
        logger.warning(f"Model file not found at {model_path}. Using stub inference.")
        _model_loaded = False
        return False
    
    try:
        logger.info(f"Loading TorchScript model from {model_path}")
        _model = torch.jit.load(model_path, map_location=torch.device("cpu"))
        _model.eval()
        _model_loaded = True
        logger.info("Model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        _model_loaded = False
        return False


def is_model_loaded() -> bool:
    """Check if model is loaded."""
    return _model_loaded


def get_model() -> Optional[torch.jit.ScriptModule]:
    """Get the loaded model instance."""
    return _model


def predict(image: Image.Image) -> Tuple[str, float]:
    """
    Run inference on an image.
    
    Args:
        image: PIL Image object
        
    Returns:
        Tuple of (predicted_class, confidence)
    """
    if not _model_loaded or _model is None:
        # Stub prediction for development
        logger.info("Using stub prediction (model not loaded)")
        return _get_stub_prediction(image)
    
    try:
        # Preprocess image
        transform = get_transform()
        input_tensor = transform(image).unsqueeze(0)  # Add batch dimension
        
        # Run inference
        with torch.no_grad():
            outputs = _model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
            
        # Get class label
        predicted_class = CLASSES[predicted_idx.item()] if predicted_idx.item() < len(CLASSES) else "unknown"
        confidence_value = confidence.item()
        
        logger.info(f"Prediction: {predicted_class} ({confidence_value:.4f})")
        return predicted_class, confidence_value
        
    except Exception as e:
        logger.error(f"Error during inference: {e}")
        return _get_stub_prediction(image)


def _get_stub_prediction(image: Image.Image) -> Tuple[str, float]:
    """
    Generate a deterministic stub prediction for development.
    
    Args:
        image: PIL Image object
        
    Returns:
        Tuple of (predicted_class, confidence)
    """
    # Use image dimensions as a seed for deterministic behavior
    width, height = image.size
    seed = (width + height) % len(CLASSES)
    
    predicted_class = CLASSES[seed]
    confidence = 0.42  # Answer to everything
    
    return predicted_class, confidence


def preprocess_for_gradcam(image: Image.Image) -> torch.Tensor:
    """
    Preprocess image for Grad-CAM visualization.
    
    Args:
        image: PIL Image object
        
    Returns:
        Preprocessed tensor with gradient enabled
    """
    transform = get_transform()
    input_tensor = transform(image).unsqueeze(0)
    input_tensor.requires_grad = True
    return input_tensor
