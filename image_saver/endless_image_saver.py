import os
import json
import re
from server import PromptServer
from datetime import datetime

from PIL import Image, PngImagePlugin
import numpy as np
import torch
import folder_paths
from PIL.PngImagePlugin import PngInfo
import platform

def get_workflow(prompt=None, extra_pnginfo=None):
    from server import PromptServer

    # ✅ First: try directly from prompt
    if isinstance(prompt, dict) and "workflow" in prompt:
        return prompt["workflow"]

    # ✅ Second: try from extra_pnginfo
    if isinstance(extra_pnginfo, dict) and "workflow" in extra_pnginfo:
        print("[INFO] Workflow recovered from extra_pnginfo.")
        return extra_pnginfo["workflow"]

    # ✅ Third: fallback from PromptServer
    last = getattr(PromptServer.instance, "last_prompt", {})
    workflow = last.get("workflow")
    if workflow:
        print("[INFO] Workflow recovered from PromptServer.last_prompt.")
        return workflow

    raise ValueError("🚫 No workflow found in prompt, extra_pnginfo, or PromptServer context.")

        
class EndlessNode_Imagesaver:
    """
    Enhanced batch image saver with comprehensive metadata support
    Saves batched images with individual prompt names in filenames
    Automatically handles multiple images from batch processing
    Enhanced with workflow embedding, JSON export, and robust filename handling
    """
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.compress_level = 4
        # OS-specific filename length limits
        self.max_filename_length = self._get_max_filename_length()

    def _get_max_filename_length(self):
        """Get maximum filename length based on OS"""
        system = platform.system().lower()
        if system == 'windows':
            return 255  # NTFS limit
        elif system in ['linux', 'darwin']:  # Linux and macOS
            return 255  # ext4/APFS limit
        else:
            return 200  # Conservative fallback




    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"images": ("IMAGE", ),
                     "prompt_list": ("STRING", {"forceInput": True}),
                     "include_timestamp": ("BOOLEAN", {"default": True}),
                     "timestamp_format": ("STRING", {"default": "%Y-%m-%d_%H-%M-%S", "description": "Use Python strftime format.\nExample: %Y-%m-%d %H-%M-%S\nSee: strftime.org for full options."}),
                     "image_format": (["PNG", "JPEG", "WEBP"], {"default": "PNG"}),
                     "jpeg_quality": ("INT", {"default": 95, "min": 1, "max": 100, "step": 1}),
                     "delimiter": ("STRING", {"default": "_"}),
                     "prompt_words_limit": ("INT", {"default": 8, "min": 1, "max": 16, "step": 1}),
                     "embed_workflow": ("BOOLEAN", {"default": True}),
                     "save_json_metadata": ("BOOLEAN", {"default": False}),
                     # ITEM #2: Enable/disable number padding
                     "enable_filename_numbering": ("BOOLEAN", {"default": True}),
                     # ITEM #1: Filename Number Padding Control
                     "filename_number_padding": ("INT", {"default": 2, "min": 1, "max": 9, "step": 1}),
                     "filename_number_start": ("BOOLEAN", {"default": False}),
                     # ITEM #3: Conditional PNG Metadata Embedding  
                     "embed_png_metadata": ("BOOLEAN", {"default": True}),
                     },
                "optional":
                    {"output_path": ("STRING", {"default": ""}),
                     "filename_prefix": ("STRING", {"default": "Batch"}),
                     "negative_prompt_list": ("STRING", {"default": ""}),
                     "json_folder": ("STRING", {"default": ""}),
                     },
                "hidden": {
                    "prompt": "PROMPT", 
                    "extra_pnginfo": "EXTRA_PNGINFO"
                     }
                }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_paths",)
    FUNCTION = "save_batch_images"
    OUTPUT_NODE = True
    CATEGORY = "Endless 🌊✨/IO"

    def encode_emoji(self, obj):
        """Properly encode emojis and special characters"""
        if isinstance(obj, str):
            return obj.encode('utf-8', 'surrogatepass').decode('utf-8')
        return obj

    def clean_filename(self, text, max_words=8, delimiter="_"):
        """Clean text for use in filenames with word limit and emoji support"""
        # Limit to specified number of words
        words = text.split()[:max_words]
        text = ' '.join(words)
        
        # Handle emojis by encoding them properly
        text = self.encode_emoji(text)
        
        # Replace illegal characters with delimiter, then clean up spaces
        illegal_chars = r'[<>:"/\\|?*]'
        clean_text = re.sub(illegal_chars, delimiter, text)
        clean_text = re.sub(r'\s+', delimiter, clean_text)  # Replace spaces with delimiter
        clean_text = re.sub(r'[^\w\-_.{}]'.format(re.escape(delimiter)), '', clean_text)  # Keep only safe chars
        
        return clean_text

    def format_timestamp(self, dt, format_string, delimiter='_'):
        try:
            formatted = dt.strftime(format_string)
            # Replace colons first
            formatted = formatted.replace(':', '-')  
            # Then replace all whitespace with the user's delimiter
            if delimiter:
                formatted = re.sub(r'\s+', delimiter, formatted)
            return formatted
        except Exception as e:
            print(f"Invalid timestamp format: {e}")
            return dt.strftime("%Y-%m-%d_%H-%M-%S")
        
    def validate_and_process_path(self, path, delimiter="_"):
        if not path or path.strip() == "":
            return path

        now = datetime.now()

        # Normalize path separators
        path = path.replace("/", os.sep).replace("\\", os.sep)

        # Handle UNC or drive prefix
        unc_prefix = ""
        parts = path.split(os.sep)

        if path.startswith("\\\\"):  # UNC path
            if len(parts) >= 4:
                unc_prefix = os.sep.join(parts[:4])  # \\server\share
                parts = parts[4:]
            else:
                raise ValueError(f"Invalid UNC path: {path}")
        elif re.match(r"^[A-Za-z]:$", parts[0]):  # Drive letter
            unc_prefix = parts[0]
            parts = parts[1:]

        # Process the remaining subfolders
        processed_parts = []
        for part in parts:
            if not part:
                continue
            if "%" in part:
                # Format date placeholders
                formatted = self.format_timestamp(now, part, delimiter)
            else:
                # Sanitize folder names
                formatted = re.sub(r'[<>:"/\\|?*]', delimiter, part)
            processed_parts.append(formatted)

        # Reconstruct full path
        full_path = os.path.join(unc_prefix, *processed_parts)
        return full_path

    def ensure_filename_length(self, full_path, base_name, extension):
        """Ensure the full filename doesn't exceed OS limits"""
        directory = os.path.dirname(full_path)
        
        # Calculate available space for filename
        dir_length = len(directory) + 1  # +1 for path separator
        available_length = self.max_filename_length - len(extension)
        max_base_length = available_length - dir_length
        
        if len(base_name) > max_base_length:
            # Truncate base name to fit
            base_name = base_name[:max_base_length-3] + "..."  # -3 for ellipsis
        
        return os.path.join(directory, base_name + extension)

    def get_unique_filename(self, file_path):
        """Generate unique filename by adding incremental numbers if file exists"""
        if not os.path.exists(file_path):
            return file_path
        
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        
        counter = 1
        while True:
            new_name = f"{name}_{counter:03d}{ext}"
            new_path = os.path.join(directory, new_name)
            
            # Check length constraints
            if len(new_name) > self.max_filename_length:
                # Truncate original name to make room for counter
                available = self.max_filename_length - len(f"_{counter:03d}{ext}")
                truncated_name = name[:available-3] + "..."
                new_name = f"{truncated_name}_{counter:03d}{ext}"
                new_path = os.path.join(directory, new_name)
            
            if not os.path.exists(new_path):
                return new_path
            counter += 1

    def save_json_metadata(self, json_path, prompt_text, negative_text, 
                           batch_index, creation_time, prompt=None, extra_pnginfo=None):
        """Exports a drag-and-drop-compatible ComfyUI workflow JSON with optional metadata."""

        import json
        import math

        def sanitize_json(obj):
            if isinstance(obj, dict):
                return {k: sanitize_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [sanitize_json(v) for v in obj]
            elif isinstance(obj, float) and math.isnan(obj):
                return None
            else:
                return obj

        try:
            workflow = get_workflow(prompt)

            # ✅ Ensure core fields
            workflow.setdefault("version", 1)
            workflow.setdefault("nodes", [])
            workflow.setdefault("links", [])
            if "state" not in workflow:
                max_id = max((n.get("id", 0) for n in workflow["nodes"]), default=0)
                workflow["state"] = {"idCounter": max_id + 1}

            # ✅ Remove sidecar metadata if present
            workflow.pop("extra_pnginfo", None)

            # ✅ Embed custom metadata
            workflow["extra"] = workflow.get("extra", {})
            workflow["extra"].update({
                "prompt": prompt_text,
                "negative_prompt": negative_text,
                "batch_index": batch_index,
                "creation_time": creation_time,
                "source": "FluxSaver"
            })

            clean_json = sanitize_json(workflow)

            with open(json_path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(clean_json, f, indent=2, default=self.encode_emoji, ensure_ascii=False)

            print(f"[SUCCESS] Workflow JSON saved: {json_path}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to save workflow JSON: {e}")
            return False



    def generate_numbered_filename(self, filename_prefix, delimiter, counter, 
                                 filename_number_padding, filename_number_start, 
                                 enable_filename_numbering, date_str, clean_prompt, ext):
        """Generate filename with configurable number positioning and padding"""
        # ITEM #3: Build filename parts in the correct order based on settings
        filename_parts = []
        
        # Always add timestamp first if provided
        if date_str:
            filename_parts.append(date_str)
        
        # Add number after timestamp if number_start is True AND numbering is enabled
        if enable_filename_numbering and filename_number_start:
            counter_str = f"{counter:0{filename_number_padding}}"
            filename_parts.append(counter_str)
        
        # Add filename prefix if provided
        if filename_prefix:
            filename_parts.append(filename_prefix)
        
        # Add cleaned prompt
        filename_parts.append(clean_prompt)
        
        # Add number at the end if number_start is False AND numbering is enabled
        if enable_filename_numbering and not filename_number_start:
            counter_str = f"{counter:0{filename_number_padding}}"
            filename_parts.append(counter_str)
        
        # Join all parts with delimiter
        filename = delimiter.join(filename_parts) + ext
        
        return filename

    def save_batch_images(self, images, prompt_list, include_timestamp=True, 
                          timestamp_format="%Y-%m-%d_%H-%M-%S", image_format="PNG", 
                          jpeg_quality=95, delimiter="_", 
                          prompt_words_limit=8, embed_workflow=True, save_json_metadata=False,
                          enable_filename_numbering=True, filename_number_padding=2, 
                          filename_number_start=False, embed_png_metadata=True, 
                          output_path="", filename_prefix="batch", 
                          negative_prompt_list="", json_folder="", prompt=None, extra_pnginfo=None):

        # Debug: Print tensor information
        print(f"DEBUG: Images tensor shape: {images.shape}")
        print(f"DEBUG: Images tensor type: {type(images)}")

        # ✅ Fallback: repair prompt if missing or partial
        if prompt is None or not isinstance(prompt, dict) or "workflow" not in prompt:
            if extra_pnginfo and "workflow" in extra_pnginfo:
                print("[INFO] Workflow recovered from extra_pnginfo.")
                prompt = {"workflow": extra_pnginfo["workflow"]}
            else:
                print("[INFO] Workflow recovered from PromptServer.last_prompt.")
                prompt = PromptServer.instance.last_prompt or {}


        # Process output path with date/time validation (always process regardless of timestamp toggle)
        processed_output_path = self.validate_and_process_path(output_path, delimiter)
        
        # Set output directory
        if processed_output_path.strip() != "":
            if not os.path.isabs(processed_output_path):
                output_dir = os.path.join(self.output_dir, processed_output_path)
            else:
                output_dir = processed_output_path
        else:
            output_dir = self.output_dir
            
        # Create directory if it doesn't exist
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Could not create output directory {output_dir}: {e}")
        
        # Set up JSON directory
        if save_json_metadata:
            if json_folder.strip():
                processed_json_folder = self.validate_and_process_path(json_folder, delimiter)
                if not os.path.isabs(processed_json_folder):
                    json_dir = os.path.join(self.output_dir, processed_json_folder)
                else:
                    json_dir = processed_json_folder
            else:
                json_dir = output_dir
            
            try:
                os.makedirs(json_dir, exist_ok=True)
            except Exception as e:
                print(f"Warning: Could not create JSON directory {json_dir}: {e}")
                json_dir = output_dir
        
        # Generate datetime string if timestamp is enabled
        now = datetime.now()
        if include_timestamp:
            date_str = self.format_timestamp(now, timestamp_format, delimiter)
        else:
            date_str = None
        
        # Parse individual prompts from the prompt list
        individual_prompts = prompt_list.split('|')
        individual_negatives = negative_prompt_list.split('|') if negative_prompt_list else []
        
        # Set file extension
        if image_format == "PNG":
            ext = ".png"
        elif image_format == "JPEG":
            ext = ".jpg"
        elif image_format == "WEBP":
            ext = ".webp"
        else:
            ext = ".png"
            
        saved_paths = []
        
        # Handle different tensor formats
        if isinstance(images, torch.Tensor):
            # Convert to numpy for easier handling
            images_np = images.cpu().numpy()
            print(f"DEBUG: Converted to numpy shape: {images_np.shape}")
            
            # Check if we have a batch dimension
            if len(images_np.shape) == 4:  # Batch format: [B, H, W, C] or [B, C, H, W]
                batch_size = images_np.shape[0]
                print(f"DEBUG: Found batch of {batch_size} images")
                
                for i in range(batch_size):
                    try:
                        # Extract single image from batch
                        img_array = images_np[i]
                        
                        # Validate and process the image array
                        if len(img_array.shape) != 3:
                            raise ValueError(f"Expected 3D tensor for image {i+1}, got shape {img_array.shape}")
                        
                        # Convert to 0-255 range if needed
                        if img_array.max() <= 1.0:
                            img_array = img_array * 255.0
                        
                        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
                        
                        # Handle different channel orders (HWC vs CHW)
                        if img_array.shape[0] == 3 or img_array.shape[0] == 4:  # CHW format
                            img_array = np.transpose(img_array, (1, 2, 0))  # Convert to HWC
                        
                        img = Image.fromarray(img_array)
                        
                        # Get the corresponding prompt for this image
                        if i < len(individual_prompts):
                            prompt_text = individual_prompts[i].strip()
                        else:
                            # Cycle through prompts if we have more images than prompts
                            prompt_text = individual_prompts[i % len(individual_prompts)].strip()
                            print(f"Note: Cycling prompt for image {i+1} (using prompt {(i % len(individual_prompts)) + 1})")
                        
                        # Get corresponding negative prompt
                        negative_text = ""
                        if individual_negatives:
                            if i < len(individual_negatives):
                                negative_text = individual_negatives[i].strip()
                            else:
                                negative_text = individual_negatives[i % len(individual_negatives)].strip()
                        
                        # Clean the prompt for filename use
                        clean_prompt = self.clean_filename(prompt_text, prompt_words_limit, delimiter)
                        
                        # Generate filename using the new method
                        filename = self.generate_numbered_filename(
                            filename_prefix, delimiter, i+1, 
                            filename_number_padding, filename_number_start, 
                            enable_filename_numbering, date_str, clean_prompt, ext
                        )
                        
                        # Create full file path and ensure length constraints
                        base_filename = os.path.splitext(filename)[0]
                        temp_path = os.path.join(output_dir, filename)
                        file_path = self.ensure_filename_length(temp_path, base_filename, ext)
                        
                        # Ensure unique filename
                        file_path = self.get_unique_filename(file_path)
                        
                        # Create JSON path if needed
                        if save_json_metadata:
                            json_base = os.path.splitext(os.path.basename(file_path))[0]
                            json_path = os.path.join(json_dir, json_base + ".json")
                            json_path = self.get_unique_filename(json_path)
                        
                        # Save image based on format
                        if image_format == "PNG":
                            # ITEM #3: Conditional PNG metadata embedding
                            if embed_png_metadata:
                                metadata = PngImagePlugin.PngInfo()
                                metadata.add_text("prompt", prompt_text)
                                metadata.add_text("negative_prompt", negative_text)
                                metadata.add_text("batch_index", str(i + 1))
                                metadata.add_text("creation_time", now.isoformat())

                                if embed_workflow and prompt and "workflow" in prompt:
                                    metadata.add_text("workflow", json.dumps(prompt, default=self.encode_emoji))

                                if extra_pnginfo:
                                    for key, value in extra_pnginfo.items():
                                        metadata.add_text(key, json.dumps(value, default=self.encode_emoji))

                                img.save(file_path, format="PNG", optimize=True,
                                         compress_level=self.compress_level, pnginfo=metadata)
                            else:
                                img.save(file_path, format="PNG", optimize=True,
                                         compress_level=self.compress_level)

                            
                        elif image_format == "JPEG":
                            # Convert RGBA to RGB for JPEG
                            if img.mode == 'RGBA':
                                background = Image.new('RGB', img.size, (255, 255, 255))
                                background.paste(img, mask=img.split()[-1])
                                img = background
                            img.save(file_path, format="JPEG", quality=jpeg_quality, optimize=True)
                            
                        elif image_format == "WEBP":
                            img.save(file_path, format="WEBP", quality=jpeg_quality, method=6)
                        
                        # Save JSON metadata if requested
                        if save_json_metadata:
                            self.save_json_metadata(json_path, prompt_text, negative_text, 
                                                  i+1, now.isoformat(), prompt, extra_pnginfo)
                        
                        saved_paths.append(file_path)
                        print(f"Saved: {os.path.basename(file_path)}")
                        print(f"  Prompt: {prompt_text}")
                        if negative_text:
                            print(f"  Negative: {negative_text}")
                        if save_json_metadata:
                            print(f"  JSON: {os.path.basename(json_path)}")
                        
                    except Exception as e:
                        error_msg = f"Failed to save image {i+1}: {e}"
                        print(error_msg)
                        # Continue with other images rather than failing completely
                        saved_paths.append(f"ERROR: {error_msg}")
            
            elif len(images_np.shape) == 3:  # Single image format: [H, W, C]
                print("DEBUG: Single image detected, processing as batch of 1")
                # Process as single image
                img_array = images_np
                
                # Convert to 0-255 range if needed
                if img_array.max() <= 1.0:
                    img_array = img_array * 255.0
                
                img_array = np.clip(img_array, 0, 255).astype(np.uint8)
                img = Image.fromarray(img_array)
                
                prompt_text = individual_prompts[0].strip() if individual_prompts else "no_prompt"
                negative_text = individual_negatives[0].strip() if individual_negatives else ""
                clean_prompt = self.clean_filename(prompt_text, prompt_words_limit, delimiter)
                
                # Generate filename using the new method
                filename = self.generate_numbered_filename(
                    filename_prefix, delimiter, 1, 
                    filename_number_padding, filename_number_start, 
                    enable_filename_numbering, date_str, clean_prompt, ext
                )
                
                base_filename = os.path.splitext(filename)[0]
                temp_path = os.path.join(output_dir, filename)
                file_path = self.ensure_filename_length(temp_path, base_filename, ext)
                file_path = self.get_unique_filename(file_path)
                
                if save_json_metadata:
                    json_base = os.path.splitext(os.path.basename(file_path))[0]
                    json_path = os.path.join(json_dir, json_base + ".json")
                    json_path = self.get_unique_filename(json_path)
                
                if image_format == "PNG":
                    # ITEM #3: Conditional PNG metadata embedding
                    if embed_png_metadata:
                        metadata = PngImagePlugin.PngInfo()
                        metadata.add_text("prompt", prompt_text)
                        metadata.add_text("negative_prompt", negative_text)
                        metadata.add_text("batch_index", "1")
                        metadata.add_text("creation_time", now.isoformat())
                        
                        if embed_workflow:
                            if prompt is not None:
                                metadata.add_text("workflow", json.dumps(prompt, default=self.encode_emoji))
                            if extra_pnginfo is not None:
                                for key, value in extra_pnginfo.items():
                                    metadata.add_text(key, json.dumps(value, default=self.encode_emoji))
                        
                        img.save(file_path, format="PNG", optimize=True, 
                               compress_level=self.compress_level, pnginfo=metadata)
                    else:
                        # ITEM #3: Save clean PNG without metadata
                        img.save(file_path, format="PNG", optimize=True, 
                               compress_level=self.compress_level)
                elif image_format == "JPEG":
                    if img.mode == 'RGBA':
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    img.save(file_path, format="JPEG", quality=jpeg_quality, optimize=True)
                elif image_format == "WEBP":
                    img.save(file_path, format="WEBP", quality=jpeg_quality, method=6)
                
                if save_json_metadata:
                    self.save_json_metadata(json_path, prompt_text, negative_text, 
                                          1, now.isoformat(), prompt, extra_pnginfo)
                
                saved_paths.append(file_path)
                print(f"Saved: {os.path.basename(file_path)}")
                print(f"  Prompt: {prompt_text}")
            
            else:
                raise ValueError(f"Unexpected image tensor shape: {images_np.shape}")
        
        else:
            # Handle case where images might be a list
            print(f"DEBUG: Images is not a tensor, type: {type(images)}")
            for i, image in enumerate(images):
                try:
                    if isinstance(image, torch.Tensor):
                        img_array = image.cpu().numpy()
                    else:
                        img_array = np.array(image)
                    
                    # Process similar to above...
                    if img_array.max() <= 1.0:
                        img_array = img_array * 255.0
                    
                    img_array = np.clip(img_array, 0, 255).astype(np.uint8)
                    
                    if len(img_array.shape) == 3 and (img_array.shape[0] == 3 or img_array.shape[0] == 4):
                        img_array = np.transpose(img_array, (1, 2, 0))
                    
                    img = Image.fromarray(img_array)
                    
                    prompt_text = individual_prompts[i % len(individual_prompts)].strip() if individual_prompts else "no_prompt"
                    negative_text = individual_negatives[i % len(individual_negatives)].strip() if individual_negatives else ""
                    clean_prompt = self.clean_filename(prompt_text, prompt_words_limit, delimiter)
                    
                    # Generate filename using the new method
                    filename = self.generate_numbered_filename(
                        filename_prefix, delimiter, i+1, 
                        filename_number_padding, filename_number_start, 
                        enable_filename_numbering, date_str, clean_prompt, ext
                    )
                    
                    base_filename = os.path.splitext(filename)[0]
                    temp_path = os.path.join(output_dir, filename)
                    file_path = self.ensure_filename_length(temp_path, base_filename, ext)
                    file_path = self.get_unique_filename(file_path)
                    
                    if save_json_metadata:
                        json_base = os.path.splitext(os.path.basename(file_path))[0]
                        json_path = os.path.join(json_dir, json_base + ".json")
                        json_path = self.get_unique_filename(json_path)
                    
                    # ITEM #3: Apply conditional PNG metadata for all image formats logic
                    if image_format == "PNG" and embed_png_metadata:
                        metadata = PngImagePlugin.PngInfo()
                        metadata.add_text("prompt", prompt_text)
                        metadata.add_text("negative_prompt", negative_text)
                        metadata.add_text("batch_index", str(i+1))
                        metadata.add_text("creation_time", now.isoformat())
                        
                        if embed_workflow:
                            if prompt is not None:
                                metadata.add_text("workflow", json.dumps(prompt, default=self.encode_emoji))
                            if extra_pnginfo is not None:
                                for key, value in extra_pnginfo.items():
                                    metadata.add_text(key, json.dumps(value, default=self.encode_emoji))
                        
                        img.save(file_path, format="PNG", optimize=True, 
                               compress_level=self.compress_level, pnginfo=metadata)
                    else:
                        img.save(file_path, format=image_format.upper())
                    
                    if save_json_metadata:
                        self.save_json_metadata(json_path, prompt_text, negative_text, 
                                              i+1, now.isoformat(), prompt, extra_pnginfo)
                    
                    saved_paths.append(file_path)
                    print(f"Saved: {os.path.basename(file_path)}")
                    
                except Exception as e:
                    error_msg = f"Failed to save image {i+1}: {e}"
                    print(error_msg)
                    saved_paths.append(f"ERROR: {error_msg}")
        
        # Return all saved paths joined with newlines
        return ("\n".join(saved_paths),)