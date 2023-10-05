"""
@author: BiffMunky
@title: Endless ️🌊✨ Nodes
@nickname: ♾️🌊✨
@description: A small set of nodes I created for various numerical and text inputs.  Features image saver with ability to have JSON saved to separate folder, parameter collection nodes, two aesthetic scoring models, switches for text and numbers, and conversion of string to numeric and vice versa.
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
	"Endless Nodes Image Saver with JSON": EndlessNode_ImageSaver,
	"Endless Nodes Aesthetic Scoring": EndlessNode_Scoring,	
#	"Endless Nodes Aesthetic Scoring Auto": EndlessNode_ScoringAutoScore,	
	"Endless Nodes Image Reward": EndlessNode_ImageReward,
#	"Endless Nodes Image Reward Auto": EndlessNode_ImageRewardAutoScore,		
	"Endless Nodes Float to Integer": EndlessNode_FloattoInt,
	"Endless Nodes Float to Number": EndlessNode_FloattoNum,
	"Endless Nodes Float to String": EndlessNode_FloattoString,
	"Endless Nodes Float to X": EndlessNode_FloattoX,
	"Endless Nodes Integer to Float": EndlessNode_InttoFloat,
	"Endless Nodes Integer to Number": EndlessNode_InttoNum,	
	"Endless Nodes Integer to String": EndlessNode_InttoString,	
	"Endless Nodes Integer to X": EndlessNode_InttoX,	
	"Endless Nodes Number to Float": EndlessNode_NumtoFloat,
	"Endless Nodes Number to Integer": EndlessNode_NumtoInt,	
	"Endless Nodes Number to String": EndlessNode_NumtoString,
	"Endless Nodes Number to X": EndlessNode_NumtoX,
	"Endless Nodes String to Float": EndlessNode_StringtoFloat,
	"Endless Nodes String to Integer": EndlessNode_StringtoInt,	
	"Endless Nodes String to Num": EndlessNode_StringtoNum,
	"Endless Nodes String to X": EndlessNode_StringtoX,
}

NODE_DISPLAY_NAME_MAPPINGS = {
	"Endless Nodes Six Input Text Switch" : "Endless 🌊✨ Six Input Text Switch",
	"Endless Nodes Eight Input Text Switch": "Endless 🌊✨ Eight Input Text Switch",
	"Endless Nodes Six Integer IO Switch": "Endless 🌊✨ Six Integer IO Switch",
	"Endless Nodes Six Integer IO Widget": "Endless 🌊✨ Six Integer IO Widget",
	"Endless Nodes Parameterizer": "Endless 🌊✨ Parameterizer",
	"Endless Nodes Parameterizer & Prompts": "Endless 🌊✨ Parameterizer & Prompts",
	"Endless Nodes Combo Parameterizer": "Endless 🌊✨ Combo Parameterizer",
	"Endless Nodes Combo Parameterizer & Prompts": "Endless 🌊✨ Combo Parameterizer & Prompts",
	"Endless Nodes Image Saver with JSON": "Endless 🌊✨ Image Saver with JSON",
	"Endless Nodes Aesthetic Scoring": "Endless 🌊✨ Aesthetic Scoring",
#	"Endless Nodes Aesthetic Scoring Auto": "Endless 🌊✨ Aesthetic Scoring Auto",
	"Endless Nodes Image Reward": "Endless 🌊✨ Image Reward",
#	"Endless Nodes Image Reward Auto": "Endless 🌊✨ Image Reward Auto",
	"Endless Nodes Float to Integer": "Endless 🌊✨ Float to Integer",
	"Endless Nodes Float to Number": "Endless 🌊✨ Float to Number",
	"Endless Nodes Float to String": "Endless 🌊✨ Float to String",
	"Endless Nodes Float to X": "Endless 🌊✨ Float to X",
	"Endless Nodes Integer to Float": "Endless 🌊✨ Integer to Float",
	"Endless Nodes Integer to Number": "Endless 🌊✨ Integer to Number",
	"Endless Nodes Integer to String": "Endless 🌊✨ Integer to String",
	"Endless Nodes Integer to X": "Endless 🌊✨ Integer to X",
	"Endless Nodes Number to Float": "Endless 🌊✨ Number to Float",
	"Endless Nodes Number to Integer": "Endless 🌊✨ Number to Integer",
	"Endless Nodes Number to String": "Endless 🌊✨ Number to String",
	"Endless Nodes Number to X": "Endless 🌊✨ Number to X",
	"Endless Nodes String to Float": "Endless 🌊✨ String to Float",
	"Endless Nodes String to Integer": "Endless 🌊✨ String to Integer",
	"Endless Nodes String to Num": "Endless 🌊✨ String to Num",
	"Endless Nodes String to X": "Endless 🌊✨ String to X",
 }
#Heh, doesn't seem to work :(

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
 
print("\033[36m An Endless Sea of Stars Custom Nodes V0.31 \033[34m: \033[92mLoaded\033[0m")