#--------------------------------------
# Endless Sea of Stars Custom Node Collection
#https://github.com/tusharbhutt/Endless-Nodes
#
#


import torch
import numpy as np
import os
import sys
import io
import json


sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))
#heh, probably not needed

import comfy.sd
import comfy.utils

import folder_paths
import typing as tg

#--------------------------------------
#Six Text Input Node for selection


class EndlessNode_SixTextInputSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 6, "step": 1, "display": "slider"}),      
#I like the slider idea, it's better for a touch screen				
                "text1": ("STRING", {"forceInput": True}),               
            },
            "optional": {
                "text2": ("STRING", {"forceInput": True}),
                "text3": ("STRING", {"forceInput": True}),
                "text4": ("STRING", {"forceInput": True}),
                "text5": ("STRING", {"forceInput": True}),
                "text6": ("STRING", {"forceInput": True}),				
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Output",)	
    
    FUNCTION = "six_text_switch"
    CATEGORY = "Endless"

    def six_text_switch(self, Input, text1, text2=None, text3=None, text4=None, text5=None, text6=None):

        if Input == 1:
            return (text1, )
        elif Input == 2:
            return (text2, )
        elif Input == 3:
            return (text3, )
        elif Input == 4:
            return (text4, )
        elif Input == 5:
            return (text5, )			
        else:
            return (text6, )            

#--------------------------------------
##Six Integer Input and Output via connectors

"""
@author: Endless Sea of Stars
@title: Endless-SixIntIO
@nickname: Endless
@description: Six Int Inputs and Output
"""

class EndlessNode_SixIntIOSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {        
                "INT1": ("INT", {"forceInput": True}),               
            },
            "optional": {
                "INT2": ("INT", {"forceInput": True}),
                "INT3": ("INT", {"forceInput": True}),
                "INT4": ("INT", {"forceInput": True}),
                "INT5": ("INT", {"forceInput": True}),
                "INT6": ("INT", {"forceInput": True}),				
            }
        }

    RETURN_TYPES = ("INT","INT","INT","INT","INT","INT",)
    RETURN_NAMES = ("INT1","INT2","INT3","INT4","INT5","INT6",)	
    
    FUNCTION = "six_intIO_switch"
    CATEGORY = "Endless"

    def six_intIO_switch(self, Input, INT1=0, INT2=0, INT3=0, INT4=0, INT5=0, INT6=0):

        if Input == 1:
            return (INT1, )
        elif Input == 2:
            return (INT2, )
        elif Input == 3:
            return (INT3, )
        elif Input == 4:
            return (INT4, )
        elif Input == 5:
            return (INT5, )			
        else:
            return (INT6, )
			
#--------------------------------------
##Six Integer Input and Output by Widget

	

class EndlessNode_SixIntIOWidget:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int1": ("INT", {"default": 0,}),
            },				
            "optional": {				
                "int2": ("INT", {"default": 0,}),
                "int3": ("INT", {"default": 0,}),
                "int4": ("INT", {"default": 0,}),
                "int5": ("INT", {"default": 0,}),
                "int6": ("INT", {"default": 0,}),				
            }
        }
    RETURN_TYPES = ("INT","INT","INT","INT","INT","INT",)
    RETURN_NAMES = ("INT1","INT2","INT3","INT4","INT5","INT6",)		
    FUNCTION = "six_int_widget"

    CATEGORY="Endless"


    def six_int_widget(self,int1,int2,int3,int4,int5,int6):
        return(int1,int2,int3,int4,int5,int6)
			

# FUTURE NODE IDEAS

			
# Dimension Flipper: flip dimensions
# WhatThePrompt: add prompt data to sidecar text file
# ???


#--------------------------------------
# CREDITS
#
# Comfyroll Custom Nodes for the overall node code layout, coding snippets,  and inspiration for the text input and number switches
#
# https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNode
#
# WLSH Nodes for some coding for the Integer Widget
# https://github.com/wallish77/wlsh_nodes
#
# ComfyUI Interface for the basic ideas of what nodes I wanted
#
# https://github.com/comfyanonymous/ComfyUI


