Oct 18/23: V0.38: (UNRELEASED)Putting in hooks for future fixes and improvements
Oct 18/23: V0.37: (UNRELEASED) Attempt to pass scoring metadata to image saver
Oct 18/23: V0.36: (UNRELEASED) Attempt to add new node to simplify resolution input and steps
Oct 14/23: V0.35: Fixed issues with scoring nodes and updated image saver for some bugs
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
