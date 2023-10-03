# Endless-Nodes
Some basic custom nodes for the ComfyUI user interface for Stable Diffusion.  Features:

+ An image saver for images and JSON files to base folder, custom folders for one, or custom folders for both.  Also allows for Python timestamping
+ Two aesthetic scoring models, one based on the same as AUTO1111, the other based on Image Reward
+ Converters for various numerical functions to the other (int, float, number) and to strings.  Still in beta
+ Switches for text and numbers
+ Parameter collection nodes
+ MORE TO COME 

When using the [ComfyUI](https://github.com/comfyanonymous/ComfyUI) interface for [Stable Diffusion](https://github.com/Stability-AI/stablediffusion), I sometimes find that the standard nodes and the many, many, many custom nodes out there don't work the way I want them to, or how I think they do.

Rightly or wrongly, I am pretending to teach myself a bit of Python to get some nodes up and running to do what I'd like.  There are no promises that these nodes will work for you or that I will maintain them.  Feel free to do with them as you wish, according to the license model.

**UPDATE: Oct 3, 2023**

+ Added an Image Saver that can place JSON files ***in separate folders***
+ Added nodes to convert from one numeric type to another, and to string.  **Still in beta**

**UPDATE: Sep 24, 2023**

+ Took the node from https://github.com/ZaneA/ComfyUI-ImageReward that uses Image Reward and repurposed it
+ Took the node from https://github.com/strimmlarn that does aesthetic scoring and repurposed it

**UPDATE: Sep 20, 2023**

+ Added an eight-input number switch because I needed it

**UPDATE: Sep 18, 2023**

+ Added the Endless Nodes Parameterizer with Text_G and Text_L prompt box
+ Added the Parameterizer with a_score for both pos/neg
+ Added the Parameterizer with a_score for both pos/neg and Text_G and Text_L prompt box
+ Fixed some typos


**UPDATE: Sep 17, 2023**

+ Added the Endless Nodes Parameterizer


## Install and Requirements 

Navigate to your /ComfyUI/custom_nodes/ folder 

In Windows, you can then right-click to start a command prompt and type:

`git clone https://github.com/tusharbhutt/Endless-Nodes`

You can also get the nodes via the [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)

**NOTE: Requires CLIP and Pytorch-Lightning for the Aesthetic Scorer and ImageReward for my take on the Image Reward node scorer.  I've added them in the requirement file but if it doesn't work, you will need to download manually**

## Node List

## Endless Image Saver

This is why I tried my hand ay Python in the first place!  There are many, many, many, good image saver nodes out there, so why one more? Well:

+ The default saver does not save to UNC in Windows
+ Some savers will allow you to save to UNC but have built-in folder formats
+ You can cobble some savers to save an image together with a text file, but the timestamp on the text file tends to be 2-3 seconds off from the image
+ No saver I know of lets you save the JSON file to a completely different folder

So… this node will allow you to save your image file wherever you want, with full support for standard [Python date and time conventions]( https://docs.python.org/2/library/time.html#time.sleep),  and you can save the JSON file somewhere else. 

I have more plans for this, but it’s ready for release now.

![imagesaver](./img/imagesaverone.png)


Does it work... ?


![imagesaverfile](./img/imagesaverfile.png)

See, it works!

## Aesthetic Scorer

This node will output a predicted aesthetic score as a number and display it with the appropriate node (e.g., rgthree's ["Any"](https://github.com/rgthree/rgthree-comfy#display-any) node).  I took the node from https://github.com/strimmlarn that does aesthetic scoring and repurposed it so that it is simpler and outputs the score as a number.  I combined the model loader and score calculator into one, and removed the Aesthetic Score Sorter.  

![aestheticone](./img/aestheticone.png)

You can load a number of scoring models, I use the "chadscorer" model found here:

https://github.com/grexzen/SD-Chad/blob/main/chadscorer.pth

As for the original node from strimmlarn, please refer to this GitHub if you would like to examine it:

https://github.com/strimmlarn/ComfyUI-Strimmlarns-Aesthetic-Score

The scorer adds about 7-10 seconds to a workflow on my Nvidia 3060 12 GB card, your mileage may vary

## Image Reward

This node will output a predicted aesthetic score as a number and display it with the appropriate node (e.g., rgthree's ["Any"](https://github.com/rgthree/rgthree-comfy#display-any) node).  I took the node from https://github.com/ZaneA/ComfyUI-ImageReward that in turn scores images using [ImageReward](https://github.com/THUDM/ImageReward).   I combined the model loader and score calculator into one and added output nodes for both the standard deviation calculation (which is what Zane's node does) and the score on a scale of one to ten based on some simple statistic calculations.

The difference between this node and the Aesthetics Scorer is that the underlying ImageReward is based on Reward Feedback Learning (ReFL) and uses 137K input samples that were scored by humans.  It often scores much lower than the Aesthetics Scorer, but not always!

![imagereward](./img/imagereward.png)

As with the Aesthetics Scorer, the Image Reward node adds about 7-10 seconds to a workflow on my Nvidia 3060 12 GB card, your mileage may vary.  

For added GPU cycle time consumption, put them both in and watch how often they vehemently disagree with the scoring :)

![disagree](./img/disagree.png)


### Endless Node Parameterizer 

This node has a collection of inputs for the CLIP text Encoder and Refiners for SDXL based workflows

Inputs include:

- base width: set width for the base encoder
- base height: set height for the base encoder
- base cropped width: crop width for the base encoder
- base cropped height: crop height for the base encoder
- base target width: target width for the base encoder
- base target height: target height for the base encoder
- refiner width: crop width for the refiner if you have included one
- refiner height: crop height for the refiner if you have included one
- refiner aesthetic score: set the score value for the refiner

You can set up two of these one for the positive and one for the negative prompt

![parameterizer](./img/parameterizer.png)

## Parameterizer with prompt

As above, but with TEXT_G and TEXT_L  outputs

![parameterizerprompt](./img/parameterizerprompt.png)

## COMBO Parameterizer with and without prompt

After making the Parameterizer, I realized having two separate ones for both the positive and negative CLIP encoders is not optimal, because almost everyone will use the same resolution for both the positive and negative base and refiners.  However, you may (well, you *should…*) want separate aesthetic scorers for the positive and negative CLIPs, so I came up with one that does this for you.  Also comes in a variant that has the prompt boxes for you.

![comboparameterizer](./img/comboparameterizer.png)

![comboparameterizerprompt](./img/comboparameterizerprompt.png)

### Six Text Input Switch
Allows the user to select between six text inputs and uses a slider to make the selection.  Useful for multiple inputs for prompt creation


![sixtext](./img/sixtext.png)

**NOT SHOWN: There is an eight input variant now too, as of Sep 20, 2023**

### Six Integer Input to Six Integer Output
I've seen a fair number of 3-, 4-, or more X-way text input and outputs, I wanted to do something for numbers as well.  Use it as you wish.


![sixintconnect](./img/sixintconnect.png)


### Six Integer Widget
As above, but with widgets for entry instead of connectors

![sixintwidget](./img/sixintwidget.png)

### Various converters

You've seen them elsewhere too, but there are few that do X to float or vice versa, so I threw them in.  *Still in beta*, sometimes they work, other times the downstream node complains.

![converters](./img/converters.png)


## Usage License and Restrictions

See GPL Licensing V3 for usage.  You may modify this code as long as you keep the credits for this repository and for those noted in the credit section below.  **YOU ARE EXPRESSLY FORBIDDEN FROM USING THIS NODE TO CREATE ANY IMAGES OR ARTWORK THAT VIOLATES THE STABLE DIFFUSION USAGE NOTES [HERE](https://huggingface.co/stabilityai/stable-diffusion-2#misuse-malicious-use-and-out-of-scope-use) AND [HERE](https://huggingface.co/stabilityai/stable-diffusion-2#misuse-and-malicious-use).**

For example, don't be a mouth-breather who creates fake celebrity nudes or sexual content of **anyone, even if you have their consent**.  JUST. DON’T. BE. A. DICK/BITCH.

The author expressly disclaims any liability for any images you create using these nodes.

## Disclaimer

These nodes may or may not be maintained.  They work on my system but may not on yours.  

## Credits

+[Comfyroll Custom Nodes](https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNode) for the overall node code layout, coding snippets,  and inspiration for the text input and number switches.

+[WLSH Nodes](https://github.com/wallish77/wlsh_nodes) for some coding for the Integer Widget.

+[ComfyUI](https://github.com/comfyanonymous/ComfyUI) Interface for the basic ideas of what nodes I wanted.

+[ComfyUI-Strimmlarns-Aesthetic-Score](https://github.com/strimmlarn/ComfyUI-Strimmlarns-Aesthetic-Score) for the original coding for the Aesthetic Scorer.  The original scorer, and therefore my derivative too, use the [MLP class code](https://github.com/christophschuhmann/improved-aesthetic-predictor) from Christoph Schuhmann

+[Zane A's ComfyUI-ImageReward](https://github.com/ZaneA/ComfyUI-ImageReward) for the original coding for the Image Reward node.  Zane's node in turn uses [ImageReward](https://github.com/THUDM/ImageReward)  

+[Mikey nodes](https://github.com/bash-j/mikey_nodes )to grab code snippet to pass scoring metadata to image

# Took some base code from the [WAS save image node](https://github.com/WASasquatch/was-node-suite-comfyui) to repurpose it