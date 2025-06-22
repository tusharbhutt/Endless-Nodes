import random
import time

class EndlessNode_RandomPromptSelector:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompts": ("STRING", {
                    "multiline": True,
                    "default": "Prompt A\nPrompt B\nPrompt C"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_prompt",)
    FUNCTION = "pick_random_prompt"
    CATEGORY = "Endless 🌊✨/Randomizers"
    
    def pick_random_prompt(self, prompts, seed):
        # Use the seed to ensure reproducible randomness
        random.seed(seed)
        
        lines = [line.strip() for line in prompts.splitlines() if line.strip()]
        if not lines:
            return ("",)
        return (random.choice(lines),)

class EndlessNode_RandomPromptMultiPicker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompts": ("STRING", {
                    "multiline": True,
                    "default": "Line 1\nLine 2\nLine 3\nLine 4"
                }),
                "num_to_pick": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 100,
                }),
                "allow_duplicates": ("BOOLEAN", {
                    "default": False
                }),
                "delimiter": ("STRING", {
                    "default": "\n"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_prompts",)
    FUNCTION = "pick_multiple"
    CATEGORY = "Endless 🌊✨/Randomizers"
    
    def pick_multiple(self, prompts, num_to_pick, allow_duplicates, delimiter, seed):
        # Use the seed to ensure reproducible randomness
        random.seed(seed)
        
        lines = [line.strip() for line in prompts.splitlines() if line.strip()]
        if not lines:
            return ("",)
        
        if allow_duplicates:
            picks = random.choices(lines, k=num_to_pick)
        else:
            picks = random.sample(lines, k=min(num_to_pick, len(lines)))
        
        return (delimiter.join(picks),)

# Optional: Auto-seed generator node
class EndlessNode_AutoSeed:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "base_seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1
                }),
            }
        }
    
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)
    FUNCTION = "generate_seed"
    CATEGORY = "Endless 🌊✨/Randomizers"
    
    def generate_seed(self, base_seed=0):
        # Generate a new seed based on current time and base seed
        current_time = int(time.time() * 1000000)  # microseconds for more variation
        new_seed = (base_seed + current_time) % (2**32 - 1)
        return (new_seed,)