from .endless_text_switches import (
    EndlessNode_FourInputTextSwitch,
    EndlessNode_SixInputTextSwitch,
    EndlessNode_EightInputTextSwitch,
)

NODE_CLASS_MAPPINGS = {
    "Four_Input_Text_Switch": EndlessNode_FourInputTextSwitch,
    "Six_Input_Text_Switch": EndlessNode_SixInputTextSwitch,
    "Eight_Input_Text_Switch": EndlessNode_EightInputTextSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Four_Input_Text_Switch": "Four Input Text Switch",
    "Six_Input_Text_Switch": "Six Input Text Switch",
    "Eight_Input_Text_Switch": "Eight Input Text Switch",
}
