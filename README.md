# FACSHuman v0.0.1 Alpha
## FACSHuman plugin for MakeHuman project
Create pictures and videos of facial expressions for your experiments.

This work is based on the Facial Action coding System :

>Ekman, P., Friesen, W. V., & Hager, J. C. (2002). Facial action coding system. A Human Face.

This software allow you to move the corresponding Action Units (AU) described in the FACS Manual.

## Paper
Please cite the following paper if you use this plugin for your research :

>Gilbert, M., Demarchi, S., & Urdapilleta, I. (2018). FACSHuman a Software to Create Experimental Material by Modeling 3D Facial Expression. Proceedings of the 18th International Conference on Intelligent Virtual Agents  - IVA ’18, 333‑334.
https://doi.org/10.1145/3267851.3267865 - ISBN: 978-1-4503-6013-5

## The conference
1. https://iva2018.westernsydney.edu.au/
2. https://dl.acm.org/citation.cfm?id=3267865#

## Link to my profile
https://www.researchgate.net/profile/Michael_Gilbert10

# Documentation
## Get started
Download and install MakeHuman from here http://www.makehumancommunity.org/content/downloads.html
and follow the instructions for your Operating System.

Then start MakeHuman once to create the MH directory in your home/YOURUSER/Document/ 

### For MH
If you have any questions about the installation and the use of this software :

http://www.makehumancommunity.org/wiki/Main_Page

http://www.makehumancommunity.org/forum/

## FACSHuman Installation
### Main files (the core)
Put this files inside the plugin directory of your MH installation (not in the plugin directory of MH in USER/Document/makehuman)

| File                   | Usage                        |
|:-----------------------| ----------------------------:|
| 9_FACS_scene_editor.py | (to edit/create scene)       |
| 8_FACSAnim.py          | (to create facial animation) |
| 7_FACSHuman.py         | (main program)               |


### Target files of the AUs
Place the targets files directory  into : 

For lastest version of MH :
>/home/YOUR_USER/Documents/makehuman/YOUR_NUMBER/data/FACSHuman/

For earlier versions :
>/home/michael/Documents/makehuman/data/FACSHuman/

This directory contains :
* 00 Emotions
* 01 Upper Face AUs
* 02 Lower Face AUs
* 03 Lip Parting and Jaw Opening
* 04 Eye Positions
* 05 Head Positions
* 06 Miscellaneous AUs
* au.json
* black.jpg

**Whithout these files plugins do not work**

## Additional ressources
Place directories in :

for lastest version of MH :
>/home/YOUR_USER/Documents/makehuman/YOUR_NUMBER/data/...

for earlier versions :
>/home/michael/Documents/makehuman/data/...

### Teeth
In order to avoid teeth distortion (original models) zhen you use mouth opening, you need to use the modified facs models.

Place it in **/teeth**

This directory contains :
* FACSTeeth01
* FACSTeeth01a
* FACSTeeth01b
* FACSTeeth02
* FACSTeeth02a
* FACSTeeth02b
* FACSteeth03
* FACSteeth03_bw
* FACSteeth04

### Eyelashes
Place it in **/eyelashes**

This directory contains :
* FACSEyeLashes01

### Tongue
Place it in **/tongue**

This directory contains :
* FACSTongue
* FACSTongue_bw (black and white model)

### Custom
Place it in **/custom**

This directory contains :
* close_lips.target
This target is useful to close the small gap between lips of the MH model.

# Information
https://www.michaelgilbert.fr/facshuman/

FACSHuman is a plugin for Makehuman.

If you have any questions please contact me  __**not the MH Team**__

# Demo videos
## All AUs demonstration
<a href="http://www.youtube.com/watch?feature=player_embedded&v=RJlP5M_Tmk8" target="_blank"><img src="http://img.youtube.com/vi/RJlP5M_Tmk8/0.jpg" alt="IMAGE ALT TEXT HERE" width="480" height="360" border="10" /></a>

## Full demo
<a href="http://www.youtube.com/watch?feature=player_embedded&v=qqUxmFsK_Po" target="_blank"><img src="http://img.youtube.com/vi/qqUxmFsK_Po/0.jpg" alt="IMAGE ALT TEXT HERE" width="480" height="360" border="10" /></a>

## FACSvatar Datas
<a href="http://www.youtube.com/watch?feature=player_embedded&v=jQwcDjFpq5g " target="_blank"><img src="http://img.youtube.com/vi/jQwcDjFpq5g/0.jpg" alt="IMAGE ALT TEXT HERE" width="480" height="360" border="10" /></a>

https://www.youtube.com/channel/UCEAepvD886XqB6wikmXW8Qg
