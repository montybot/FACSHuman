# FACSHuman v0.0.1 Alpha
## FACSHuman plugin for MakeHuman project
Create pictures and videos of facial expressions for your experiments.

This work is based on the Facial Action coding System :

>Ekman, P., Friesen, W. V., & Hager, J. C. (2002). Facial action coding system. A Human Face.

This plugin allow you to create facial expressions by moving the corresponding Action Units (AU) described in the FACS Manual.
Additional plugins are available to create scene (lights placement and lights colors) and animations.

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
| 7_FACSHuman.py         | (main program)               |
| 8_FACSAnim.py          | (to create facial animation) |
| 9_FACS_scene_editor.py | (to edit/create scene)       |


### Target files of the AUs
All the FACSHuman target files were created with Blender and the MH tools for Blender.

Place targets files directory  into : 

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
Teeth, eyes, eylashes and tongue are modified versions of materials assets from the http://www.makehumancommunity.org/

Place directories in :

for lastest version of MH :
>/home/YOUR_USER/Documents/makehuman/YOUR_NUMBER/data/...

for earlier versions :
>/home/YOUR_USER/Documents/makehuman/data/...

### Teeth
In order to avoid teeth distortion (original models) when you use mouth opening AUs, you need to use the modified facs models.

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

### Eyes
Place it in **/eyes**

This directory contains :
* black_map.png
* /eyes_no_cornea
* /facs-poly
* makehuman_eye_specular.png
* makehuman_eye_specular2.png
* /materials
* /real_pupil_no-cornea
* specular_map.png
* specular_map_invert.png
* specular_map_white_b.png

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

## Additional installation
If you want to use the video production inside FACSHuman you need to install FFmpeg tools :

https://ffmpeg.org/about.html

and put this software into the **path** of your computer.

You will find the procedure on the net depending of your operating system.

# Information
https://www.michaelgilbert.fr/facshuman/

FACSHuman is a plugin for Makehuman.

If you have any questions please contact me  __**not the MH Team**__

# Demo videos
More tutorials videos will be available soon. 
## All AUs demonstration
<a href="http://www.youtube.com/watch?feature=player_embedded&v=RJlP5M_Tmk8" target="_blank"><img src="http://img.youtube.com/vi/RJlP5M_Tmk8/0.jpg" alt="IMAGE ALT TEXT HERE" width="480" height="360" border="10" /></a>

## Full demo
<a href="http://www.youtube.com/watch?feature=player_embedded&v=qqUxmFsK_Po" target="_blank"><img src="http://img.youtube.com/vi/qqUxmFsK_Po/0.jpg" alt="IMAGE ALT TEXT HERE" width="480" height="360" border="10" /></a>

## FACSvatar Datas
<a href="http://www.youtube.com/watch?feature=player_embedded&v=jQwcDjFpq5g " target="_blank"><img src="http://img.youtube.com/vi/jQwcDjFpq5g/0.jpg" alt="IMAGE ALT TEXT HERE" width="480" height="360" border="10" /></a>

https://www.youtube.com/channel/UCEAepvD886XqB6wikmXW8Qg

# Usable Action Units in FACSHuman
<table id="org3211805" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
<caption class="t-above"><span class="table-number">Table 1:</span> Usable Action Units in FACS</caption>

<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Action units</th>
<th scope="col" class="org-left">Simple</th>
<th scope="col" class="org-left">Right / Left</th>
<th scope="col" class="org-left">Alternative</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">Upper Face AUs</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
<tbody>
<tr>
<td class="org-left">1 Inner Brow Raise</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
</tr>

<tr>
<td class="org-left">2 Outer Brow Raise</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
</tr>

<tr>
<td class="org-left">4 Brow Lowerer</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">X (41,42,44)</td>
</tr>

<tr>
<td class="org-left">5 Upper Lid Raise</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">6 Cheek Raise</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">X (2)</td>
</tr>

<tr>
<td class="org-left">7 Lids Tight</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">43 Eye Closure</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">45 Blink</td>
<td class="org-left">Use 43</td>
<td class="org-left">Use 43</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">46 Wink</td>
<td class="org-left">Use 43</td>
<td class="org-left">Use 43</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">70 Brows Not Visible</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-left">71 Eyes Not Visible</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
</tr>
</tbody>
<tbody>
<tr>
<td class="org-left">Head Positions</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
<tbody>
<tr>
<td class="org-left">51 Turn Left</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">52 Turn Right</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">53 Head Up</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">54 Head Down</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">55 Tilt Left</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">56 Tilt Right</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">57 Forward</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">58 Back</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">Eye Positions</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">61 Eyes Left</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">62 Eyes Right</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">63 Eyes Up</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">64 Eyes Down</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">65 Walleye</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">66 Crosseye</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">Lip Parting and Jaw Opening</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">25 Lips Part</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
</tr>

<tr>
<td class="org-left">26 Jaw Drop</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">X(4)</td>
</tr>

<tr>
<td class="org-left">27 Mouth Stretch</td>
<td class="org-left">Use 26</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
</table>

<table id="orgab4f278" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
<caption class="t-above"><span class="table-number">Table 2:</span> Lower Face and Miscellaneous Action Units</caption>

<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Action units</th>
<th scope="col" class="org-left">Simple</th>
<th scope="col" class="org-left">Right / Left</th>
<th scope="col" class="org-left">Alternative</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">Lower Face AUs</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
<tbody>
<tr>
<td class="org-left">9 Nose Wrinkle</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
</tr>

<tr>
<td class="org-left">10 Upper Lip Raiser</td>
<td class="org-left">X + 25</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">11 Nasolabial Furrow Deepener</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">12 Lip Corner Puller</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">X(2)</td>
</tr>

<tr>
<td class="org-left">13 Sharp Lip Puller</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">14 Dimpler</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">15 Lip Corner Depressor</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">16 Lower Lip Depress</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">17 Chin Raiser</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">X</td>
</tr>

<tr>
<td class="org-left">18 Lip Pucker</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">X</td>
</tr>

<tr>
<td class="org-left">20 Lip Stretch</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">22 Lip Funneler</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">X(2)</td>
</tr>

<tr>
<td class="org-left">23 Lip Tightener</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">24 Lip Presser</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">28 Lips Suck</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">X(2)</td>
</tr>

<tr>
<td class="org-left">72 Lower Face Not Visible</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
</tr>
</tbody>
<tbody>
<tr>
<td class="org-left">Miscellaneous AUs</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
<tbody>
<tr>
<td class="org-left">8 Lips Toward Each Other</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-left">19 Tongue Show</td>
<td class="org-left">X + 26</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">21 Neck Tightener</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-left">29 Jaw Thrust</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">30 Jaw Sideways</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">31 Jaw Clencher</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">32 Bite</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">33 Blow</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">34 Puff</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">35 Cheek Suck</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">36 Tongue Bulge</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-left">37 Lip Wipe</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-left">38 Nostril Dilate</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">39 Nostril Compress</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
</table>

<table id="orgd74d3ec" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
<caption class="t-above"><span class="table-number">Table 3:</span> Additional Action Units</caption>

<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">FACSHuman</th>
<th scope="col" class="org-left">Simple</th>
<th scope="col" class="org-left">Right / Left</th>
<th scope="col" class="org-left">Alternative</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">pupils dilatation</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">pupils constriction</td>
<td class="org-left">X</td>
<td class="org-left">X</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
</table>

<table id="orgef85b8f" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
<caption class="t-above"><span class="table-number">Table 4:</span> Table of legends</caption>

<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">X :</td>
<td class="org-left">Usable in the module</td>
</tr>

<tr>
<td class="org-left">-  :</td>
<td class="org-left">non implemented</td>
</tr>

<tr>
<td class="org-left">+ :</td>
<td class="org-left">Usable with …</td>
</tr>

<tr>
<td class="org-left">(Num) :</td>
<td class="org-left">Alternative Action units</td>
</tr>
</tbody>
</table>




