import random

def ensure_order(a, b):
    return (a, b) if a <= b else (b, a)

class EndlessNode_Mayhem:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "steps_min": ("INT", {"default": 20, "min": 1, "max": 150}),
                "steps_max": ("INT", {"default": 40, "min": 1, "max": 150}),
                "cfg_min": ("FLOAT", {"default": 6.0, "min": 1.0, "max": 20.0}),
                "cfg_max": ("FLOAT", {"default": 12.0, "min": 1.0, "max": 20.0}),
                "guidance_min": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 6.0}),
                "guidance_max": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 6.0}),
                "height_min": ("INT", {"default": 512, "min": 256, "max": 4096}),
                "height_max": ("INT", {"default": 768, "min": 256, "max": 4096}),
                "width_min": ("INT", {"default": 512, "min": 256, "max": 4096}),
                "width_max": ("INT", {"default": 768, "min": 256, "max": 4096}),
                "flip_dimensions": ("BOOLEAN", {"default": True}),
                "divisible_by_64": ("BOOLEAN", {"default": False}),
                "seed_min": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "seed_max": ("INT", {"default": 8675309, "min": 0, "max": 2**32 - 1}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1
                }),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT", "FLOAT", "INT", "INT", "INT")
    RETURN_NAMES = ("steps", "cfg_scale", "cfg_guidance", "height", "width", "seed")
    FUNCTION = "randomize_with_flip"
    CATEGORY = "Endless 🌊✨/Randomizers"

    def randomize_with_flip(self, steps_min, steps_max, cfg_min, cfg_max, guidance_min, guidance_max, height_min, height_max, width_min, width_max, flip_dimensions, divisible_by_64, seed_min, seed_max, seed):
        # Use the seed to ensure reproducible randomness
        random.seed(seed)
        
        # Set divisibility requirement
        divisor = 64 if divisible_by_64 else 16
        
        # Min and max sanity checks

        steps_min, steps_max = ensure_order(steps_min, steps_max)
        cfg_min, cfg_max = ensure_order(cfg_min, cfg_max)
        guidance_min, guidance_max = ensure_order(guidance_min, guidance_max)
        height_min, height_max = ensure_order(height_min, height_max)
        width_min, width_max = ensure_order(width_min, width_max)
        seed_min, seed_max = ensure_order(seed_min, seed_max)


        # Ensure dimensions are divisible by divisor and at least 256
        height_min = max(256, (height_min // divisor) * divisor)
        height_max = max(256, (height_max // divisor) * divisor)
        width_min = max(256, (width_min // divisor) * divisor)
        width_max = max(256, (width_max // divisor) * divisor)

        # Random values
        steps = random.randint(steps_min, steps_max)
        cfg_scale = round(random.uniform(cfg_min, cfg_max), 2)
        cfg_guidance = round(random.uniform(guidance_min, guidance_max), 2)

        # Pick values based on user-defined intent
        height = random.randint(height_min // divisor, height_max // divisor) * divisor
        width = random.randint(width_min // divisor, width_max // divisor) * divisor

        # Flip output if requested
        if flip_dimensions and random.random() < 0.5:
            width, height = height, width
        
        output_seed = random.randint(seed_min, seed_max)
        return (steps, cfg_scale, cfg_guidance, height, width, output_seed)


class EndlessNode_Chaos:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "steps_min": ("INT", {"default": 20, "min": 1, "max": 150}),
                "steps_max": ("INT", {"default": 40, "min": 1, "max": 150}),
                "cfg_min": ("FLOAT", {"default": 6.0, "min": 1.0, "max": 20.0}),
                "cfg_max": ("FLOAT", {"default": 12.0, "min": 1.0, "max": 20.0}),
                "guidance_min": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 6.0}),
                "guidance_max": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 6.0}),
                "dimension_min": ("INT", {"default": 512, "min": 256, "max": 4096}),
                "dimension_max": ("INT", {"default": 1024, "min": 256, "max": 4096}),
                "orientation": (["portrait", "landscape", "square", "random"], {"default": "random"}),
                "divisible_by_64": ("BOOLEAN", {"default": False}),
                "seed_min": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "seed_max": ("INT", {"default": 8675309, "min": 0, "max": 2**32 - 1}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1
                }),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT", "FLOAT", "INT", "INT", "INT")
    RETURN_NAMES = ("steps", "cfg_scale", "cfg_guidance", "height", "width", "seed")
    FUNCTION = "randomize_aspect_ratio_chaos"
    CATEGORY = "Endless 🌊✨/Randomizers"

    def randomize_aspect_ratio_chaos(self, steps_min, steps_max, cfg_min, cfg_max, guidance_min, guidance_max, dimension_min, dimension_max, orientation, divisible_by_64, seed_min, seed_max, seed):
        # Use the seed to ensure reproducible randomness
        random.seed(seed)
        
        # Set divisibility requirement
        divisor = 64 if divisible_by_64 else 16
        

        # Min and max sanity checks

        steps_min, steps_max = ensure_order(steps_min, steps_max)
        cfg_min, cfg_max = ensure_order(cfg_min, cfg_max)
        guidance_min, guidance_max = ensure_order(guidance_min, guidance_max)
        dimension_min, dimension_max = ensure_order(dimension_min, dimension_max)
        seed_min, seed_max = ensure_order(seed_min, seed_max)


        # Ensure min/max dimensions are properly divisible
        dimension_min = max(256, (dimension_min // divisor) * divisor)
        dimension_max = max(256, (dimension_max // divisor) * divisor)
        
        # Common aspect ratios (width:height)
        aspect_ratios = [
            (1, 1),      # 1:1 Square
            (4, 3),      # 4:3 Classic
            (3, 2),      # 3:2 Classic photo
            (16, 9),     # 16:9 Widescreen
            (5, 4),      # 5:4 
            (5, 3),      # 5:3
            (7, 5),      # 7:5
            (8, 5),      # 8:5
            (192, 100),  # 1.92:1 Instagram Stories
            (21, 9),     # 21:9 Ultrawide (2.33:1)
            (9, 21),     # 9:21 Ultra-tall mobile
            (22, 10),    # 2.2:1 70mm Cinema
            (28, 10),    # 2.8:1 Facebook Cover (approx)
            (185, 100),  # 1.85:1 Cinema
            (239, 100),  # 2.39:1 Anamorphic
        ]
        
        # Filter aspect ratios based on orientation
        if orientation == "square":
            filtered_ratios = [(1, 1)]
        elif orientation == "landscape":
            filtered_ratios = [(w, h) for w, h in aspect_ratios if w > h]
        elif orientation == "portrait":
            filtered_ratios = [(h, w) for w, h in aspect_ratios if w > h]  # Flip to portrait
            filtered_ratios.append((1, 1))  # Include square
        else:  # random
            # Include both orientations for non-square ratios
            all_ratios = []
            for w, h in aspect_ratios:
                all_ratios.append((w, h))  # Landscape
                if w != h:  # Don't duplicate square
                    all_ratios.append((h, w))  # Portrait
            filtered_ratios = all_ratios
        
        # Find valid dimensions for each aspect ratio
        valid_dimensions = []
        
        for aspect_w, aspect_h in filtered_ratios:
            # Try different scales to find dimensions within our bounds
            for scale in range(1, 100):  # Reasonable scale range
                width = (aspect_w * scale * divisor) // divisor * divisor
                height = (aspect_h * scale * divisor) // divisor * divisor
                
                # Check if dimensions are within bounds
                if (dimension_min <= width <= dimension_max and 
                    dimension_min <= height <= dimension_max):
                    valid_dimensions.append((width, height))
                
                # If we've exceeded max dimension, no point in larger scales
                if width > dimension_max or height > dimension_max:
                    break
        
        # Remove duplicates and ensure we have at least one option
        valid_dimensions = list(set(valid_dimensions))
        
        if not valid_dimensions:
            # Fallback to square if no valid aspect ratios found
            size = (dimension_min // divisor) * divisor
            valid_dimensions = [(size, size)]
        
        # Choose random dimensions
        width, height = random.choice(valid_dimensions)
        
        # Generate other random values
        steps = random.randint(steps_min, steps_max)
        cfg_scale = round(random.uniform(cfg_min, cfg_max), 2)
        output_seed = random.randint(seed_min, seed_max)
        cfg_guidance = round(random.uniform(guidance_min, guidance_max), 2)
        
        return (steps, cfg_scale, cfg_guidance, height, width, output_seed)


class EndlessNode_Pandemonium:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "divisible_by_64": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1
                }),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT", "FLOAT", "INT", "INT", "INT")
    RETURN_NAMES = ("steps", "cfg_scale", "cfg_guidance", "height", "width", "seed")
    FUNCTION = "randomize_aspect_ratio_mayhem"
    CATEGORY = "Endless 🌊✨/Randomizers"

    def randomize_aspect_ratio_mayhem(self, divisible_by_64, seed):
        import random
        random.seed(seed)

        # Fixed internal config
        dimension_min = 512
        dimension_max = 1536
        divisor = 64 if divisible_by_64 else 16

        dimension_min = max(256, (dimension_min // divisor) * divisor)
        dimension_max = max(256, (dimension_max // divisor) * divisor)

        # All aspect ratios (landscape + portrait + square)
        aspect_ratios = [
            (1, 1),
            (4, 3), (3, 2),
            (16, 9), (9, 16),
            (5, 4), (4, 5),
            (5, 3), (3, 5),
            (7, 5), (5, 7),
            (8, 5), (5, 8),
            (192, 100), (100, 192),
            (21, 9), (9, 21),
            (22, 10), (10, 22),
            (28, 10), (10, 28),
            (185, 100), (100, 185),
            (239, 100), (100, 239)
        ]

        valid_dimensions = []

        for aspect_w, aspect_h in aspect_ratios:
            for scale in range(1, 100):
                width = (aspect_w * scale * divisor) // divisor * divisor
                height = (aspect_h * scale * divisor) // divisor * divisor
                if dimension_min <= width <= dimension_max and dimension_min <= height <= dimension_max:
                    valid_dimensions.append((width, height))
                if width > dimension_max or height > dimension_max:
                    break

        if not valid_dimensions:
            fallback = (dimension_min // divisor) * divisor
            valid_dimensions = [(fallback, fallback)]

        width, height = random.choice(valid_dimensions)
        steps = random.randint(5, 60)
        cfg_scale = round(random.uniform(0, 15), 2)
        cfg_guidance = round(random.uniform(1, 4), 2)
        output_seed = random.randint(0, seed)

        return (steps, cfg_scale, cfg_guidance, height, width, output_seed)

