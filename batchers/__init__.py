"""
EndlessSeaofStars Custom Nodes for ComfyUI
Batch processing nodes with specialized support for FLUX and SDXL models
"""

from .endless_batchers import (
    EndlessNode_SimpleBatchPrompts,
    EndlessNode_FluxBatchPrompts,
    EndlessNode_SDXLBatchPrompts,
    EndlessNode_BatchNegativePrompts,
    EndlessNode_PromptCounter,
)

# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "SimpleBatchPrompts": EndlessNode_SimpleBatchPrompts,
    "FluxBatchPrompts": EndlessNode_FluxBatchPrompts,
    "SDXLBatchPrompts": EndlessNode_SDXLBatchPrompts,
    "BatchNegativePrompts": EndlessNode_BatchNegativePrompts,
    "PromptCounter": EndlessNode_PromptCounter,
}

# Display names for ComfyUI interface
NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleBatchPrompts": "Simple Batch Prompts",
    "FluxBatchPrompts": "FLUX Batch Prompts",
    "SDXLBatchPrompts": "SDXL Batch Prompts", 
    "BatchNegativePrompts": "Batch Negative Prompts",
    "PromptCounter": "Prompt Counter",
}


