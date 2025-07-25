July 25/25, V1.5: Adds the Node Spawner to create multiple nodes at once,and a node minimap

July 19/25, V1.3: Introducing the  Endless Fontifier, a javascript file that adds allows the user to change font sizes and fonts for various text elements on the ComfyUI interface.

July 8/25, V1.2.5: Fixed bug in Image Saver that forced a connection for prompts.  That is now optional

July 7/25, V1.2.4: You can now use the batch prompt node with Flux Kontext Dev.  The process works the same way as the other nodes, except here the prompts are used to make changes to the image(s).  You cannot iterate within the prompt set (e.g, set up a list of prompts for a sequence of changes), it is designed to allow you to process multiple scenarios at once.

July 6/25, V1.2.3: Corrected the JSON files that were being exported.  They will now load the workflow when dragged back to the UI.  As a bonus, if the PNGINfo is also selected, the JSON will remove that, lowering the size of the file.

June 28/25, V1.2.2: Corrected Prompt Counter Node so it can accept pipe or newline characters as line breaks, allowing it to be connected immediately to the Batch Prompt node (unlike before), or somewhere else downstream from the prompt creation node(s).  Uploaded JSON files for SD1x and SD2x, SDXL, and updated Flux batch workflow was standardized loader nodes appropriate to the model.  Added an example dynamic prompt workflow for Flux that can be repurposed for other models.  Added images with embedded workflows for the above.

Jun 24/23, V1.2.1: Added parent level requirements.txt file

Jun 23/25, V1.2.0: Added the Endless Pandemonium node, a black box that randomly and invisibly changes parameters on you.  Put in ability to use 64 or 16 as the minimum steps for the dimensions in the Randomizer nodes, added CFG Guidance outputs for Flux.  Fixed typos and added better credits in README.  Some bug squishing.

Jun 22/25, V1.1.1: Minor typos and trying to align version numbers

Jun 21/25, V1.0.0: Blew it all up and started again

Aug 19/24, V0.41: Fixed Image Saver node so it appears

Oct 20/23, V0.40: Updated ImageSaver to turn off  JSON save to image data

Oct 18/23, V0.39: Added six float output node

Oct 18/23, V0.38: (UNRELEASED)Putting in hooks for future fixes and improvements

Oct 18/23, V0.37: Bug fix in Image Saver module that would overwrite files was corrected

Oct 07/23, V0.36: Killed the scorers until I figure out why CLIP won't load for some people

Oct 06/23, V0.35: Reverted the Image Saver module as I had inadvertently removed the ability to add date and time to the filenames

Oct 05/23, V0.33: Renamed nodes to make them shorter and easier to search for, breaks names of previous workflows though

Oct 07/23, V0.33: Removed Aesthetic Scorer and ImageReward until I can figure out why the CLIP module isn't working for a few people

Oct 05/23, V0.32: (UNRELEASED)Set rules for image saver so paths + filename length do not exceed 248 (leaves room for extension)

Oct 04/23, V0.31: Release of V0.28 functionality (int, float, num to X), added String to X, code cleanup, vanity node renaming and recategorization

Oct 04/23, V0.30: Squished bugs in the various X to X nodes

Oct 03/23, V0.29: Save Image module added, saves images and JSON to separate folder if requested

Sep 28/23, V0.28: (UNRELEASED)  Added Variable types to X

Sep 28/23, V0.27: (UNRELEASED) Corrected scoring nodes to actually add the value of the score into the image metadata .... still goobered!

Sep 24/23, V0.26: (UNRELEASED) starting to correct scoring to get to image metadata

Sep 24/23, V0.25: Added various X to String Nodes

Sep 24/23, V0.24: Added In Image Reward scoring model with a single node to load model and output standard deviation and scoring via number or string nodes

Sep 24/23, V0.23: Rework Aesthetic Score model and integrate it into single node to display score, added a requirements file

Sep 23/23, V0.22: (UNRELEASED) Convert ImageReward output to base ten score

Sep 22/23, V0.21: (UNRELEASED) Introduced aestheticscore, recategorized nodes into submenus, added some vanity coding to the node names, changed the ComfyUI manager header text

Sep 21/23, V0.20: (UNRELEASED) Skeleton for save image

Sep 21/23, V0.19: (UNRELEASED) Attempt for basic display nodes

Sep 20/23, V0.16: Added Eight Input Number String 

Sep 18/23, V0.15: Added Combo Parameterizers to reduce number of nodes, allows for common resolution parameters to go to both pos/neg CLIP encode and adds separate pos/neg aesthetic score.  Also has a version with pos/neg prompts

Sep 18/23, V0.13: Fixed typos, added Paramaterizer with Prompt (unreleased to GitHub)

Sep 18/23, V0.12: Added "Parameterizer", allows for parameters to be added to CLIP Encode

Sep 15/23, V0.10: Added Six Input Number Widget, first release to GitHub

Sep 12/23, V0.05: Added Six Input Number String

Sep 08/23, V0.00: Basic Flow for Six Input Text Switch
