from .endless_randomizers import (
    EndlessNode_Mayhem,
    EndlessNode_Chaos,
    EndlessNode_Pandemonium,
)

NODE_CLASS_MAPPINGS = {
    "Randomizer_Mayhem": EndlessNode_Mayhem,
    "Randomizer_Chaos": EndlessNode_Chaos,
    "Randomizer_Pandemonium": EndlessNode_Pandemonium,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Randomizer_Mayhem": "Mayhem Randomizer",
    "Randomizer_Chaos": "Chaos Randomizer",
    "Randomizer_Pandemonium": "Pandemonium Randomizer",
}