from .endless_int_switches import (
    EndlessNode_FourInputIntSwitch,
    EndlessNode_SixInputIntSwitch,
    EndlessNode_EightInputIntSwitch,
)

NODE_CLASS_MAPPINGS = {
    "Four_Input_Int_Switch": EndlessNode_FourInputIntSwitch,
    "Six_Input_Int_Switch": EndlessNode_SixInputIntSwitch,
    "Eight_Input_Int_Switch": EndlessNode_EightInputIntSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Four_Input_Int_Switch": "Four Input Integer Switch",
    "Six_Input_Int_Switch": "Six Input Integer Switch",
    "Eight_Input_Int_Switch": "Eight Input Integer Switch",
}
