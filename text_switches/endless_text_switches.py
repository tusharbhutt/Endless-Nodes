# text_switches.py

class EndlessNode_FourInputTextSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("INT", {"default": 1, "min": 1, "max": 4, "widget": "int"}),
            },
            "optional": {
                "text1": ("STRING", {"default": ""}),
                "text2": ("STRING", {"default": ""}),
                "text3": ("STRING", {"default": ""}),
                "text4": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "switch_text"
    CATEGORY = "Endless 🌊✨/Text Switches"
    OUTPUT_NODE = True

    def switch_text(self, switch, text1, text2, text3, text4):
        texts = [text1, text2, text3, text4]
        if 1 <= switch <= 4:
            return (texts[switch - 1],)
        return ("",)


class EndlessNode_SixInputTextSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("INT", {"default": 1, "min": 1, "max": 6, "widget": "int"}),
            },
            "optional": {
                "text1": ("STRING", {"default": ""}),
                "text2": ("STRING", {"default": ""}),
                "text3": ("STRING", {"default": ""}),
                "text4": ("STRING", {"default": ""}),
                "text5": ("STRING", {"default": ""}),
                "text6": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "switch_text"
    CATEGORY = "Endless 🌊✨/Text Switches"
    OUTPUT_NODE = True

    def switch_text(self, switch, text1, text2, text3, text4, text5, text6):
        texts = [text1, text2, text3, text4, text5, text6]
        if 1 <= switch <= 6:
            return (texts[switch - 1],)
        return ("",)


class EndlessNode_EightInputTextSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("INT", {"default": 1, "min": 1, "max": 8, "widget": "int"}),
            },
            "optional": {
                "text1": ("STRING", {"default": ""}),
                "text2": ("STRING", {"default": ""}),
                "text3": ("STRING", {"default": ""}),
                "text4": ("STRING", {"default": ""}),
                "text5": ("STRING", {"default": ""}),
                "text6": ("STRING", {"default": ""}),
                "text7": ("STRING", {"default": ""}),
                "text8": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "switch_text"
    CATEGORY = "Endless 🌊✨/Text Switches"
    OUTPUT_NODE = True

    def switch_text(self, switch, text1, text2, text3, text4, text5, text6, text7, text8):
        texts = [text1, text2, text3, text4, text5, text6, text7, text8]
        if 1 <= switch <= 8:
            return (texts[switch - 1],)
        return ("",)


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