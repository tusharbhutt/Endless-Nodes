from .endless_int_switches_widget import (
    EndlessNode_FourInputIntSwitch_Widget,
    EndlessNode_SixInputIntSwitch_Widget,
    EndlessNode_EightInputIntSwitch_Widget,
)

NODE_CLASS_MAPPINGS = {
    "Four_Input_Int_Switch_Widget": EndlessNode_FourInputIntSwitch_Widget,
    "Six_Input_Int_Switch_Widget": EndlessNode_SixInputIntSwitch_Widget,
    "Eight_Input_Int_Switch_Widget": EndlessNode_EightInputIntSwitch_Widget,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Four_Input_Int_Switch_Widget": "Four Input Integer Switch (Widget)",
    "Six_Input_Int_Switch_Widget": "Six Input Integer Switch (Widget)",
    "Eight_Input_Int_Switch_Widget": "Eight Input Integer Switch (Widget)",
}
