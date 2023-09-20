"""
@author: Endless Sea of Stars
@title: Endless Nodes
@nickname: Endless Nodes
@description: A small set of nodes I created for various numerical and text inputs.
"""
from .endless_nodes import *

NODE_CLASS_MAPPINGS = {
    "Endless Nodes Six Input Text Switch": EndlessNode_SixTextInputSwitch,
    "Endless Nodes Eight Input Text Switch": EndlessNode_EightTextInputSwitch,	
    "Endless Nodes Six Integer IO Switch": EndlessNode_SixIntIOSwitch,
    "Endless Nodes Six Integer IO Widget": EndlessNode_SixIntIOWidget,
	"Endless Nodes Parameterizer": EndlessNode_XLParameterizer,
	"Endless Nodes Parameterizer & Prompts": EndlessNode_XLParameterizerPrompt,	
	"Endless Nodes Combo Parameterizer": EndlessNode_ComboXLParameterizer,
	"Endless Nodes Combo Parameterizer & Prompts": EndlessNode_ComboXLParameterizerPrompt,
}

__all__ = ['NODE_CLASS_MAPPINGS']

print("\033[34mEndelssSeaofStars Custom Nodes: \033[92mLoaded\033[0m")
