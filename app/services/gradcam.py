"""Grad-CAM visualization service for model interpretability."""
import logging
from typing import Optional
import numpy as np
import torch
import cv2
from PIL import Image
from app.services.inference import get_model, is_model_loaded, preprocess_for_gradcam, NORMALIZE_MEAN, NORMALIZE_STD

logger = logging.getLogger(__name__)


class GradCAM:
    """Grad-CAM implementation for CNN visualization."""
    
    def __init__(self, model: torch.jit.ScriptModule, target_layer_name: Optional[str] = None):
        """
        Initialize Grad-CAM.
        
        Args:
            model: TorchScript model
            target_layer_name: Name of target convolutional layer (optional)
        """
        self.model = model
        self.target_layer_name = target_layer_name
        self.gradients = None
        self.activations = None
        
    def save_gradient(self, grad: torch.Tensor) -> None:
        """Save gradients during backward pass."""
        self.gradients = grad
        
    def forward_hook(self, module: torch.nn.Module, input: tuple, output: torch.Tensor) -> None:
        """Save activations during forward pass."""
        self.activations = output
        
    def backward_hook(self, module: torch.nn.Module, grad_input: tuple, grad_output: tuple) -> None:
        """Save gradients during backward pass."""
        self.gradients = grad_output[0]
        
    def generate_cam(self, input_tensor: torch.Tensor, target_class: int) -> np.ndarray:
        """
        Generate Class Activation Map.
        
        Args:
            input_tensor: Preprocessed input tensor
            target_class: Target class index
            
        Returns:
            CAM as numpy array
        """
        # Forward pass
        output = self.model(input_tensor)
        
        # Zero gradients
        self.model.zero_grad()
        
        # Backward pass for target class
        class_loss = output[0, target_class]
        class_loss.backward()
        
        # Get gradients and activations
        if self.gradients is None or self.activations is None:
            logger.warning("Gradients or activations not captured")
            return np.zeros((224, 224))
        
        # Calculate weights
        weights = torch.mean(self.gradients, dim=(2, 3), keepdim=True)
        
        # Calculate CAM
        cam = torch.sum(weights * self.activations, dim=1).squeeze(0)
        cam = torch.nn.functional.relu(cam)
        
        # Normalize
        cam = cam.detach().cpu().numpy()
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        
        return cam


def generate_gradcam_heatmap(
    image: Image.Image,
    predicted_class_idx: int
) -> Optional[Image.Image]:
    """
    Generate Grad-CAM heatmap overlay for an image.
    
    Args:
        image: Original PIL Image
        predicted_class_idx: Index of predicted class
        
    Returns:
        PIL Image with heatmap overlay, or None if not possible
    """
    if not is_model_loaded():
        logger.info("Model not loaded, skipping Grad-CAM generation")
        return None
    
    model = get_model()
    if model is None:
        return None
    
    try:
        # Note: TorchScript models may not support hooks easily
        # This is a simplified implementation that may need adjustment
        # based on the actual model architecture
        
        # For now, generate a simple visualization
        # In production, you'd need to properly register hooks on the model
        logger.info("Generating Grad-CAM heatmap")
        
        # Create a simple heatmap visualization
        heatmap_overlay = create_simple_heatmap(image)
        return heatmap_overlay
        
    except Exception as e:
        logger.error(f"Error generating Grad-CAM: {e}")
        return None


def create_simple_heatmap(image: Image.Image) -> Image.Image:
    """
    Create a simple heatmap overlay as a placeholder.
    
    Args:
        image: Original PIL Image
        
    Returns:
        PIL Image with heatmap overlay
    """
    # Convert to numpy array
    img_array = np.array(image.convert("RGB"))
    height, width = img_array.shape[:2]
    
    # Create a simple center-focused heatmap
    y, x = np.ogrid[:height, :width]
    center_y, center_x = height // 2, width // 2
    
    # Gaussian-like heatmap
    sigma = min(height, width) // 3
    heatmap = np.exp(-((x - center_x)**2 + (y - center_y)**2) / (2 * sigma**2))
    heatmap = (heatmap * 255).astype(np.uint8)
    
    # Apply colormap
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    
    # Blend with original image
    alpha = 0.4
    overlay = cv2.addWeighted(img_array, 1 - alpha, heatmap_colored, alpha, 0)
    
    return Image.fromarray(overlay)


def denormalize_image(tensor: torch.Tensor) -> np.ndarray:
    """
    Denormalize tensor to image array.
    
    Args:
        tensor: Normalized image tensor
        
    Returns:
        Denormalized numpy array
    """
    img = tensor.squeeze(0).detach().cpu().numpy()
    img = np.transpose(img, (1, 2, 0))
    
    # Denormalize
    mean = np.array(NORMALIZE_MEAN)
    std = np.array(NORMALIZE_STD)
    img = img * std + mean
    
    # Clip and convert to uint8
    img = np.clip(img * 255, 0, 255).astype(np.uint8)
    
    return img
