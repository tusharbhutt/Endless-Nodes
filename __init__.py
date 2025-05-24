"""
@author: BiffMunky
@title: Endless ️🌊✨ Nodes
@nickname: ♾️🌊✨
@description: A small set of nodes I created for various numerical and text inputs.  Features image saver with ability to have JSON saved to separate folder, parameter collection nodes, two aesthetic scoring models, switches for text and numbers, and conversion of string to numeric and vice versa.
"""
from .endless_nodes import *

NODE_CLASS_MAPPINGS = {
	"ESS Six Input Text Switch": EndlessNode_SixTextInputSwitch,
	"ESS Eight Input Text Switch": EndlessNode_EightTextInputSwitch,
	"ESS Six Integer IO Switch": EndlessNode_SixIntIOSwitch,
	"ESS Six Integer IO Widget": EndlessNode_SixIntIOWidget,
	# "ESS Six Input Random": EndlessNode_SixTextRandomSwitch,
	# "ESS Eight Input Random": EndlessNode_EightTextRandomSwitch,
	"ESS Six Float Output": EndlessNode_SixFloatOutput,
	"ESS Parameterizer": EndlessNode_XLParameterizer,
	"ESS Global Envoy": EndlessNode_XLGlobalEnvoy,
	"ESS Parameterizer & Prompts": EndlessNode_XLParameterizerPrompt,
	"ESS Combo Parameterizer": EndlessNode_ComboXLParameterizer,
	"ESS Combo Parameterizer & Prompts": EndlessNode_ComboXLParameterizerPrompt,
	"ESS Image Saver with JSON": EndlessNode_ImageSaver,
	"ESS Aesthetic Scoring": EndlessNode_Scoring,
	# "ESS Aesthetic Scoring Auto": EndlessNode_ScoringAutoScore,
	"ESS Image Reward": EndlessNode_ImageReward,
	# "ESS Image Reward Auto": EndlessNode_ImageRewardAutoScore,
	"ESS Float to Integer": EndlessNode_FloattoInt,
	"ESS Float to Number": EndlessNode_FloattoNum,
	"ESS Float to String": EndlessNode_FloattoString,
	"ESS Float to X": EndlessNode_FloattoX,
	"ESS Integer to Float": EndlessNode_InttoFloat,
	"ESS Integer to Number": EndlessNode_InttoNum,
	"ESS Integer to String": EndlessNode_InttoString,
	"ESS Integer to X": EndlessNode_InttoX,
	"ESS Number to Float": EndlessNode_NumtoFloat,
	"ESS Number to Integer": EndlessNode_NumtoInt,
	"ESS Number to String": EndlessNode_NumtoString,
	"ESS Number to X": EndlessNode_NumtoX,
	"ESS String to Float": EndlessNode_StringtoFloat,
	"ESS String to Integer": EndlessNode_StringtoInt,
	"ESS String to Num": EndlessNode_StringtoNum,
	"ESS String to X": EndlessNode_StringtoX,

}

NODE_DISPLAY_NAME_MAPPINGS = {
	"ESS Six Input Text Switch" : "♾️🌊✨ Six Input Text Switch",
	"ESS Eight Input Text Switch": "♾️🌊✨ Eight Input Text Switch",
	"ESS Six Integer IO Switch": "♾️🌊✨ Six Integer IO Switch",
	"ESS Six Integer IO Widget": "♾️🌊✨ Six Integer IO Widget",
	"ESS Six Float Output": "♾️🌊✨ Six Float Output Widget",
	"ESS Parameterizer": "♾️🌊✨ Parameterizer",
	"ESS Global Envoy": "♾️🌊✨ Global Envoy",
	"ESS Parameterizer & Prompts": "♾️🌊✨ Parameterizer & Prompts",
	"ESS Combo Parameterizer": "♾️🌊✨ Combo Parameterizer",
	"ESS Combo Parameterizer & Prompts": "♾️🌊✨ Combo Parameterizer & Prompts",
	"ESS Image Saver with JSON": "♾️🌊✨ Image Saver with JSON",
	"ESS Aesthetic Scoring": "♾️🌊✨ Aesthetic Scoring",
	# "ESS Aesthetic Scoring Auto": "♾️🌊✨ Aesthetic Scoring Auto",
	"ESS Image Reward": "♾️🌊✨ Image Reward",
	# "ESS Image Reward Auto": "♾️🌊✨ Image Reward Auto",
	"ESS Float to Integer": "♾️🌊✨ Float to Integer",
	"ESS Float to Number": "♾️🌊✨ Float to Number",
	"ESS Float to String": "♾️🌊✨ Float to String",
	"ESS Float to X": "♾️🌊✨ Float to X",
	"ESS Integer to Float": "♾️🌊✨ Integer to Float",
	"ESS Integer to Number": "♾️🌊✨ Integer to Number",
	"ESS Integer to String": "♾️🌊✨ Integer to String",
	"ESS Integer to X": "♾️🌊✨ Integer to X",
	"ESS Number to Float": "♾️🌊✨ Number to Float",
	"ESS Number to Integer": "♾️🌊✨ Number to Integer",
	"ESS Number to String": "♾️🌊✨ Number to String",
	"ESS Number to X": "♾️🌊✨ Number to X",
	"ESS String to Float": "♾️🌊✨ String to Float",
	"ESS String to Integer": "♾️🌊✨ String to Integer",
	"ESS String to Num": "♾️🌊✨ String to Num",
	"ESS String to X": "♾️🌊✨ String to X",
 }

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# print("\033[36m An Endless Sea of Stars Custom Nodes V0.41 \033[34m: \033[92m Loaded \033[0m")
