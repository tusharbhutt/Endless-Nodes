"""
@author: BiffMunky
@title: 🌌 An Endless Sea of Stars Node 🌌
@nickname: 🌌 Endless Nodes 🌌
@description: A small set of nodes I created for various numerical and text inputs.  Features switches for text and numbers, parameter collection nodes, and two aesthetic scoring models.
"""

#0.29 - Save Image module added, saves images and JSON to separate folder if requested
#0.28 - Unreleased -  Added Variable types to X
#0.27 - Unreleased - Corrected scoring nodes to actually add the value of the score into the image metadata .... still goobered!
#0.26 - Unreleased - starting to correct scoring to get to image metadata
#0.25 - Added various X to String Nodes
#0.24 - Image reward node added
#0.23 - Aesthetic Scorer added
#0.22 Unreleased - intro'd aestheticscore
#0.21 unreleased -- trying for display nodes
#0.20 sorted categories of nodes

#----------------------------------------------
# Endless Sea of Stars Custom Node Collection
#https://github.com/tusharbhutt/Endless-Nodes
#----------------------------------------------
#
#______________________________________________________________________________________________________________________________________________________________
#				IMPORT MODULES BLOCK				#


from PIL import Image
from PIL.PngImagePlugin import PngInfo
from colorama import init, Fore, Back, Style
from os.path import join
from warnings import filterwarnings
import ImageReward as RM
import clip
import colorama
import datetime
import folder_paths as endless_paths
import io
import json
import math
import numpy as np
import os
import pytorch_lightning as pl
import re
import socket
import statistics
import sys
import time
import torch
import torch.nn as nn


sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

import comfy.sd
import comfy.utils
#import folder_paths
import typing as tg


# Initialize colorama for colored text
colorama.init(autoreset=True)

#______________________________________________________________________________________________________________________________________________________________
#				"SWITCHES" BLOCK				#

#----------------------------------------------
# Six Text Input Node for selection

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
	CATEGORY = "Endless 🌌/Switches"

	def six_text_switch(self, Input, text1=None,text2=None,text3=None,text4=None,text5=None,text6=None):

		if Input == 1:
			return (text1,)
		elif Input == 2:
			return (text2,)
		elif Input == 3:
			return (text3,)
		elif Input == 4:
			return (text4,)
		elif Input == 5:
			return (text5,)
		else:
			return (text6,)

#----------------------------------------------
# Eight Text Input Node for selection (needed more slots, what can I say)


class EndlessNode_EightTextInputSwitch:
	def __init__(self):
		pass

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {
				"Input": ("INT", {"default": 1, "min": 1, "max": 8, "step": 1, "display": "slider"}),	  
#I like the slider idea, it's better for a touch screen
				"text1": ("STRING", {"forceInput": True}),
			},
			"optional": {
				"text2": ("STRING", {"forceInput": True}),
				"text3": ("STRING", {"forceInput": True}),
				"text4": ("STRING", {"forceInput": True}),
				"text5": ("STRING", {"forceInput": True}),
				"text6": ("STRING", {"forceInput": True}),
				"text7": ("STRING", {"forceInput": True}),
				"text8": ("STRING", {"forceInput": True}),
			}
		}

	RETURN_TYPES = ("STRING",)
	RETURN_NAMES = ("Output",)

	FUNCTION = "eight_text_switch"
	CATEGORY = "Endless 🌌/Switches"

	def eight_text_switch(self,Input,text1=None,text2=None,text3=None,text4=None,text5=None,text6=None,text7=None,text8=None,):

		if Input == 1:
			return (text1,)
		elif Input == 2:
			return (text2,)
		elif Input == 3:
			return (text3,)
		elif Input == 4:
			return (text4,)
		elif Input == 5:
			return (text5,)
		elif Input == 6:
			return (text6,)
		elif Input == 7:
			return (text7,)
		else:
			return (text8,)

#----------------------------------------------
# Six Integer Input and Output via connectors


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
	CATEGORY = "Endless 🌌/Switches"

	def six_intIO_switch(self, Input, INT1=0, INT2=0, INT3=0, INT4=0, INT5=0, INT6=0):

		if Input == 1:
			return (INT1,)
		elif Input == 2:
			return (INT2,)
		elif Input == 3:
			return (INT3,)
		elif Input == 4:
			return (INT4,)
		elif Input == 5:
			return (INT5,)
		else:
			return (INT6,)

#----------------------------------------------
# Six Integer Input and Output by Widget

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

	CATEGORY = "Endless 🌌/Switches"


	def six_int_widget(self,int1,int2,int3,int4,int5,int6):
		return(int1,int2,int3,int4,int5,int6)


#______________________________________________________________________________________________________________________________________________________________
#				PARAMETERS  BLOCK				#

#----------------------------------------------
# Text Encode Combo Box with prompt

class EndlessNode_XLParameterizerPrompt: 
	def __init__(self):
		pass

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {
				"base_width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_crop_w": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 8}),
				"base_crop_h": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 8}),
				"base_target_w": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_target_h": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_ascore": ("FLOAT", {"default": 6, "min": 0, "max": 0xffffffffffffffff}),
			},
			"optional": {
				"endlessG": ("STRING", {"default": "TEXT_G,acts as main prompt and connects to refiner text input", "multiline": True}),
				"endlessL": ("STRING", {"default": "TEXT_L, acts as supporting prompt", "multiline": True}),
			}
		}

	RETURN_TYPES = ("INT","INT","INT","INT","INT","INT","INT","INT","FLOAT","STRING","STRING",)
	RETURN_NAMES = ("Base Width","Base Height","Base Cropped Width","Base Cropped Height","Base Target Width","Base Target Height","Refiner Width","Refiner Height","Refiner Aesthetic Score","Text_G/Refiner Prompt","Text_L Prompt",)

	FUNCTION = "ParameterizerPrompt"

	CATEGORY = "Endless 🌌/Parameters"

	def ParameterizerPrompt(self,base_width,base_height,base_crop_w,base_crop_h,base_target_w,base_target_h,refiner_width,refiner_height,refiner_ascore,endlessG,endlessL):
		return(base_width,base_height,base_crop_w,base_crop_h,base_target_w,base_target_h,refiner_width,refiner_height,refiner_ascore,endlessG,endlessL)

#----------------------------------------------
# CLIP text encode box without prompt

class EndlessNode_XLParameterizer:
	def __init__(self):
		pass

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {
				"base_width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_crop_w": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 16}),
				"base_crop_h": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 16}),
				"base_target_w": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_target_h": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_ascore": ("FLOAT", {"default": 6, "min": 0, "max": 0xffffffffffffffff}),
			}
		}
	RETURN_TYPES = ("INT","INT","INT","INT","INT","INT","INT","INT","FLOAT",)
	RETURN_NAMES = ("Base Width","Base Height","Base Cropped Width","Base Cropped Height","Base Target Width","Base Target Height","Refiner Width","Refiner Height","Refiner Aesthetic Score",)
	FUNCTION = "Parameterizer"

	CATEGORY = "Endless 🌌/Parameters"


	def Parameterizer(self,base_width,base_height,base_crop_w,base_crop_h,base_target_w,base_target_h,refiner_width,refiner_height,refiner_ascore):
		return(base_width,base_height,base_crop_w,base_crop_h,base_target_w,base_target_h,refiner_width,refiner_height,refiner_ascore)

#----------------------------------------------
# Text Encode Combo Box with prompt

class EndlessNode_ComboXLParameterizerPrompt: 
	def __init__(self):
		pass

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {
				"base_width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_crop_w": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 16}),
				"base_crop_h": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 16}),
				"base_target_w": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_target_h": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_pascore": ("FLOAT", {"default": 6.5, "min": 0, "max": 0xffffffffffffffff}),
				"refiner_nascore": ("FLOAT", {"default": 2.5, "min": 0, "max": 0xffffffffffffffff}),
			},
			"optional": {
				"PendlessG": ("STRING", {"default": "Positive TEXT_G,acts as main prompt and connects to refiner text input", "multiline": True}),
				"PendlessL": ("STRING", {"default": "Positive TEXT_L, acts as supporting prompt", "multiline": True}),
				"NendlessG": ("STRING", {"default": "Negative TEXT_G, acts as main prompt and connects to refiner text input", "multiline": True}),
				"NendlessL": ("STRING", {"default": "Negative TEXT_L, acts as supporting prompt", "multiline": True}),
			}
		}

	RETURN_TYPES = ("INT","INT","INT","INT","INT","INT","INT","INT","FLOAT","FLOAT","STRING","STRING", "STRING","STRING",)
	RETURN_NAMES = ("Base Width","Base Height","Base Cropped Width","Base Cropped Height","Base Target Width","Base Target Height","Refiner Width","Refiner Height","Positive Refiner Aesthetic Score","Negative Refiner Aesthetic Score","Positive Text_G and Refiner Text Prompt","Postive Text_L Prompt","Negative Text_G and Refiner Text Prompt","Negative Text_L Prompt",)

	FUNCTION = "ComboParameterizerPrompt"

	CATEGORY = "Endless 🌌/Parameters"

	def ComboParameterizerPrompt(self,base_width,base_height,base_crop_w,base_crop_h,base_target_w,base_target_h,refiner_width,refiner_height,refiner_pascore,refiner_nascore,PendlessG,PendlessL,NendlessG,NendlessL):
		return(base_width,base_height,base_crop_w,base_crop_h,base_target_w,base_target_h,refiner_width,refiner_height,refiner_pascore,refiner_nascore,PendlessG,PendlessL,NendlessG,NendlessL)

#----------------------------------------------
# CLIP text encode box without prompt, COMBO that allows one box for both pos/neg parameters to be fed to CLIP text, with separate POS/NEG Aesthetic score

class EndlessNode_ComboXLParameterizer:
	def __init__(self):
		pass

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {
				"base_width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_crop_w": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 16}),
				"base_crop_h": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 16}),
				"base_target_w": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"base_target_h": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 16}),
				"refiner_pascore": ("FLOAT", {"default": 6.5, "min": 0, "max": 0xffffffffffffffff}),
				"refiner_nascore": ("FLOAT", {"default": 2.5, "min": 0, "max": 0xffffffffffffffff}),
			}
		}
	RETURN_TYPES = ("INT","INT","INT","INT","INT","INT","INT","INT","FLOAT","FLOAT")
	RETURN_NAMES = ("Base Width","Base Height","Base Cropped Width","Base Cropped Height","Base Target Width","Base Target Height","Refiner Width","Refiner Height","Positive Refiner Aesthetic Score","Negative Refiner Aesthetic Score",)
	FUNCTION = "ComboParameterizer"

	CATEGORY = "Endless 🌌/Parameters"


	def ComboParameterizer(self,base_width,base_height,base_crop_w,base_crop_h,base_target_w,base_target_h,refiner_width,refiner_height,refiner_pascore, refiner_nascore):
		return(base_width,base_height,base_crop_w,base_crop_h,base_target_w,base_target_h,refiner_width,refiner_height,refiner_pascore, refiner_nascore)

#______________________________________________________________________________________________________________________________________________________________
#				IMAGE SCORING BLOCK				#

#----------------------------------------------
# Aesthetic Scoring Node

folder_paths.folder_names_and_paths["aesthetic"] = ([os.path.join(folder_paths.models_dir,"aesthetic")], folder_paths.supported_pt_extensions)


class MLP(pl.LightningModule):
	def __init__(self, input_size, xcol='emb', ycol='avg_rating'):
		super().__init__()
		self.input_size = input_size
		self.xcol = xcol
		self.ycol = ycol
		self.layers = nn.Sequential(
			nn.Linear(self.input_size, 1024),
			#nn.ReLU(),
			nn.Dropout(0.2),
			nn.Linear(1024, 128),
			#nn.ReLU(),
			nn.Dropout(0.2),
			nn.Linear(128, 64),
			#nn.ReLU(),
			nn.Dropout(0.1),
			nn.Linear(64, 16),
			#nn.ReLU(),
			nn.Linear(16, 1)
		)
	def forward(self, x):
		return self.layers(x)
	def training_step(self, batch, batch_idx):
			x = batch[self.xcol]
			y = batch[self.ycol].reshape(-1, 1)
			x_hat = self.layers(x)
			loss = F.mse_loss(x_hat, y)
			return loss
	def validation_step(self, batch, batch_idx):
		x = batch[self.xcol]
		y = batch[self.ycol].reshape(-1, 1)
		x_hat = self.layers(x)
		loss = F.mse_loss(x_hat, y)
		return loss
	def configure_optimizers(self):
		optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
		return optimizer
def normalized(a, axis=-1, order=2):
	import numpy as np  # pylint: disable=import-outside-toplevel
	l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
	l2[l2 == 0] = 1
	return a / np.expand_dims(l2, axis)


class EndlessNode_Scoring:
	def __init__(self):
		pass

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {
				"model_name": (folder_paths.get_filename_list("aesthetic"), {"multiline": False, "default": "chadscorer.pth"}),
				"image": ("IMAGE",),
				}
		}

	RETURN_TYPES = ("NUMBER","IMAGE")
	FUNCTION = "calc_score"
	CATEGORY = "Endless 🌌/Scoring"

	def calc_score(self, model_name, image):
		m_path = folder_paths.folder_names_and_paths["aesthetic"][0]
		m_path2 = os.path.join(m_path[0], model_name)
		model = MLP(768)  # CLIP embedding dim is 768 for CLIP ViT L 14
		s = torch.load(m_path2)
		model.load_state_dict(s)
		model.to("cuda")
		model.eval()
		device = "cuda" 
		model2, preprocess = clip.load("ViT-L/14", device=device)  # RN50x64
		tensor_image = image[0]
		img = (tensor_image * 255).to(torch.uint8).numpy()
		pil_image = Image.fromarray(img, mode='RGB')
		image2 = preprocess(pil_image).unsqueeze(0).to(device)
		with torch.no_grad():
			image_features = model2.encode_image(image2)
		im_emb_arr = normalized(image_features.cpu().detach().numpy())
		prediction = model(torch.from_numpy(im_emb_arr).to(device).type(torch.cuda.FloatTensor))
		final_prediction = round(float(prediction[0]), 2)
		del model
		return (final_prediction,)

# #---------------------------------------------- NOT WORKING, NEED TO LOOK AT IT
# # Aesthetic Scoring Node with Scoring passed to image

# class EndlessNode_ScoringAutoScore:
	# def __init__(self):
		# pass

	# @classmethod
	# def INPUT_TYPES(cls):
		# return {
			# "required": {
				# "model_name": (folder_paths.get_filename_list("aesthetic"), {"multiline": False, "default": "chadscorer.pth"}),
				# "image": ("IMAGE",),
				# }
		# }

	# RETURN_TYPES = ("NUMBER","IMAGE")
	# FUNCTION = "calc_score"
	# OUTPUT_NODE = True
	# CATEGORY = "Endless 🌌/Scoring"

	# def calc_score(self, model_name, image):
		# m_path = folder_paths.folder_names_and_paths["aesthetic"][0]
		# m_path2 = os.path.join(m_path[0], model_name)
		# model = MLP(768)  # CLIP embedding dim is 768 for CLIP ViT L 14
		# s = torch.load(m_path2)
		# model.load_state_dict(s)
		# model.to("cuda")
		# model.eval()
		# device = "cuda" 
		# model2, preprocess = clip.load("ViT-L/14", device=device)  # RN50x64
		# tensor_image = image[0]
		# img = (tensor_image * 255).to(torch.uint8).numpy()
		# pil_image = Image.fromarray(img, mode='RGB')
		# image2 = preprocess(pil_image).unsqueeze(0).to(device)
		# with torch.no_grad():
			# image_features = model2.encode_image(image2)
		# im_emb_arr = normalized(image_features.cpu().detach().numpy())
		# prediction = model(torch.from_numpy(im_emb_arr).to(device).type(torch.cuda.FloatTensor))
		# final_prediction = round(float(prediction[0]), 2)
		# del model
		# # Metadata part
		# extra_pnginfo = {"SCORE": str(final_prediction)}
		# return (final_prediction, image)

#----------------------------------------------
# Image Reward Scoring

class EndlessNode_ImageReward:
	def __init__(self):
		self.model = None

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {
				"model": ("STRING", {"multiline": False, "default": "ImageReward-v1.0"}),
				"prompt": ("STRING", {"multiline": True, "forceInput": True}),
				"images": ("IMAGE",),
			},
		}

	RETURN_TYPES = ("FLOAT", "STRING", "FLOAT", "STRING")
	RETURN_NAMES = ("SCORE_FLOAT", "SCORE_STRING", "VALUE_FLOAT", "VALUE_STRING")

	CATEGORY = "Endless 🌌/Scoring"

	FUNCTION = "process_images"

	def process_images(self, model, prompt, images,): #rounded):
		if self.model is None:
			self.model = RM.load(model)

		score = 0.0
		for image in images:
			# convert to PIL image
			i = 255.0 * image.cpu().numpy()
			img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
			score += self.model.score(prompt, [img])
		score /= len(images)
		# assume std dev follows normal distribution curve
		valuescale = 0.5 * (1 + math.erf(score / math.sqrt(2))) * 10  # *10 to get a value between -10
		return (score, str(score), valuescale, str(valuescale))
	

# #---------------------------------------------- NOT WORKING, NEED TO LOOK AT
# # Image Reward Scoring with score passed to image

# class EndlessNode_ImageRewardAutoScore:
	# def __init__(self):
		# self.model = None

	# @classmethod
	# def INPUT_TYPES(cls):
		# return {
			# "required": {
				# "model": ("STRING", {"multiline": False, "default": "ImageReward-v1.0"}),
				# "prompt": ("STRING", {"multiline": True, "forceInput": True}),
				# "images": ("IMAGE",),
			# },
		# }

	# RETURN_TYPES = ("FLOAT", "STRING", "FLOAT", "STRING", "IMAGE")
	# RETURN_NAMES = ("SCORE_FLOAT", "SCORE_STRING", "VALUE_FLOAT", "VALUE_STRING", "TO_IMAGE")
	# OUTPUT_NODE = True

	# CATEGORY = "Endless 🌌/Scoring"

	# FUNCTION = "score_meta"

	# def score_meta(self, model, prompt, images):
		# if self.model is None:
			# self.model = RM.load(model)

		# # Scoring part
		# score = 0.0
		# for image in images:
			# i = 255.0 * image.cpu().numpy()
			# img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
			# score += self.model.score(prompt, [img])
		# score /= len(images)
		# valuescale = 0.5 * (1 + math.erf(score / math.sqrt(2))) * 10

		# # Metadata part
		# extra_pnginfo = {"SCORE": str(score)}

		# # Returning both the score and the modified image
		# return (score, str(score), valuescale, str(valuescale), images)

# ______________________________________________________________________________________________________________________________________________________________
				# IMAGE SAVERS BLOCK				#

# ----------------------------------------------
# Saver type one: saves IMAGE and JSON files, can specify separate folders for each, or one, or none, and use Python timestamps


class EndlessNode_ImageSaver:
	def __init__(self):
		self.output_dir = endless_paths.get_output_directory()
		self.type = "output"

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {
				"images": ("IMAGE",),
				"filename_prefix": ("STRING", {"default": "ComfyUI"}),
				"delimiter": ("STRING", {"default": "_"}),
				"filename_number_padding": ("INT", {"default": 4, "min": 1, "max": 9, "step": 1}),
				"filename_number_start": (["false", "true"],),
				"img_folder": ("STRING", {"default": None}),
				"json_folder": ("STRING", {"default": None}),
			},
			"hidden": {
				"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"
			},
		}
	RETURN_TYPES = ()
	FUNCTION = "save_images"
	OUTPUT_NODE = True
	CATEGORY = "Endless 🌌/IO"

	def save_images(self, images, filename_prefix="ComfyUI", delimiter="_",
					filename_number_padding=4, filename_number_start='false',
					img_folder=None, json_folder=None, prompt=None, extra_pnginfo=None):

		# Replace illegal characters in the filename prefix with dashes
		filename_prefix = re.sub(r'[<>:"\/\\|?*]', '-', filename_prefix)

		# Set IMG Extension
		img_extension = '.png'

		counter = 1

		results = list()

		for image in images:
			i = 255. * image.cpu().numpy()
			img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

			metadata = PngInfo()
			if prompt is not None:
				metadata.add_text("prompt", json.dumps(prompt))
			if extra_pnginfo is not None:
				for x in extra_pnginfo:
					metadata.add_text(x, json.dumps(extra_pnginfo[x]))

			img_file, json_file = self.generate_filenames(filename_prefix, delimiter, counter,filename_number_padding, filename_number_start,img_extension, img_folder, json_folder)

			try:
				if img_extension == '.png':
					img.save(img_file, pnginfo=metadata, compress_level=4)
				elif img_extension == '.jpeg':
					img.save(img_file, quality=100, optimize=True)

				with open(json_file, 'w', encoding='utf-8', newline='\n') as f:
					if prompt is not None:
						f.write(json.dumps(prompt, indent=4))

				print(Fore.GREEN + f"+ File(s) saved to: {img_file}")

				results.append({
					"image_filename": os.path.basename(img_file),
					"image_path": img_file,
					"json_filename": os.path.basename(json_file),
					"text_path": json_file,
					"type": self.type
				})

			except OSError as e:
				print(Fore.RED + " + Unable to save file: ", end='')
				print({img_file})
				print(e)
			except Exception as e:
				print(Fore.RED + " + Unable to save file due to the following error: ", end='')
				print(e)

			counter += 1

		return {"ui": {"results": results}}

	def generate_filenames(self, filename_prefix, delimiter, counter, filename_number_padding, filename_number_start, img_extension, img_folder, json_folder):
		if filename_number_start == 'true':
			img_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}{img_extension}"
			json_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}.json"
		else:
			img_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}{img_extension}"
			json_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}.json"

		# Construct full paths for image and text files based on folders provided

		if img_folder:
			img_folder = self.replace_date_time_placeholders(img_folder)		
			os.makedirs(img_folder, exist_ok=True)  # Create the image folder if it doesn't exist
			img_file = os.path.join(img_folder, img_file)
		else:
			img_file = os.path.join(self.output_dir, img_file)

		if json_folder:
			json_folder = self.replace_date_time_placeholders(json_folder)
			os.makedirs(json_folder, exist_ok=True)  # Create the image folder if it doesn't exist
			json_file = os.path.join(json_folder, json_file)
		else:
			json_file = os.path.join(os.path.dirname(img_file), json_file)
			
		# Apply placeholders for date and time in filenames and folder
		img_file = self.replace_date_time_placeholders(img_file)
		json_file = self.replace_date_time_placeholders(json_file)



		# Check if files with the same name exist, increment counter if necessary
		while os.path.exists(img_file) or os.path.exists(json_file):
			counter += 1
			if filename_number_start == 'true':
				img_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}{img_extension}"
				json_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}.json"
			else:
				img_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}{img_extension}"
				json_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}.json"

		# Construct full paths for image and text files based on folders provided

		if img_folder:
			img_folder = self.replace_date_time_placeholders(img_folder)
			os.makedirs(img_folder, exist_ok=True)  # Create the image folder if it doesn't exist
			img_file = os.path.join(img_folder, img_file)
		else:
			img_file = os.path.join(self.output_dir, img_file)

		if json_folder:
			json_folder = self.replace_date_time_placeholders(json_folder)
			os.makedirs(json_folder, exist_ok=True)  # Create the image folder if it doesn't exist
			json_file = os.path.join(json_folder, json_file)
		else:
			json_file = os.path.join(os.path.dirname(img_file), json_file)
			
		# Apply placeholders for date and time in filenames and folder
		img_file = self.replace_date_time_placeholders(img_file)
		json_file = self.replace_date_time_placeholders(json_file)

		return img_file, json_file

	def replace_date_time_placeholders(self, filename):
		# Replace date and time placeholders with actual date and time strings
		now = datetime.datetime.now()
		placeholders = {
			'%Y': now.strftime('%Y'),  # Year with century as a decimal number
			'%y': now.strftime('%y'),  # Year without century as a zero-padded decimal number
			'%m': now.strftime('%m'),  # Month as a zero-padded decimal number
			'%d': now.strftime('%d'),  # Day of the month as a zero-padded decimal number
			'%H': now.strftime('%H'),  # Hour (24-hour clock) as a zero-padded decimal number
			'%M': now.strftime('%M'),  # Minute as a zero-padded decimal number
			'%S': now.strftime('%S'),  # Second as a zero-padded decimal number
		}

		for placeholder, replacement in placeholders.items():
			filename = filename.replace(placeholder, replacement)

		return filename
# ______________________________________________________________________________________________________________________________________________________________
				# CONVERTER NODES BLOCK				#

# ----------------------------------------------
# Float value to Integer

class EndlessNode_FloattoInt:
	CATEGORY = "Endless 🌌/Converters"

	def __init__(self):
		pass	
		
	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {"FloatValue": ("FLOAT", {"default": 0.0},)}
		}

	RETURN_TYPES = ("INT",) 
	FUNCTION = "inputfloat"

	def inputfloat(self, FloatValue):
		return int(FloatValue,)


# ----------------------------------------------
# Float value to Number, passes minimum one decimal
# There is no real "Number" function in Python, this is here so that nodes that need a NUMBER can take the FLOAT value

class EndlessNode_FloattoNum:
	CATEGORY = "Endless 🌌/Converters"

	def __init__(self):
		pass	
		
	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {"FloatValue": ("FLOAT", {"default": 0.0,}),}
		}

	RETURN_TYPES = ("NUMBER",) 
	FUNCTION = "inputfloat"

	def inputfloat(self, FloatValue):
		return float(FloatValue,)


# ----------------------------------------------
# Float value to String, passes one to eight decimals

class EndlessNode_FloattoString:
	CATEGORY = "Endless 🌌/Converters"

	def __init__(self):
		pass	
		
	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {"FloatValue": ("FLOAT", {"default": 0.0,},)}
		}

	RETURN_TYPES = ("STRING",) 
	FUNCTION = "inputfloat"

	def inputfloat(self, FloatValue):
		if isinstance(FloatValue, float):
			formatted_value = f'{FloatValue:.1f}' if FloatValue.is_integer() else f'{FloatValue:.8f}'
			return str((formatted_value),)
		elif isinstance(FloatValue, int):
			#Convert integer to float and then format
			formatted_value = f'{float(FloatValue):.1f}'
			return str((formatted_value),)
		else:
			try:
				#Try to convert to float, and then format
				float_value = float(FloatValue)
				formatted_value = f'{float_value:.1f}' if float_value.is_integer() else f'{float_value:.8f}'
				return str((formatted_value),)
			except ValueError:
				return ("Not a valid float",)


# # ---------------------------------------------- NEED TO FIX
# # Float value to X

# class EndlessNode_FloattoX:
	# CATEGORY = "Endless 🌌/Converters"

	# def __init__(self):
		# pass

	# @classmethod
	# def INPUT_TYPES(cls):
		# return {
			# "required": {
				# "FloatValue": ("FLOAT", {"default": 0, "min": -8675309362436420, "max": 8675309362436420}),
			# },
		# }

	# RETURN_TYPES = ("INT", "NUMBER", "STR")
	# FUNCTION = "return_constant_number"

	# def return_constant_number(self, FloatValue):

		# # Return number
		# return (int(FloatValue), (FloatValue), str(FloatValue))


# ----------------------------------------------
# Integer to Float

class EndlessNode_InttoFloat:
	CATEGORY = "Endless 🌌/Converters"
	def __init__(self):
		pass	

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {"IntegerValue": ("INT",),}
		}

	RETURN_TYPES = ("FLOAT",) 
	FUNCTION = "inputint"

	def inputint(self, IntegerValue):
		return int((IntegerValue),)
		
		
# ----------------------------------------------
# Integer to Number

class EndlessNode_InttoNum:
	CATEGORY = "Endless 🌌/Converters"
	def __init__(self):
		pass	

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {"IntegerValue": ("INT",),}
		}

	RETURN_TYPES = ("NUMBER",) 
	FUNCTION = "inputint"

	def inputint(self, IntegerValue):
		return int((IntegerValue),)
		

# ----------------------------------------------
# Integer to String

class EndlessNode_InttoString:
	CATEGORY = "Endless 🌌/Converters"

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {"IntegerValue": ("INT",{"default": 0,},)}
		}
	RETURN_TYPES = ("STRING",)
	FUNCTION = "inputint"

	def inputint(self, IntegerValue):
		return str((IntegerValue),)

# # ---------------------------------------------- NOT ORKING, NEED TO FIX
# # Integer value to X

# class EndlessNode_InttoX:
	# CATEGORY = "Endless 🌌/Converters"

	# def __init__(self):
		# pass

	# @classmethod
	# def INPUT_TYPES(cls):
		# return {
			# "required": {
				# "number": ("INT", {"default": 0, "min": -8675309, "max": 8675309}),
			# },
		# }

	# RETURN_TYPES = ("FLOAT", "NUMBER", "STR")
	# FUNCTION = "return_constant_number"

	# def return_constant_number(self, number):

		# # Return number
		# return (float(number), float(number), str(number))


# ----------------------------------------------
# Number to Float

class EndlessNode_NumtoFloat:
	CATEGORY = "Endless 🌌/Converters"
	
	def __init__(self):
		pass	

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {"NumberValue": ("NUMBER",),}
		}

	RETURN_TYPES = ("FLOAT",) 
	FUNCTION = "inputnum"

	def inputnum(self, NumberValue):
		return float((NumberValue),)
		
		
# ----------------------------------------------
# Number to Integer

class EndlessNode_NumtoInt:
	CATEGORY = "Endless 🌌/Converters"
	def __init__(self):
		pass	

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {"NumberValue": ("NUMBER",),}
		}
	RETURN_TYPES = ("INT",) 
	FUNCTION = "inputnum"

	def inputnum(self, NumberValue):
		return int((NumberValue),)

# ----------------------------------------------
# Number value to String

class EndlessNode_NumtoString:
	def __init__(self):
		pass
	CATEGORY = "Endless 🌌/Converters"

	@classmethod
	def INPUT_TYPES(cls):
		return {
			"required": {"NumberValue": ("NUMBER",),}
		}
	RETURN_TYPES = ("STRING",)
	FUNCTION = "inputnum"

	def inputnum(self, NumberValue):
		return str((NumberValue),)

# NEED TO FIX STILL 
# class EndlessNode_NumtoX:
	# CATEGORY = "Endless 🌌/Converters"

	# def __init__(self):
		# pass

	# @classmethod
	# def INPUT_TYPES(cls):
		# return {
			# "required": {
				# "number": ("FLOAT", {"default": 0, "min": -8675309362436420, "max": 8675309362436420}),
			# },
		# }

	# RETURN_TYPES = ("FLOAT", "INT", "STR")
	# FUNCTION = "return_constant_number"

	# def return_constant_number(self, number):

		# # Return number
		# return (float(number), int(number), str(number))


#______________________________________________________________________________________________________________________________________________________________
#				CREDITS				#

#
# Comfyroll Custom Nodes for the initial node code layout, coding snippets, and inspiration for the text input and number switches
#
# https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNode
#
# WLSH Nodes for some coding for the Integer Widget
# https://github.com/wallish77/wlsh_nodes
#
# ComfyUI Interface for the basic ideas of what nodes I wanted
#
# https://github.com/comfyanonymous/ComfyUI
#
# ComfyUI-Strimmlarns-Aesthetic-Score for the original coding for Aesthetic Scoring
#
# https://github.com/strimmlarn/ComfyUI-Strimmlarns-Aesthetic-Score
#
# The scorer uses the MLP class code from Christoph Schuhmann
# 
#https://github.com/christophschuhmann/improved-aesthetic-predictor
#[Zane A's ComfyUI-ImageReward](https://github.com/ZaneA/ComfyUI-ImageReward) for the original coding for the Image Reward node
#
#Zane's node in turn uses [ImageReward](https://github.com/THUDM/ImageReward)  
#
#
#Mikey nodes to grab code snippet to pass scoring metadata to image
#
#https://github.com/bash-j/mikey_nodes

# Took some base code from the WAS save image node to repurpose it
#
#https://github.com/WASasquatch/was-node-suite-comfyui
#--------------------------------------


########################################################################################  CELLAR DWELLERS


