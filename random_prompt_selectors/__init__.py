from .endless_random_prompt_selectors import (
    EndlessNode_RandomPromptSelector,
    EndlessNode_RandomPromptMultiPicker,
)


NODE_CLASS_MAPPINGS = {
    "Random_Prompt_Selector": EndlessNode_RandomPromptSelector,
    "Random_Prompt_Multipicker": EndlessNode_RandomPromptMultiPicker,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Random_Prompt_Selector": "Random Prompt Selector",
    "Random_Prompt_Multipicker": "Random Multiprompt Picker"
}