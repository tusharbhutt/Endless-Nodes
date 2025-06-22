from .endless_randomizers import (
    EndlessNode_Mayhem,
    EndlessNode_Chaos,
    EndlessNode_Pandemonium,
)

NODE_CLASS_MAPPINGS = {
    "Randomzier_Mayhem": EndlessNode_Mayhem,
    "Randomzier_Chaos": EndlessNode_Chaos,
    # "Randomzier_Pandemonium": EndlessNode_Pandemonium,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Randomzier_Mayhem": "Mayhem Randomizer",
    "Randomzier_Chaos": "Chaos Randomizer",
    # "Randomzier_Pandemonium": "Pandemonium Randomizer",
}
