import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import colorama
from colorama import init, Fore, Back, Style
import os
import json
import time
import socket
import re
import folder_paths
import datetime  # Added to support date and time placeholders

# Initialize colorama
colorama.init(autoreset=True)

class EndlessNode_ImageSaver:
	def __init__(self):
		self.output_dir = folder_paths.get_output_directory()
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
				"image_folder": ("STRING", {"default": ""}),
				"json_folder": ("STRING", {"default": ""}),
			},
			"hidden": {
				"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"
			},
		}

	RETURN_TYPES = ()
	FUNCTION = "save_images"
	OUTPUT_NODE = True
	CATEGORY = "Endless 🌊✨/IO"

	def save_images(self, images, filename_prefix="ComfyUI", delimiter="_",
					filename_number_padding=4, filename_number_start='false',
					image_folder=None, json_folder=None, prompt=None, extra_pnginfo=None):

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

			img_file, json_file = self.generate_filenames(filename_prefix, delimiter, counter,
														 filename_number_padding, filename_number_start,
														 img_extension, image_folder, json_folder)

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
					"json_path": json_file,
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

	def generate_filenames(self, filename_prefix, delimiter, counter,
						   filename_number_padding, filename_number_start, img_extension,
						   image_folder, json_folder):
		if filename_number_start == 'true':
			img_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}{img_extension}"
			json_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}.json"
		else:
			img_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}{img_extension}"
			json_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}.json"

		# Apply placeholders for date and time in filenames
		img_file = self.replace_date_time_placeholders(img_file)
		json_file = self.replace_date_time_placeholders(json_file)

		# Construct full paths for image and text files based on folders provided
		if image_folder:
			img_file = os.path.join(image_folder, img_file)
		else:
			img_file = os.path.join(self.output_dir, img_file)

		if json_folder:
			json_file = os.path.join(json_folder, json_file)
		else:
			json_file = os.path.join(os.path.dirname(img_file), json_file)

		# Check if files with the same name exist, increment counter if necessary
		while os.path.exists(img_file) or os.path.exists(json_file):
			counter += 1
			if filename_number_start == 'true':
				img_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}{img_extension}"
				json_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}.json"
			else:
				img_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}{img_extension}"
				json_file = f"{filename_prefix}{delimiter}{counter:0{filename_number_padding}}.json"

			# Apply placeholders for date and time in filenames
			img_file = self.replace_date_time_placeholders(img_file)
			json_file = self.replace_date_time_placeholders(json_file)

			if image_folder:
				img_file = os.path.join(image_folder, img_file)
			else:
				img_file = os.path.join(self.output_dir, img_file)

			if json_folder:
				json_file = os.path.join(json_folder, json_file)
			else:
				json_file = os.path.join(os.path.dirname(img_file), json_file)

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

NODE_CLASS_MAPPINGS = {
	"♾️🌊✨ Image Saver with JSON": EndlessNode_ImageSaver
}
