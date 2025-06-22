class EndlessNode_FourInputIntSwitch_Widget:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("INT", {"default": 1, "min": 1, "max": 4, "widget": "int"}),
            },
            "optional": {
                "int1": ("INT", {"default": 0, "widget": "int"}),
                "int2": ("INT", {"default": 0, "widget": "int"}),
                "int3": ("INT", {"default": 0, "widget": "int"}),
                "int4": ("INT", {"default": 0, "widget": "int"}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "switch_int"
    CATEGORY = "Endless 🌊✨/Integer Switches"
    OUTPUT_NODE = True

    def switch_int(self, switch, int1, int2, int3, int4):
        ints = [int1, int2, int3, int4]
        if 1 <= switch <= 4:
            return (ints[switch - 1],)
        return (0,)


class EndlessNode_SixInputIntSwitch_Widget:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("INT", {"default": 1, "min": 1, "max": 6, "widget": "int"}),
            },
            "optional": {
                "int1": ("INT", {"default": 0, "widget": "int"}),
                "int2": ("INT", {"default": 0, "widget": "int"}),
                "int3": ("INT", {"default": 0, "widget": "int"}),
                "int4": ("INT", {"default": 0, "widget": "int"}),
                "int5": ("INT", {"default": 0, "widget": "int"}),
                "int6": ("INT", {"default": 0, "widget": "int"}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "switch_int"
    CATEGORY = "Endless 🌊✨/Integer Switches"
    OUTPUT_NODE = True

    def switch_int(self, switch, int1, int2, int3, int4, int5, int6):
        ints = [int1, int2, int3, int4, int5, int6]
        if 1 <= switch <= 6:
            return (ints[switch - 1],)
        return (0,)


class EndlessNode_EightInputIntSwitch_Widget:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("INT", {"default": 1, "min": 1, "max": 8, "widget": "int"}),
            },
            "optional": {
                "int1": ("INT", {"default": 0, "widget": "int"}),
                "int2": ("INT", {"default": 0, "widget": "int"}),
                "int3": ("INT", {"default": 0, "widget": "int"}),
                "int4": ("INT", {"default": 0, "widget": "int"}),
                "int5": ("INT", {"default": 0, "widget": "int"}),
                "int6": ("INT", {"default": 0, "widget": "int"}),
                "int7": ("INT", {"default": 0, "widget": "int"}),
                "int8": ("INT", {"default": 0, "widget": "int"}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "switch_int"
    CATEGORY = "Endless 🌊✨/Integer Switches"
    OUTPUT_NODE = True

    def switch_int(self, switch, int1, int2, int3, int4, int5, int6, int7, int8):
        ints = [int1, int2, int3, int4, int5, int6, int7, int8]
        if 1 <= switch <= 8:
            return (ints[switch - 1],)
        return (0,)


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