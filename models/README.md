# LeafDoc Models

This directory contains the machine learning models used by the LeafDoc backend for plant disease classification.

## Model Architecture

The LeafDoc system uses a **MobileNetV3-Small** architecture, which provides an excellent balance between:
- **Accuracy**: High classification performance on plant disease detection
- **Efficiency**: Lightweight model suitable for deployment
- **Speed**: Fast inference times for real-time predictions

## Model Details

- **Architecture**: MobileNetV3-Small (pretrained on ImageNet)
- **Input Size**: 224x224x3 (RGB images)
- **Output Classes**: 25 plant disease classes
- **Format**: TorchScript (`.ts` file)
- **Framework**: PyTorch 2.0+

## Supported Disease Classes

The model can classify 25 different plant disease conditions across 4 plant types:

### Apple (4 classes)
- apple_scab
- apple_black_rot
- apple_cedar_rust
- apple_healthy

### Corn (4 classes)
- corn_cercospora_leaf_spot
- corn_common_rust
- corn_northern_leaf_blight
- corn_healthy

### Grape (4 classes)
- grape_black_rot
- grape_esca
- grape_leaf_blight
- grape_healthy

### Potato (3 classes)
- potato_early_blight
- potato_late_blight
- potato_healthy

### Tomato (10 classes)
- tomato_bacterial_spot
- tomato_early_blight
- tomato_late_blight
- tomato_leaf_mold
- tomato_septoria_leaf_spot
- tomato_spider_mites
- tomato_target_spot
- tomato_mosaic_virus
- tomato_yellow_leaf_curl
- tomato_healthy

## Generating the Model

To generate a new model file, use the provided `generate_model.py` script:

```bash
# From the models directory
python generate_model.py
```

This script will:
1. Load the MobileNetV3-Small architecture
2. Modify the classifier head for 25 classes
3. Export the model to TorchScript format
4. Save it as `leafdoc_mobilev3.ts`
5. Verify the exported model

### Requirements

```bash
torch>=2.0.0
torchvision>=0.15.0
```

### Output

After running the script, you'll have:
- **File**: `leafdoc_mobilev3.ts`
- **Size**: ~2-3 MB (compressed TorchScript model)
- **Parameters**: ~1.5M total parameters

## Using the Model

### Configuration

Set the model path in your `.env` file:

```bash
MODEL_PATH=models/leafdoc_mobilev3.ts
```

### API Usage

The model is automatically loaded by the FastAPI backend when the server starts. It will be used for:

1. **Inference**: Classifying uploaded plant leaf images
2. **Grad-CAM**: Generating visual explanations of predictions
3. **Confidence Scoring**: Providing prediction confidence values

### Without a Model

If no model file is present, the backend will:
- Use stub predictions for development
- Return fixed confidence scores (0.42)
- Skip Grad-CAM generation
- Still allow frontend development and testing

## Training Your Own Model

To train a custom model:

1. **Prepare Dataset**: Organize images in class folders
2. **Modify Architecture**: Update `generate_model.py` if needed
3. **Train**: Use PyTorch training loop with your dataset
4. **Export**: Use `torch.jit.trace()` to export to TorchScript
5. **Validate**: Test with sample images
6. **Deploy**: Place the `.ts` file in this directory

### Example Training Structure

```
data/
├── train/
│   ├── apple_scab/
│   ├── apple_black_rot/
│   └── ...
└── val/
    ├── apple_scab/
    ├── apple_black_rot/
    └── ...
```

## Model Performance

### Expected Metrics (with proper training)

- **Accuracy**: 92-95% on validation set
- **Inference Time**: ~50-100ms per image (CPU)
- **Inference Time**: ~10-20ms per image (GPU)
- **Model Size**: ~2-3 MB (TorchScript)

### Optimization Tips

1. **Quantization**: Reduce model size by 4x with minimal accuracy loss
2. **ONNX Export**: Convert to ONNX for broader deployment options
3. **Batch Inference**: Process multiple images simultaneously
4. **GPU Acceleration**: Use CUDA for faster predictions

## File Structure

```
models/
├── README.md                 # This file
├── generate_model.py         # Model generation script
├── leafdoc_mobilev3.ts      # TorchScript model (generated)
└── .gitkeep                  # Git placeholder
```

## Troubleshooting

### Model Won't Load

- Verify TorchScript format compatibility
- Check PyTorch version (>=2.0.0)
- Ensure file path is correct in `.env`
- Check file permissions

### Low Accuracy

- Ensure proper training with balanced dataset
- Verify image preprocessing matches training
- Check for data augmentation consistency
- Consider fine-tuning on your specific dataset

### Slow Inference

- Enable GPU if available (`CUDA_VISIBLE_DEVICES=0`)
- Use model quantization
- Batch multiple predictions
- Consider model optimization techniques

## References

- [MobileNetV3 Paper](https://arxiv.org/abs/1905.02244)
- [PyTorch TorchScript](https://pytorch.org/docs/stable/jit.html)
- [PlantVillage Dataset](https://www.kaggle.com/datasets/emmarex/plantdisease)

## License

The model architecture is based on MobileNetV3, which is available under the Apache 2.0 license. Your trained model weights are yours to use according to your project's license (MIT).
