"""
@author: BiffMunky
@title: Endless ️🌊🌠 Node 🌌
@nickname: ♾️🌊🌠
@description: A small set of nodes I created for various numerical and text inputs.  Features switches for text and numbers, parameter collection nodes, and two aesthetic scoring models.
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
	"Endless Nodes Image Save with Text File": EndlessNode_ImageSaver,
	"Endless Nodes Aesthetic Scoring": EndlessNode_Scoring,	
	"Endless Nodes Aesthetic Scoring Auto": EndlessNode_ScoringAutoScore,	
	"Endless Nodes Image Reward": EndlessNode_ImageReward,
	"Endless Nodes Image Reward Auto": EndlessNode_ImageRewardAutoScore,		
	"Endless Nodes Float to Integer": EndlessNode_FloattoInt,
	"Endless Nodes Float to Number": EndlessNode_FloattoNum,
	"Endless Nodes Float to String": EndlessNode_FloattoString,
	"Endless Nodes Number to Float": EndlessNode_NumtoFloat,
	"Endless Nodes Number to Integer": EndlessNode_NumtoInt,	
	"Endless Nodes Number to String": EndlessNode_NumtoString,
	"Endless Nodes Integer to Float": EndlessNode_InttoFloat,
	"Endless Nodes Integer to Number": EndlessNode_InttoNum,	
	"Endless Nodes Integer to String": EndlessNode_InttoString,	
	"Endless Nodes Float to X": EndlessNode_FloattoX,
	"Endless Nodes Integer to X": EndlessNode_InttoX,
	"Endless Nodes Number to X": EndlessNode_NumtoX,
	
	
}

__all__ = ['NODE_CLASS_MAPPINGS']

print("\033[36m 🌌 An Endless Sea of Stars Custom Nodes 🌌 \033[33mreV0.28 \033[34m: \033[92mLoaded\033[0m")