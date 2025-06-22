import os
import json
import re
from datetime import datetime
from PIL import Image, PngImagePlugin
import numpy as np
import torch
import folder_paths
from PIL.PngImagePlugin import PngInfo
import platform

class EndlessNode_SimpleBatchPrompts:
    """
    Takes multiple prompts (one per line) and creates batched conditioning tensors
    Automatically detects number of prompts and creates appropriate batch size
    Handles batch size mismatches by cycling through prompts if needed
    """
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "prompts": ("STRING", {"multiline": True, "default": "beautiful landscape\nmountain sunset\nocean waves\nfield of sunflowers"}),
                    "clip": ("CLIP", ),
                    "print_output": ("BOOLEAN", {"default": True}),
                    "max_batch_size": ("INT", {"default": 0, "min": 0, "max": 64, "step": 1}),
                    }}
    
    RETURN_TYPES = ("CONDITIONING", "STRING", "INT")
    RETURN_NAMES = ("CONDITIONING", "PROMPT_LIST", "PROMPT_COUNT")
    FUNCTION = "batch_encode"
    CATEGORY = "Endless 🌊✨/BatchProcessing"

    def batch_encode(self, prompts, clip, print_output, max_batch_size=0):
        # Split prompts by lines and clean them
        prompt_lines = [line.strip() for line in prompts.split('\n') if line.strip()]
        prompt_count = len(prompt_lines)
        
        if not prompt_lines:
            raise ValueError("No valid prompts found. Please enter at least one prompt.")
        
        # Handle batch size logic
        if max_batch_size > 0 and max_batch_size < len(prompt_lines):
            # Limit to max_batch_size
            prompt_lines = prompt_lines[:max_batch_size]
            if print_output:
                print(f"Limited to first {max_batch_size} prompts due to max_batch_size setting")
        elif max_batch_size > len(prompt_lines) and max_batch_size > 0:
            # Cycle through prompts to fill batch
            original_count = len(prompt_lines)
            while len(prompt_lines) < max_batch_size:
                prompt_lines.extend(prompt_lines[:min(original_count, max_batch_size - len(prompt_lines))])
            if print_output:
                print(f"Cycling through {original_count} prompts to fill batch size of {max_batch_size}")
        
        if print_output:
            print(f"Processing {len(prompt_lines)} prompts in batch:")
            for i, prompt in enumerate(prompt_lines):
                print(f"  {i+1}: {prompt}")
        
        # Encode each prompt separately with error handling
        cond_tensors = []
        pooled_tensors = []
        
        for i, prompt in enumerate(prompt_lines):
            try:
                tokens = clip.tokenize(prompt)
                cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
                cond_tensors.append(cond)
                pooled_tensors.append(pooled)
            except Exception as e:
                print(f"Error encoding prompt {i+1} '{prompt}': {e}")
                # Use a fallback empty prompt
                try:
                    tokens = clip.tokenize("")
                    cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
                    cond_tensors.append(cond)
                    pooled_tensors.append(pooled)
                    print(f"  Using empty fallback for prompt {i+1}")
                except Exception as fallback_error:
                    raise ValueError(f"Failed to encode prompt {i+1} and fallback failed: {fallback_error}")
        
        # Batch the conditioning tensors properly
        try:
            # Stack the conditioning tensors along batch dimension
            batched_cond = torch.cat(cond_tensors, dim=0)
            batched_pooled = torch.cat(pooled_tensors, dim=0)
            
            if print_output:
                print(f"Created batched conditioning: {batched_cond.shape}")
                print(f"Created batched pooled: {batched_pooled.shape}")
            
            # Return as proper conditioning format
            conditioning = [[batched_cond, {"pooled_output": batched_pooled}]]
            
        except Exception as e:
            print(f"Error creating batched conditioning: {e}")
            print("Falling back to list format...")
            # Fallback to list format if batching fails
            conditioning = []
            for i in range(len(cond_tensors)):
                conditioning.append([cond_tensors[i], {"pooled_output": pooled_tensors[i]}])
        
        # Create the prompt list string for filename use
        prompt_list_str = "|".join(prompt_lines)  # Join with | separator
        
        return (conditioning, prompt_list_str, prompt_count)


class EndlessNode_FluxBatchPrompts:
    """
    Specialized batch prompt encoder for FLUX models
    Handles FLUX-specific conditioning requirements including guidance and T5 text encoding
    """
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "prompts": ("STRING", {"multiline": True, "default": "beautiful landscape\nmountain sunset\nocean waves\nfield of sunflowers"}),
                    "clip": ("CLIP", ),
                    "guidance": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 100.0, "step": 0.1}),
                    "print_output": ("BOOLEAN", {"default": True}),
                    "max_batch_size": ("INT", {"default": 0, "min": 0, "max": 64, "step": 1}),
                    }}
    
    RETURN_TYPES = ("CONDITIONING", "STRING", "INT")
    RETURN_NAMES = ("CONDITIONING", "PROMPT_LIST", "PROMPT_COUNT")
    FUNCTION = "batch_encode_flux"
    CATEGORY = "Endless 🌊✨/BatchProcessing"

    def batch_encode_flux(self, prompts, clip, guidance, print_output, max_batch_size=0):
        # Split prompts by lines and clean them
        prompt_lines = [line.strip() for line in prompts.split('\n') if line.strip()]
        prompt_count = len(prompt_lines)
        
        if not prompt_lines:
            raise ValueError("No valid prompts found. Please enter at least one prompt.")
        
        # Handle batch size logic
        if max_batch_size > 0 and max_batch_size < len(prompt_lines):
            prompt_lines = prompt_lines[:max_batch_size]
            if print_output:
                print(f"Limited to first {max_batch_size} prompts due to max_batch_size setting")
        elif max_batch_size > len(prompt_lines) and max_batch_size > 0:
            original_count = len(prompt_lines)
            while len(prompt_lines) < max_batch_size:
                prompt_lines.extend(prompt_lines[:min(original_count, max_batch_size - len(prompt_lines))])
            if print_output:
                print(f"Cycling through {original_count} prompts to fill batch size of {max_batch_size}")
        
        if print_output:
            print(f"Processing {len(prompt_lines)} FLUX prompts in batch:")
            for i, prompt in enumerate(prompt_lines):
                print(f"  {i+1}: {prompt}")
        
        # Encode each prompt with FLUX-specific conditioning
        cond_tensors = []
        pooled_tensors = []
        
        for i, prompt in enumerate(prompt_lines):
            try:
                tokens = clip.tokenize(prompt)
                cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
                cond_tensors.append(cond)
                pooled_tensors.append(pooled)
            except Exception as e:
                print(f"Error encoding FLUX prompt {i+1} '{prompt}': {e}")
                # Use a fallback empty prompt
                try:
                    tokens = clip.tokenize("")
                    cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
                    cond_tensors.append(cond)
                    pooled_tensors.append(pooled)
                    print(f"  Using empty fallback for FLUX prompt {i+1}")
                except Exception as fallback_error:
                    raise ValueError(f"Failed to encode FLUX prompt {i+1} and fallback failed: {fallback_error}")
        
        # Batch the conditioning tensors properly for FLUX
        try:
            # Stack the conditioning tensors along batch dimension
            batched_cond = torch.cat(cond_tensors, dim=0)
            batched_pooled = torch.cat(pooled_tensors, dim=0)
            
            if print_output:
                print(f"Created FLUX batched conditioning: {batched_cond.shape}")
                print(f"Created FLUX batched pooled: {batched_pooled.shape}")
            
            # FLUX-specific conditioning with guidance
            conditioning = [[batched_cond, {
                "pooled_output": batched_pooled,
                "guidance": guidance,
                "guidance_scale": guidance  # Some FLUX implementations use this key
            }]]
            
        except Exception as e:
            print(f"Error creating FLUX batched conditioning: {e}")
            print("Falling back to list format...")
            # Fallback to list format if batching fails
            conditioning = []
            for i in range(len(cond_tensors)):
                flux_conditioning = [cond_tensors[i], {
                    "pooled_output": pooled_tensors[i],
                    "guidance": guidance,
                    "guidance_scale": guidance
                }]
                conditioning.append(flux_conditioning)
        
        prompt_list_str = "|".join(prompt_lines)
        return (conditioning, prompt_list_str, prompt_count)


class EndlessNode_SDXLBatchPrompts:
    """
    Specialized batch prompt encoder for SDXL models
    Handles dual text encoders and SDXL-specific conditioning requirements
    """
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "prompts": ("STRING", {"multiline": True, "default": "beautiful landscape\nmountain sunset\nocean waves"}),
                    "clip": ("CLIP", ),
                    "print_output": ("BOOLEAN", {"default": True}),
                    "max_batch_size": ("INT", {"default": 0, "min": 0, "max": 64, "step": 1}),
                    }}
    
    RETURN_TYPES = ("CONDITIONING", "STRING", "INT")
    RETURN_NAMES = ("CONDITIONING", "PROMPT_LIST", "PROMPT_COUNT")
    FUNCTION = "batch_encode_sdxl"
    CATEGORY = "Endless 🌊✨/BatchProcessing"

    def batch_encode_sdxl(self, prompts, clip, print_output, max_batch_size=0):
        # Split prompts by lines and clean them
        prompt_lines = [line.strip() for line in prompts.split('\n') if line.strip()]
        prompt_count = len(prompt_lines)
        
        if not prompt_lines:
            raise ValueError("No valid prompts found. Please enter at least one prompt.")
        
        # Handle batch size logic
        if max_batch_size > 0 and max_batch_size < len(prompt_lines):
            prompt_lines = prompt_lines[:max_batch_size]
            if print_output:
                print(f"Limited to first {max_batch_size} prompts due to max_batch_size setting")
        elif max_batch_size > len(prompt_lines) and max_batch_size > 0:
            original_count = len(prompt_lines)
            while len(prompt_lines) < max_batch_size:
                prompt_lines.extend(prompt_lines[:min(original_count, max_batch_size - len(prompt_lines))])
            if print_output:
                print(f"Cycling through {original_count} prompts to fill batch size of {max_batch_size}")
        
        if print_output:
            print(f"Processing {len(prompt_lines)} SDXL prompts in batch:")
            for i, prompt in enumerate(prompt_lines):
                print(f"  {i+1}: {prompt}")
        
        # Encode each prompt with SDXL-specific conditioning
        cond_tensors = []
        pooled_tensors = []
        
        for i, prompt in enumerate(prompt_lines):
            try:
                tokens = clip.tokenize(prompt)
                cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
                cond_tensors.append(cond)
                pooled_tensors.append(pooled)
            except Exception as e:
                print(f"Error encoding SDXL prompt {i+1} '{prompt}': {e}")
                # Use a fallback empty prompt
                try:
                    tokens = clip.tokenize("")
                    cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
                    cond_tensors.append(cond)
                    pooled_tensors.append(pooled)
                    print(f"  Using empty fallback for SDXL prompt {i+1}")
                except Exception as fallback_error:
                    raise ValueError(f"Failed to encode SDXL prompt {i+1} and fallback failed: {fallback_error}")
        
        # Batch the conditioning tensors properly for SDXL
        try:
            # Stack the conditioning tensors along batch dimension
            batched_cond = torch.cat(cond_tensors, dim=0)
            batched_pooled = torch.cat(pooled_tensors, dim=0)
            
            if print_output:
                print(f"Created SDXL batched conditioning: {batched_cond.shape}")
                print(f"Created SDXL batched pooled: {batched_pooled.shape}")
            
            # SDXL-specific conditioning - simplified without size parameters
            conditioning = [[batched_cond, {"pooled_output": batched_pooled}]]
            
        except Exception as e:
            print(f"Error creating SDXL batched conditioning: {e}")
            print("Falling back to list format...")
            # Fallback to list format if batching fails
            conditioning = []
            for i in range(len(cond_tensors)):
                sdxl_conditioning = [cond_tensors[i], {"pooled_output": pooled_tensors[i]}]
                conditioning.append(sdxl_conditioning)
        
        prompt_list_str = "|".join(prompt_lines)
        return (conditioning, prompt_list_str, prompt_count)


class EndlessNode_BatchNegativePrompts:
    """
    Handles batch negative prompts - simplified version without unnecessary parameters
    """
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "negative_prompts": ("STRING", {"multiline": True, "default": "blurry, low quality\nartifacts, distorted\nnoise, bad anatomy"}),
                    "clip": ("CLIP", ),
                    "print_output": ("BOOLEAN", {"default": True}),
                    "max_batch_size": ("INT", {"default": 0, "min": 0, "max": 64, "step": 1}),
                    }}
    
    RETURN_TYPES = ("CONDITIONING", "STRING")
    RETURN_NAMES = ("NEGATIVE_CONDITIONING", "NEGATIVE_PROMPT_LIST")
    FUNCTION = "batch_encode_negative"
    CATEGORY = "Endless 🌊✨/BatchProcessing"

    def batch_encode_negative(self, negative_prompts, clip, print_output, max_batch_size=0):
        # Split prompts by lines and clean them
        prompt_lines = [line.strip() for line in negative_prompts.split('\n') if line.strip()]
        
        if not prompt_lines:
            # Use empty negative prompt if none provided
            prompt_lines = [""]
        
        # Handle batch size logic
        if max_batch_size > 0 and max_batch_size < len(prompt_lines):
            prompt_lines = prompt_lines[:max_batch_size]
            if print_output:
                print(f"Limited to first {max_batch_size} negative prompts due to max_batch_size setting")
        elif max_batch_size > len(prompt_lines) and max_batch_size > 0:
            original_count = len(prompt_lines)
            while len(prompt_lines) < max_batch_size:
                prompt_lines.extend(prompt_lines[:min(original_count, max_batch_size - len(prompt_lines))])
            if print_output:
                print(f"Cycling through {original_count} negative prompts to fill batch size of {max_batch_size}")
        
        if print_output:
            print(f"Processing {len(prompt_lines)} negative prompts in batch:")
            for i, prompt in enumerate(prompt_lines):
                print(f"  {i+1}: {prompt if prompt else '(empty)'}")
        
        # Encode each negative prompt
        cond_tensors = []
        pooled_tensors = []
        
        for i, prompt in enumerate(prompt_lines):
            try:
                tokens = clip.tokenize(prompt)
                cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
                cond_tensors.append(cond)
                pooled_tensors.append(pooled)
            except Exception as e:
                print(f"Error encoding negative prompt {i+1} '{prompt}': {e}")
                # Use fallback empty prompt
                try:
                    tokens = clip.tokenize("")
                    cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
                    cond_tensors.append(cond)
                    pooled_tensors.append(pooled)
                    print(f"  Using empty fallback for negative prompt {i+1}")
                except Exception as fallback_error:
                    raise ValueError(f"Failed to encode negative prompt {i+1} and fallback failed: {fallback_error}")
        
        # Batch the conditioning tensors - simplified without model-specific parameters
        try:
            # Stack the conditioning tensors along batch dimension
            batched_cond = torch.cat(cond_tensors, dim=0)
            batched_pooled = torch.cat(pooled_tensors, dim=0)
            
            if print_output:
                print(f"Created negative batched conditioning: {batched_cond.shape}")
                print(f"Created negative batched pooled: {batched_pooled.shape}")
            
            # Simple conditioning format that works with all model types
            conditioning = [[batched_cond, {"pooled_output": batched_pooled}]]
                
        except Exception as e:
            print(f"Error creating negative batched conditioning: {e}")
            print("Falling back to list format...")
            # Fallback to list format if batching fails
            conditioning = []
            for i in range(len(cond_tensors)):
                cond_item = [cond_tensors[i], {"pooled_output": pooled_tensors[i]}]
                conditioning.append(cond_item)
        
        prompt_list_str = "|".join(prompt_lines)
        return (conditioning, prompt_list_str)


class EndlessNode_PromptCounter:
    """
    Utility node to count prompts from input text and display a preview.
    The preview will be shown in the console output and returned as a string output.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompts": ("STRING", {"multiline": True, "forceInput": True}),
                "print_to_console": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("count", "preview")
    FUNCTION = "count_prompts"
    CATEGORY = "Endless 🌊✨/BatchProcessing"

    def count_prompts(self, prompts, print_to_console):
        prompt_lines = [line.strip() for line in prompts.split('\n') if line.strip()]
        count = len(prompt_lines)

        preview = f"Found {count} prompt{'s' if count != 1 else ''}:\n"
        for i, prompt in enumerate(prompt_lines[:5]):
            preview += f"{i+1}. {prompt}\n"
        if count > 5:
            preview += f"... and {count - 5} more"

        if print_to_console:
            print(f"\n=== Prompt Counter ===")
            print(preview)
            print("======================\n")

        return (count, preview)

NODE_CLASS_MAPPINGS = {
    "EndlessNode_SimpleBatchPrompts": EndlessNode_SimpleBatchPrompts,
    "EndlessNode_FluxBatchPrompts": EndlessNode_FluxBatchPrompts,
    "EndlessNode_SDXLBatchPrompts": EndlessNode_SDXLBatchPrompts,
    "EndlessNode_BatchNegativePrompts": EndlessNode_BatchNegativePrompts,
    "EndlessNode_PromptCounter": EndlessNode_PromptCounter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EndlessNode_SimpleBatchPrompts": "Simple Batch Prompts",
    "EndlessNode_FluxBatchPrompts": "Flux Batch Prompts",
    "EndlessNode_SDXLBatchPrompts": "SDXL Batch Prompts",
    "EndlessNode_BatchNegativePrompts": "Batch Negative Prompts",
    "EndlessNode_PromptCounter": "Prompt Counter",
}