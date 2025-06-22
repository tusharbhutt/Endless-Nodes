from .endless_image_analysis import (
    EndlessNode_ImageNoveltyScorer,
    EndlessNode_ImageComplexityScorer,
)

NODE_CLASS_MAPPINGS = {
    "ImageNoveltyScorer": EndlessNode_ImageNoveltyScorer,
    "ImageComplexityScorer": EndlessNode_ImageComplexityScorer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageNoveltyScorer": "Novelty Score (CLIP)",
    "ImageComplexityScorer": "Complexity Score (Edge Density)",
}