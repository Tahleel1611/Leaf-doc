#!/usr/bin/env python3
"""
Model Generator for LeafDoc Plant Disease Classification

This script creates a MobileNetV3-based model for classifying 25 plant disease classes
and exports it to TorchScript format for use with the LeafDoc backend.

Usage:
    python generate_model.py

Requirements:
    - torch>=2.0.0
    - torchvision>=0.15.0
"""

import torch
import torch.nn as nn
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights
import json
from pathlib import Path


class LeafDocClassifier(nn.Module):
    """MobileNetV3-based plant disease classifier."""
    
    def __init__(self, num_classes=25):
        super().__init__()
        # Load pretrained MobileNetV3 Small model
        self.backbone = mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.DEFAULT)
        
        # Replace the classifier head with our custom one
        in_features = self.backbone.classifier[3].in_features
        self.backbone.classifier[3] = nn.Linear(in_features, num_classes)
        
    def forward(self, x):
        return self.backbone(x)


def create_model(num_classes=25):
    """Create and initialize the model."""
    model = LeafDocClassifier(num_classes=num_classes)
    model.eval()  # Set to evaluation mode
    return model


def export_to_torchscript(model, output_path):
    """Export model to TorchScript format."""
    # Create example input
    example_input = torch.rand(1, 3, 224, 224)
    
    # Trace the model
    traced_model = torch.jit.trace(model, example_input)
    
    # Save the traced model
    traced_model.save(str(output_path))
    print(f"Model exported to: {output_path}")
    print(f"File size: {output_path.stat().st_size / (1024*1024):.2f} MB")


def main():
    # Load class information
    classes_file = Path(__file__).parent.parent / "classes.json"
    
    if classes_file.exists():
        with open(classes_file, 'r') as f:
            classes_data = json.load(f)
            num_classes = len(classes_data['classes'])
            print(f"Found {num_classes} disease classes")
    else:
        num_classes = 25
        print(f"Warning: classes.json not found. Using default {num_classes} classes")
    
    # Create model
    print("\nCreating MobileNetV3 model...")
    model = create_model(num_classes=num_classes)
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    
    # Export to TorchScript
    output_path = Path(__file__).parent / "leafdoc_mobilev3.ts"
    print(f"\nExporting to TorchScript...")
    export_to_torchscript(model, output_path)
    
    # Verify the exported model
    print("\nVerifying exported model...")
    loaded_model = torch.jit.load(str(output_path))
    test_input = torch.rand(1, 3, 224, 224)
    with torch.no_grad():
        output = loaded_model(test_input)
    print(f"Output shape: {output.shape}")
    print(f"Output classes: {output.shape[1]}")
    
    print("\n✅ Model generation complete!")
    print(f"\nTo use this model:")
    print(f"1. Set MODEL_PATH=models/leafdoc_mobilev3.ts in your .env file")
    print(f"2. Start the FastAPI server")
    print(f"3. The model will be loaded automatically")


if __name__ == "__main__":
    main()
