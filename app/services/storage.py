"""Storage service for managing uploaded images and generated heatmaps."""
import os
import uuid
from pathlib import Path
from typing import Tuple
from PIL import Image
from app.config import settings


def ensure_storage_dirs() -> None:
    """Ensure storage directories exist."""
    Path(settings.images_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.heatmaps_dir).mkdir(parents=True, exist_ok=True)


def save_uploaded_image(image: Image.Image) -> Tuple[str, str]:
    """
    Save uploaded image to storage.
    
    Args:
        image: PIL Image object
        
    Returns:
        Tuple of (file_path, uuid)
    """
    image_uuid = str(uuid.uuid4())
    filename = f"{image_uuid}.jpg"
    file_path = os.path.join(settings.images_dir, filename)
    
    # Convert to RGB if necessary
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Save image
    image.save(file_path, "JPEG", quality=95)
    
    return file_path, image_uuid


def save_heatmap(heatmap_image: Image.Image, image_uuid: str) -> str:
    """
    Save heatmap overlay image to storage.
    
    Args:
        heatmap_image: PIL Image object with heatmap overlay
        image_uuid: UUID of the original image
        
    Returns:
        Path to saved heatmap file
    """
    filename = f"{image_uuid}.jpg"
    file_path = os.path.join(settings.heatmaps_dir, filename)
    
    # Convert to RGB if necessary
    if heatmap_image.mode != "RGB":
        heatmap_image = heatmap_image.convert("RGB")
    
    # Save heatmap
    heatmap_image.save(file_path, "JPEG", quality=90)
    
    return file_path


def get_static_url(file_path: str) -> str:
    """
    Convert a file path to a static URL.
    
    Args:
        file_path: File path relative to or absolute
        
    Returns:
        Static URL path
    """
    # Normalize path separators to forward slashes
    normalized_path = file_path.replace("\\", "/")
    
    # Remove storage directory prefix if present
    if settings.STORAGE_DIR in normalized_path:
        # Extract the part after STORAGE_DIR
        parts = normalized_path.split(settings.STORAGE_DIR + "/", 1)
        if len(parts) > 1:
            relative_path = parts[1]
            return f"/static/{relative_path}"
    
    return f"/static/{normalized_path}"
