"""
@author: BiffMunky
@title: 🌌 An Endless Sea of Stars Nodes 🌌
@nickname: 🌌 Endless Nodes 🌌
@description: A small set of nodes I created for various numerical and text inputs.  Features switches for text and numbers, parameter collection nodes, and two aesthetic scoring modwls.
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
	#"Endless Nodes Image Save with Text File": EndlessNode_ImageSaver,
	# "Endless Nodes Display String": EndlessNode_DisplayString,
	# "Endless Nodes Display Number": EndlessNode_DisplayNumber,
	# "Endless Nodes Display Integer": EndlessNode_DisplayInt,
	# "Endless Nodes Display Float": EndlessNode_DisplayFloat,
	"Endless Nodes Aesthetic Scoring": EndlessNode_Scoring,	
	"Endless Nodes Image Reward": EndlessNode_ImageReward,	

}

__all__ = ['NODE_CLASS_MAPPINGS']

print("\033[36m 🌌 An Endless Sea of Stars Custom Nodes 🌌 V0.24 \033[34m: \033[92mLoaded\033[0m")