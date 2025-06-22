class EndlessNode_FourInputIntSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("INT", {"default": 1, "min": 1, "max": 4}),
            },
            "optional": {
                "int1": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int2": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int3": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int4": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("INT",)
    FUNCTION = "switch_int"
    CATEGORY = "Endless 🌊✨/Integer Switches"
    OUTPUT_NODE = True
    
    def switch_int(self, switch, int1=None, int2=None, int3=None, int4=None):
        ints = [int1, int2, int3, int4]
        
        # Check if the selected switch position has a connected input
        if 1 <= switch <= 4:
            selected_value = ints[switch - 1]
            if selected_value is not None:
                return (selected_value,)
        
        # If no valid input is connected at the switch position, return 0
        return (0,)


class EndlessNode_SixInputIntSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("INT", {"default": 1, "min": 1, "max": 6}),
            },
            "optional": {
                "int1": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int2": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int3": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int4": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int5": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int6": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("INT",)
    FUNCTION = "switch_int"
    CATEGORY = "Endless 🌊✨/Integer Switches"
    OUTPUT_NODE = True
    
    def switch_int(self, switch, int1=None, int2=None, int3=None, int4=None, int5=None, int6=None):
        ints = [int1, int2, int3, int4, int5, int6]
        
        # Check if the selected switch position has a connected input
        if 1 <= switch <= 6:
            selected_value = ints[switch - 1]
            if selected_value is not None:
                return (selected_value,)
        
        # If no valid input is connected at the switch position, return 0
        return (0,)


class EndlessNode_EightInputIntSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("INT", {"default": 1, "min": 1, "max": 8}),
            },
            "optional": {
                "int1": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int2": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int3": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int4": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int5": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int6": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int7": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
                "int8": ("INT", {"default": 0, "max": 999999999999, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("INT",)
    FUNCTION = "switch_int"
    CATEGORY = "Endless 🌊✨/Integer Switches"
    OUTPUT_NODE = True
    
    def switch_int(self, switch, int1=None, int2=None, int3=None, int4=None, int5=None, int6=None, int7=None, int8=None):
        ints = [int1, int2, int3, int4, int5, int6, int7, int8]
        
        # Check if the selected switch position has a connected input
        if 1 <= switch <= 8:
            selected_value = ints[switch - 1]
            if selected_value is not None:
                return (selected_value,)
        
        # If no valid input is connected at the switch position, return 0
        return (0,)


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