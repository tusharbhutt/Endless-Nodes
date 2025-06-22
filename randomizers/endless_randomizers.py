import random

# Safe samplers and schedulers for Flux (example set from your flux matrix)
SAFE_SAMPLERS = [
    "DDIM", "Euler", "Euler a", "LMS", "Heun", "DPM2", "DPM2 a", "DPM++ 2S a", "DPM++ 2M", "DPM++ SDE"
]
SAFE_SCHEDULERS = [
    "Default", "Scheduler A", "Scheduler B"  # Replace with actual safe schedulers if known
]

class EndlessNode_Mayhem:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "steps_min": ("INT", {"default": 20, "min": 1, "max": 150}),
                "steps_max": ("INT", {"default": 40, "min": 1, "max": 150}),
                "cfg_min": ("FLOAT", {"default": 6.0, "min": 1.0, "max": 20.0}),
                "cfg_max": ("FLOAT", {"default": 12.0, "min": 1.0, "max": 20.0}),
                "height_min": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "height_max": ("INT", {"default": 768, "min": 256, "max": 4096}),
                "width_min": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "width_max": ("INT", {"default": 768, "min": 256, "max": 4096}),
                "seed_min": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "seed_max": ("INT", {"default": 8675309, "min": 0, "max": 2**32 - 1}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1
                }),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT", "INT", "INT", "INT")
    RETURN_NAMES = ("steps", "cfg_scale", "height", "width", "seed")
    FUNCTION = "randomize"
    CATEGORY = "Endless 🌊✨/Randomizers"

    def randomize(self, steps_min, steps_max, cfg_min, cfg_max, height_min, height_max, width_min, width_max, seed_min, seed_max, seed):
        # Use the seed to ensure reproducible randomness
        random.seed(seed)
        
        # Ensure dimensions are divisible by 16 and at least 256
        height_min = max(256, (height_min // 16) * 16)
        height_max = max(256, (height_max // 16) * 16)
        width_min = max(256, (width_min // 16) * 16)
        width_max = max(256, (width_max // 16) * 16)
        
        steps = random.randint(steps_min, steps_max)
        cfg_scale = round(random.uniform(cfg_min, cfg_max), 2)
        height = random.randint(height_min // 16, height_max // 16) * 16
        width = random.randint(width_min // 16, width_max // 16) * 16
        output_seed = random.randint(seed_min, seed_max)
        return (steps, cfg_scale, height, width, output_seed)

class EndlessNode_Chaos:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "steps_min": ("INT", {"default": 20, "min": 1, "max": 150}),
                "steps_max": ("INT", {"default": 40, "min": 1, "max": 150}),
                "cfg_min": ("FLOAT", {"default": 6.0, "min": 1.0, "max": 20.0}),
                "cfg_max": ("FLOAT", {"default": 12.0, "min": 1.0, "max": 20.0}),
                "height_min": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "height_max": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "width_min": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "width_max": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "seed_min": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "seed_max": ("INT", {"default": 8675309, "min": 0, "max": 2**32 - 1}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1
                }),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT", "INT", "INT", "INT")
    RETURN_NAMES = ("steps", "cfg_scale", "height", "width", "seed")
    FUNCTION = "randomize_with_flip"
    CATEGORY = "Endless 🌊✨/Randomizers"

    def randomize_with_flip(self, steps_min, steps_max, cfg_min, cfg_max, height_min, height_max, width_min, width_max, seed_min, seed_max, seed):
        # Use the seed to ensure reproducible randomness
        random.seed(seed)
        
        # Ensure dimensions are divisible by 16 and at least 256
        height_min = max(256, (height_min // 16) * 16)
        height_max = max(256, (height_max // 16) * 16)
        width_min = max(256, (width_min // 16) * 16)
        width_max = max(256, (width_max // 16) * 16)
        
        steps = random.randint(steps_min, steps_max)
        cfg_scale = round(random.uniform(cfg_min, cfg_max), 2)

        # Randomly flip height and width with 50% chance
        if random.random() < 0.5:
            height = random.randint(height_min // 16, height_max // 16) * 16
            width = random.randint(width_min // 16, width_max // 16) * 16
        else:
            width = random.randint(height_min // 16, height_max // 16) * 16
            height = random.randint(width_min // 16, width_max // 16) * 16

        output_seed = random.randint(seed_min, seed_max)
        return (steps, cfg_scale, height, width, output_seed)

class EndlessNode_Pandemonium:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "steps_min": ("INT", {"default": 20, "min": 1, "max": 150}),
                "steps_max": ("INT", {"default": 40, "min": 1, "max": 150}),
                "cfg_min": ("FLOAT", {"default": 6.0, "min": 1.0, "max": 20.0}),
                "cfg_max": ("FLOAT", {"default": 12.0, "min": 1.0, "max": 20.0}),
                "height_min": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "height_max": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "width_min": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "width_max": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "seed_min": ("INT", {"default": 0, "min": 0, "max": 2**32-1}),
                "seed_max": ("INT", {"default": 8675309, "min": 0, "max": 2**32 - 1}),
                "samplers": ("STRING", {
                    "multiline": True,
                    "default": "euler\neuler_ancestral\nheun\nheunpp2\ndpm_2\ndpm_2_ancestral\nlms\ndpm_fast\ndpm_adaptive\ndpmpp_2s_ancestral\ndpmpp_sde\ndpmpp_sde_gpu\ndpmpp_2m\ndpmpp_2m_sde\ndpmpp_2m_sde_gpu\ndpmpp_3m_sde\ndpmpp_3m_sde_gpu\nddpm\nlcm\nddim\nuni_pc\nuni_pc_bh2"
                }),
                "schedulers": ("STRING", {
                    "multiline": True,
                    "default": "normal\nkarras\nexponential\nsgm_uniform\nsimple\nddim_uniform\nbeta"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1
                }),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT", "INT", "INT", "INT", "STRING", "STRING")
    RETURN_NAMES = ("steps", "cfg_scale", "height", "width", "seed", "sampler", "scheduler")
    FUNCTION = "randomize_all"
    CATEGORY = "Endless 🌊✨/Randomizers"

    def randomize_all(self, steps_min, steps_max, cfg_min, cfg_max, height_min, height_max, width_min, width_max, seed_min, seed_max, samplers, schedulers, seed):
        # Use the seed to ensure reproducible randomness
        random.seed(seed)
        
        # Ensure dimensions are divisible by 16 and at least 256
        height_min = max(256, (height_min // 16) * 16)
        height_max = max(256, (height_max // 16) * 16)
        width_min = max(256, (width_min // 16) * 16)
        width_max = max(256, (width_max // 16) * 16)
        
        steps = random.randint(steps_min, steps_max)
        cfg_scale = round(random.uniform(cfg_min, cfg_max), 2)
        height = random.randint(height_min // 16, height_max // 16) * 16
        width = random.randint(width_min // 16, width_max // 16) * 16
        output_seed = random.randint(seed_min, seed_max)

        # Parse samplers and schedulers from input strings
        sampler_list = [s.strip() for s in samplers.splitlines() if s.strip()]
        scheduler_list = [s.strip() for s in schedulers.splitlines() if s.strip()]
        
        # Fallback to defaults if lists are empty
        if not sampler_list:
            sampler_list = SAFE_SAMPLERS
        if not scheduler_list:
            scheduler_list = SAFE_SCHEDULERS

        sampler = random.choice(sampler_list)
        scheduler = random.choice(scheduler_list)

        return (steps, cfg_scale, height, width, output_seed, sampler, scheduler)