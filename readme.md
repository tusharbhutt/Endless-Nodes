# Endless-Nodes
Some basic custom nodes for the ComfyUI user interface for Stable Diffusion.

When using the [ComfyUI](https://github.com/comfyanonymous/ComfyUI) interface for [Stable Diffusion](https://github.com/Stability-AI/stablediffusion), I sometimes find that the standard nodes and the many, many, many custom nodes out there don't work the way I want them to, or how I think they do.

Rightly or wrongly, I am pretending to teach myself a bit of Python to get some nodes up and running to do what I'd like.  There are no promises that these nodes will work for you or that I will maintain them.  Feel free to do with them as you wish, according to the license model.

## UPDATE: Sep 17, 2023

### Added the Endless Nodes Parameterizer

## Install

Navigate to your /ComfyUI/custom_nodes/ folder 

In Windows, you can then right-click to start a command prompt and type:

`git clone https://github.com/tusharbhutt/Endless-Nodes`

## Node List

### Six Text Input Switch
Allows the user to select between six text inputs and uses a slider to make the selection.  Useful for multiple inputs for prompt creation


![sixtext](./img/sixtext.png)


### Six Integer Input to Six Integer Output
I've seen a fair number of 3-, 4-, or more way text input and outputs, I wanted to do something for numbers as well.  Use it as you wish.

![sixintconnect](./img/sixintconnect.png)

### Six Integer Widget
As above, but with widgets for entry instead of connectors

![sixintwidget](./img/sixintwidget.png)

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

![sixintconnect](./img/parameterizer.png)

## Usage License and Restrictions

See GPL Licensing V3 for usage.  You may modify this code as long as you keep the credits for this repository and for those noted in the credit section below.  **YOU ARE EXPRESSLY FORBIDDEN FROM USING THIS NODE TO CREATE ANY IMAGES OR ARTWORK THAT VIOLATES THE STABLE DIFFUSION USAGE NOTES [HERE](https://huggingface.co/stabilityai/stable-diffusion-2#misuse-malicious-use-and-out-of-scope-use) AND [HERE](https://huggingface.co/stabilityai/stable-diffusion-2#misuse-and-malicious-use).**

For example, don't be a mouth-breathing dick who creates fake celebrity nudes or sexual content of **anyone, even** if you have their consent

The author expressly disclaims any liability for any images you create using these nodes.

## Disclaimer

These nodes may or may not be maintained.  They work on my system, but may not on yours.  

## Credits

[Comfyroll Custom Nodes](https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNode) for the overall node code layout, coding snippets,  and inspiration for the text input and number switches


 [WLSH Nodes](https://github.com/wallish77/wlsh_nodes) for some coding for the Integer Widget
 

[ComfyUI](https://github.com/comfyanonymous/ComfyUI) Interface for the basic ideas of what nodes I wanted
