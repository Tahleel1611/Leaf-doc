"""Plant disease classification tips and recommendations."""
from typing import Dict

# Disease-specific tips
DISEASE_TIPS: Dict[str, str] = {
    "apple_scab": "Remove infected leaves and apply fungicide. Ensure good air circulation and avoid overhead watering.",
    "apple_black_rot": "Prune infected branches, remove mummified fruits, and apply fungicide during early spring.",
    "apple_cedar_rust": "Remove nearby cedar trees if possible. Apply fungicide preventively in spring.",
    "apple_healthy": "Continue regular care: proper watering, pruning, and monitoring for early disease signs.",
    
    "corn_cercospora_leaf_spot": "Use resistant varieties, rotate crops, and apply fungicide if severe.",
    "corn_common_rust": "Plant resistant hybrids, ensure proper spacing for air flow, and monitor regularly.",
    "corn_northern_leaf_blight": "Rotate crops, remove crop debris, and use resistant varieties.",
    "corn_healthy": "Maintain proper nutrition, adequate spacing, and regular monitoring.",
    
    "grape_black_rot": "Remove infected fruit and leaves. Apply fungicide starting at bloom.",
    "grape_esca": "Prune infected wood, avoid stress, and improve soil drainage.",
    "grape_leaf_blight": "Remove infected leaves, improve air circulation, and apply copper fungicide.",
    "grape_healthy": "Proper pruning, good air circulation, and balanced nutrition are key.",
    
    "potato_early_blight": "Use certified disease-free seed, rotate crops, and apply fungicide.",
    "potato_late_blight": "Remove infected plants immediately. Use resistant varieties and fungicide.",
    "potato_healthy": "Maintain good drainage, proper spacing, and monitor for disease signs.",
    
    "tomato_bacterial_spot": "Use disease-free seeds, avoid overhead watering, and apply copper spray.",
    "tomato_early_blight": "Mulch plants, stake for air flow, and remove lower infected leaves.",
    "tomato_late_blight": "Remove infected plants, improve air circulation, and use fungicide.",
    "tomato_leaf_mold": "Reduce humidity, improve ventilation, and remove infected leaves.",
    "tomato_septoria_leaf_spot": "Mulch soil, avoid wetting foliage, and remove infected leaves.",
    "tomato_spider_mites": "Spray with water, use insecticidal soap, and introduce predatory mites.",
    "tomato_target_spot": "Remove infected leaves, improve air flow, and apply fungicide.",
    "tomato_mosaic_virus": "Remove infected plants immediately. Disinfect tools and wash hands.",
    "tomato_yellow_leaf_curl": "Control whiteflies, remove infected plants, and use resistant varieties.",
    "tomato_healthy": "Regular watering, proper spacing, mulching, and consistent monitoring.",
    
    # Generic fallbacks
    "healthy": "Your plant looks healthy! Continue with regular care and monitoring.",
    "diseased": "Disease detected. Remove affected parts, improve conditions, and consider treatment.",
    "unknown": "Unable to identify specific condition. Consult a plant disease expert for advice.",
}


def get_tips(label: str) -> str:
    """
    Get actionable care tips for a given plant disease label.
    
    Args:
        label: Disease classification label
        
    Returns:
        Actionable tip string
    """
    # Normalize label to lowercase and replace spaces with underscores
    normalized_label = label.lower().replace(" ", "_").replace("-", "_")
    
    # Direct match
    if normalized_label in DISEASE_TIPS:
        return DISEASE_TIPS[normalized_label]
    
    # Check if it contains 'healthy'
    if "healthy" in normalized_label:
        return DISEASE_TIPS["healthy"]
    
    # Check for partial matches
    for key, tip in DISEASE_TIPS.items():
        if key in normalized_label or normalized_label in key:
            return tip
    
    # Default fallback
    return DISEASE_TIPS["unknown"]


def get_all_classes() -> list[str]:
    """
    Get list of all known disease classes.
    
    Returns:
        List of disease class names
    """
    return list(DISEASE_TIPS.keys())
