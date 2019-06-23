#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

""" 
**Project Name:**      FACSAnim for FACSHuman facial expression creation tool
**Authors:**           Michaël GILBERT
**Copyright(c):**      Michaël GILBERT 2019
"""

# FACSHuman
# Copyright (C) 2019  Michael GILBERT

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



import random
import gui3d
import mh
import gui
import log
import getpath
import os
import humanmodifier
import modifierslider
# import algos3d
import json
# import scene
# import projection
# import numpy as np
import glmodule
import image
from image import Image
import image_operations as imgop
# import guirender
from core import G
from progress import Progress
# import 7_FACSHuman2
import locale

##########################################################################
# Main Class for FACSHuman plugin
##########################################################################

class FacsTimeLineSlider(object):

    def __init__(self, anim_task_view, au_timeline, au_event = 0,
                 image_start = 0, image_stop= 1,
                 intensity_start = 0, intensity_stop = 1,
                 apex_start = 0.33, apex_stop = 0.66,
                 apex_intensity_start = 0.33, apex_intensity_stop = 0.66
                 ):
        # Box creation
        # self.box_au_right = anim_task_view.addRightWidget(gui.GroupBox(au_timeline))
        # anim_task_view.facs_code_names[str(mod.name.capitalize())
        au_timeline = str(au_timeline)
        self.box_au_right = anim_task_view.addRightWidget(gui.GroupBox(anim_task_view.facs_code_names[au_timeline]))
        box_intensity = self.box_au_right.addWidget(gui.GroupBox('Intensity'))
        box_time = self.box_au_right.addWidget(gui.GroupBox('Time'))

        # Intensity Sliders
        slider_intensity_start = box_intensity.addWidget(gui.Slider(value=intensity_start, min=0, max=1, vertical=True, label=['',' %.2f']), 1, 0)
        slider_apex_intensity_start = box_intensity.addWidget(gui.Slider(value=apex_intensity_start, min=0, max=1, vertical=True, label=['',' %.2f']), 1, 1)
        slider_apex_intensity_stop = box_intensity.addWidget(gui.Slider(value=apex_intensity_stop, min=0, max=1, vertical=True, label=['',' %.2f']), 1, 2)
        slider_intensity_stop = box_intensity.addWidget(gui.Slider(value=intensity_stop, min=0, max=1, vertical=True, label=['',' %.2f']), 1, 3)
        box_intensity.addWidget(gui.TextView('Start | Apex start | Apex stop | Stop'), columnSpan = 4)
        
        # Timeline Sliders        
        slider_image_start = box_time.addWidget(gui.Slider(value=image_start, min=0, max=1, label=['Start',' %.2f']))
        slider_apex_start = box_time.addWidget(gui.Slider(value=apex_start, min=0, max=1, label=['Apex Start',' %.2f']))
        slider_apex_stop = box_time.addWidget(gui.Slider(value=apex_stop, min=0, max=1, label=['Apex Stop',' %.2f']))
        slider_image_stop = box_time.addWidget(gui.Slider(value=image_stop, min=0, max=1, label=['Stop',' %.2f']))
        
        remove_au_widgets_button = box_time.addWidget(gui.Button('Remove AU'))

        ##########################################################################
        # Define each slider intensity event
        ##########################################################################
       
        @slider_intensity_start.mhEvent
        def onChange(value):
            #log.message('FACSHumMsg %s %s %s', labelSlider, slider, slidersValues)
            # anim_task_view.au_timeline_values[au_timeline][au_event]['intensity_start'] = value
            anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'intensity_start', value)
       
        @slider_apex_intensity_start.mhEvent
        def onChange(value):
            #log.message('FACSHumMsg %s %s %s', labelSlider, slider, slidersValues)
            # anim_task_view.au_timeline_values[au_timeline][au_event]['apex_intensity_start'] = value
            anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_intensity_start', value)
            
        @slider_apex_intensity_stop.mhEvent
        def onChange(value):
            #log.message('FACSHumMsg %s %s %s', labelSlider, slider, slidersValues)
            # anim_task_view.au_timeline_values[au_timeline][au_event]['apex_intensity_stop'] = value
            anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_intensity_stop', value)
           
        @slider_intensity_stop.mhEvent
        def onChange(value):
            #log.message('FACSHumMsg %s %s %s', labelSlider, slider, slidersValues)
            # anim_task_view.au_timeline_values[au_timeline][au_event]['intensity_stop'] = value
            anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'intensity_stop', value)
           
        @slider_image_start.mhEvent
        def onChange(value):
            #log.message('FACSHumMsg %s %s %s', labelSlider, slider, slidersValues)
            # anim_task_view.au_timeline_values[au_timeline][au_event]['image_start'] = value
            if value >= slider_apex_start.getValue():
               slider_apex_start.setValue(value+0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_start', value+0.01)
            if value >= slider_apex_stop.getValue():
               slider_apex_stop.setValue(value+0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_stop', value+0.01)
            if value >= slider_image_stop.getValue():
               slider_image_stop.setValue(value+0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'image_stop',  value+0.01)
            
            anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'image_start', value)

           
        @slider_apex_start.mhEvent
        def onChange(value):
            #log.message('FACSHumMsg %s %s %s', labelSlider, slider, slidersValues)
            # anim_task_view.au_timeline_values[au_timeline][au_event]['apex_start'] = value
            if value >= slider_apex_stop.getValue():
               slider_apex_stop.setValue(value+0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_stop', value+0.01)
            if value >= slider_image_stop.getValue():
               slider_image_stop.setValue(value+0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'image_stop',  value+0.01)
            
            if value <= slider_image_start.getValue():
               slider_image_start.setValue(value - 0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'image_start', value - 0.01)
               
            anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_start', value)
            
        @slider_apex_stop.mhEvent
        def onChange(value):
            #log.message('FACSHumMsg %s %s %s', labelSlider, slider, slidersValues)
            # anim_task_view.au_timeline_values[au_timeline][au_event]['apex_stop'] = value
            if value >= slider_image_stop.getValue():
               slider_image_stop.setValue(value+0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'image_stop',  value+0.01)
            if value <= slider_apex_start.getValue():
               slider_apex_start.setValue(value - 0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_start', value - 0.01)
            if value <= slider_image_start.getValue():
               slider_image_start.setValue(value - 0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'image_start', value - 0.01)
            
            anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_stop', value)
          
        @slider_image_stop.mhEvent
        def onChange(value):
            #log.message('FACSHumMsg %s %s %s', labelSlider, slider, slidersValues)
            # anim_task_view.au_timeline_values[au_timeline][au_event]['image_stop'] = value
            if value <= slider_apex_stop.getValue():
               slider_apex_stop.setValue(value - 0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'image_stop',  value+0.01)
            if value <= slider_apex_start.getValue():
               slider_apex_start.setValue(value - 0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_start', value - 0.01)
            if value <= slider_image_start.getValue():
               slider_image_start.setValue(value - 0.01)
               anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'image_start', value - 0.01)
            
            anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'image_stop', value)
         
            
        ##########################################################################
        # Remove au widget from animation
        ##########################################################################
            
        @remove_au_widgets_button.mhEvent
        def onClicked(event):
            log.message('Box removed %s', self)
            self.box_au_right.removeWidget(self.box_au_right)
            anim_task_view.delAuTimelineEvent(au_timeline, au_event)
            anim_task_view.modifiers_sliders[au_timeline].onChanging(0)
            anim_task_view.modifiers_sliders[au_timeline].update()
            anim_task_view.modifiers_sliders[au_timeline].setValue(0)
            # log.message('la box %s', anim_task_view.au_timeline_box)
        
    def removeAu(self):
        self.box_au_right.removeWidget(self.box_au_right)


class FACSTest(gui3d.TaskView):

    def __init__(self, category, appFacsAnim):
        gui3d.TaskView.__init__(self, category, 'FACS Animation Tool')
        self.facs_human = appFacsAnim.selectedHuman
        self.app = appFacsAnim
        ##########################################################################
        # .json Au's list loading
        ##########################################################################

        self.facs_code_names_path = getpath.getDataPath('FACSHuman')
        self.facs_code_names_file = self.facs_code_names_path + '/au.json'
        self.facs_code_names = json.loads(open(self.facs_code_names_file).read())

        box_aus_list = self.addLeftWidget(gui.GroupBox('AUs List chooser'))
        box_tools_intensity = self.addLeftWidget(gui.GroupBox('Initial intensity pattern'))
        box_tools_time = self.addLeftWidget(gui.GroupBox('Initial time pattern'))
        box_animation = self.addLeftWidget(gui.GroupBox('Animation'))
       
        
        self.user_add_facs_intesity_pattern = 'all' # all = all ; zerotofull = 0 to full ; fulltozero = full to 0

        
# Box tools        

        # Intensity Sliders
        self.select_intensity_add_facs_button_group = []
        self.intensity_facs_radiobutton1 = box_tools_intensity.addWidget(gui.RadioButton(self.select_intensity_add_facs_button_group, 'Full'), 0, 0)
        self.intensity_facs_radiobutton2 = box_tools_intensity.addWidget(gui.RadioButton(self.select_intensity_add_facs_button_group, '0>full', selected=True), 0, 1)
        self.intensity_facs_radiobutton3 = box_tools_intensity.addWidget(gui.RadioButton(self.select_intensity_add_facs_button_group, 'full>0'), 0, 2)
        self.intensity_facs_radiobutton4 = box_tools_intensity.addWidget(gui.RadioButton(self.select_intensity_add_facs_button_group, '/full\\'), 0, 3)
        
        self.slider_intensity_start_tool = box_tools_intensity.addWidget(gui.Slider(value=0, min=0, max=1, vertical=True, label=['',' %.2f']), 1, 0)
        self.slider_apex_intensity_start_tool = box_tools_intensity.addWidget(gui.Slider(value=0.33, min=0, max=1, vertical=True, label=['',' %.2f']), 1, 1)
        self.slider_apex_intensity_stop_tool = box_tools_intensity.addWidget(gui.Slider(value=0.66, min=0, max=1, vertical=True, label=['',' %.2f']), 1, 2)
        self.slider_intensity_stop_tool = box_tools_intensity.addWidget(gui.Slider(value=1, min=0, max=1, vertical=True, label=['',' %.2f']), 1, 3)
        
        box_tools_intensity.addWidget(gui.TextView('Start'),2,0,)
        box_tools_intensity.addWidget(gui.TextView('Apex start'),2,1)
        box_tools_intensity.addWidget(gui.TextView('Apex stop'),2,2)
        box_tools_intensity.addWidget(gui.TextView('Stop'),2,3)
        
        
        @self.intensity_facs_radiobutton1.mhEvent
        def onClicked(event):
            self.slider_intensity_start_tool.setValue(1)
            self.slider_apex_intensity_start_tool.setValue(1)
            self.slider_apex_intensity_stop_tool.setValue(1)
            self.slider_intensity_stop_tool.setValue(1)
            
        
        @self.intensity_facs_radiobutton2.mhEvent
        def onClicked(event):
            self.slider_intensity_start_tool.setValue(0)
            self.slider_apex_intensity_start_tool.setValue(0.33)
            self.slider_apex_intensity_stop_tool.setValue(0.66)
            self.slider_intensity_stop_tool.setValue(1)

        
        @self.intensity_facs_radiobutton3.mhEvent
        def onClicked(event):
            self.slider_intensity_start_tool.setValue(1)
            self.slider_apex_intensity_start_tool.setValue(0.66)
            self.slider_apex_intensity_stop_tool.setValue(0.33)
            self.slider_intensity_stop_tool.setValue(0)
         
        @self.intensity_facs_radiobutton4.mhEvent
        def onClicked(event):
            self.slider_intensity_start_tool.setValue(0)
            self.slider_apex_intensity_start_tool.setValue(1)
            self.slider_apex_intensity_stop_tool.setValue(1)
            self.slider_intensity_stop_tool.setValue(0)
       
        # Timeline Sliders 
        self.select_time_add_facs_button_group = []
        self.time_facs_radiobutton0 = box_tools_time.addWidget(gui.RadioButton(self.select_time_add_facs_button_group, 'full', selected=True), 0, 0)
        self.time_facs_radiobutton1 = box_tools_time.addWidget(gui.RadioButton(self.select_time_add_facs_button_group, '1/3>'), 0, 1)
        self.time_facs_radiobutton2 = box_tools_time.addWidget(gui.RadioButton(self.select_time_add_facs_button_group, '2/3>'), 0, 2)
        self.time_facs_radiobutton3 = box_tools_time.addWidget(gui.RadioButton(self.select_time_add_facs_button_group, '<2/3'), 0, 3)
        self.time_facs_radiobutton4 = box_tools_time.addWidget(gui.RadioButton(self.select_time_add_facs_button_group, '<1/3'), 0, 4)
        
        self.slider_image_start_tool = box_tools_time.addWidget(gui.Slider(value=0, min=0, max=1, label=['Start',' %.2f']), columnSpan = 5)
        self.slider_apex_start_tool = box_tools_time.addWidget(gui.Slider(value=0.33, min=0, max=1, label=['Apex Start',' %.2f']), columnSpan = 5)
        self.slider_apex_stop_tool = box_tools_time.addWidget(gui.Slider(value=0.66, min=0, max=1, label=['Apex Stop',' %.2f']), columnSpan = 5)
        self.slider_image_stop_tool = box_tools_time.addWidget(gui.Slider(value=1, min=0, max=1, label=['Stop',' %.2f']), columnSpan = 5)


        @self.time_facs_radiobutton0.mhEvent
        def onClicked(event):
            self.slider_image_start_tool.setValue(0)
            self.slider_apex_start_tool.setValue(0.33)
            self.slider_apex_stop_tool.setValue(0.66)
            self.slider_image_stop_tool.setValue(1)

        @self.time_facs_radiobutton1.mhEvent
        def onClicked(event):
            self.slider_image_start_tool.setValue(0)
            self.slider_apex_start_tool.setValue(0.11)
            self.slider_apex_stop_tool.setValue(0.22)
            self.slider_image_stop_tool.setValue(0.33)
            
        
        @self.time_facs_radiobutton2.mhEvent
        def onClicked(event):
            self.slider_image_start_tool.setValue(0)
            self.slider_apex_start_tool.setValue(0.22)
            self.slider_apex_stop_tool.setValue(0.44)
            self.slider_image_stop_tool.setValue(0.66)

        
        @self.time_facs_radiobutton3.mhEvent
        def onClicked(event):
            self.slider_image_start_tool.setValue(0.33)
            self.slider_apex_start_tool.setValue(0.55)
            self.slider_apex_stop_tool.setValue(0.77)
            self.slider_image_stop_tool.setValue(1)
            
        @self.time_facs_radiobutton4.mhEvent
        def onClicked(event):
            self.slider_image_start_tool.setValue(0.66)
            self.slider_apex_start_tool.setValue(0.77)
            self.slider_apex_stop_tool.setValue(0.88)
            self.slider_image_stop_tool.setValue(1)
       
        ##########################################################################
        # Define each slider intensity event
        ##########################################################################
       
        # @self.slider_image_start_tool.mhEvent
        # def onChange(value):
            # anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'intensity_start', value)
       
        # @self.slider_apex_start_tool.mhEvent
        # def onChange(value):
            # anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_intensity_start', value)
            
        # @self.slider_apex_stop_tool.mhEvent
        # def onChange(value):
            # anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'apex_intensity_stop', value)
           
        # @self.slider_image_stop_tool.mhEvent
        # def onChange(value):
            # anim_task_view.setOneAuTimelineValue(au_timeline, au_event, 'intensity_stop', value)
            

# Box tools        
        self.animation_test = box_aus_list.addWidget(gui.Slider(value=0.00, min=0.00, max=25, label=['Animation frame test : ','%d']), columnSpan = 3)
        self.txt_number_of_frame = box_aus_list.addWidget(gui.TextView('Frames : '), 1, 0)
        self.images_number_to_render = box_aus_list.addWidget(gui.TextEdit(text='25'), 1, 1)
        self.mix_toggle_button = box_aus_list.addWidget(gui.CheckBox('Mix AUs'), 1, 2)
        self.aus_list_items = box_aus_list.addWidget(gui.ListView(), columnSpan = 3)
        self.add_au_timeline_button = box_aus_list.addWidget(gui.Button('Add AU to the timeline'), columnSpan = 3)
        
        self.facs_modifiers = []
        self.facs_modifiers = G.app.selectedHuman.getModifiersByGroup('Upper Face AUs')
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Lower Face AUs'))
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Head Positions'))
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Eye Positions'))
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Lip Parting and Jaw Opening'))
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Miscellaneous AUs'))
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Emotions Blender'))

        self.au_timeline_values = {} # For the animation functionality
        self.au_timeline_box = {}
        self.save_path = getpath.getDataPath('facs')
      
# Box animation
        self.txt_animatiom_file_loaded = box_animation.addWidget(gui.TextView('No animation file loaded'))
        self.load_animation_button =  box_animation.addWidget(gui.BrowseButton('open', "Load AUs animation timeline"))
        self.save_animation_button =  box_animation.addWidget(gui.BrowseButton('save', "Save AUs animation timeline"))
        self.reset_au_widgets_button = box_animation.addWidget(gui.Button('Remove all AUs of animation'))
        self.load_facs_button =  box_animation.addWidget(gui.BrowseButton('open', "Add FACS file to timeline"))
        self.reset_camera_button = box_animation.addWidget(gui.Button('Full face camera view'))
        
        #self.render_timelined_video_button = box_images_rendering.addWidget(gui.Button('Render timelined animation'))
        #self.index_timeline = box_images_rendering.addWidget(gui.TextEdit(text='1'))
        self.load_animation_button.setDirectory(self.save_path)
        self.load_facs_button.setDirectory(self.save_path)
        self.save_animation_button.setDirectory(self.save_path)
        self.load_animation_button.setFilter("Aus animation timeline (*.fani)")
        self.save_animation_button.setFilter("Aus animation timeline (*.fani)")
        self.load_facs_button.setFilter("FACS code file (*.facs)")
        
        self.modifiers_sliders = {}
        
        self.au_number_to_add = ''

        for mod in self.facs_modifiers:
            self.modifiers_sliders[mod.name] = modifierslider.ModifierSlider(modifier=mod, label=mod.name)
            self.aus_list_items.addItem(self.facs_code_names[str(mod.name)], 'black', mod.name,  False)

        @self.add_au_timeline_button.mhEvent  
        def onClicked(event):
            if len(self.au_number_to_add) > 0:
               au_event = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
               self.au_timeline_box[str(au_event)] = FacsTimeLineSlider(self, self.au_number_to_add, au_event, image_start = self.slider_image_start_tool.getValue(),
                                                                                                               image_stop= self.slider_image_stop_tool.getValue(),
                                                                                                               intensity_start = self.slider_intensity_start_tool.getValue(),
                                                                                                               intensity_stop = self.slider_intensity_stop_tool.getValue(),
                                                                                                               apex_start = self.slider_apex_start_tool.getValue(),
                                                                                                               apex_stop = self.slider_apex_stop_tool.getValue(),
                                                                                                               apex_intensity_start = self.slider_apex_intensity_start_tool.getValue(),
                                                                                                               apex_intensity_stop = self.slider_apex_intensity_stop_tool.getValue())
                                                                                                               
               self.addAuTimelineValues(self.au_number_to_add, au_event, image_start = self.slider_image_start_tool.getValue(),
                                                                         image_stop= self.slider_image_stop_tool.getValue(),
                                                                         intensity_start = self.slider_intensity_start_tool.getValue(),
                                                                         intensity_stop = self.slider_intensity_stop_tool.getValue(),
                                                                         apex_start = self.slider_apex_start_tool.getValue(),
                                                                         apex_stop = self.slider_apex_stop_tool.getValue(),
                                                                         apex_intensity_start = self.slider_apex_intensity_start_tool.getValue(),
                                                                         apex_intensity_stop = self.slider_apex_intensity_stop_tool.getValue())
            
        @self.aus_list_items.mhEvent
        def onClicked(item):
            log.message('tftf %s %s', item.getUserData(), type(item.getUserData()))
            self.au_number_to_add = str(item.getUserData())
            # self.modifiers_sliders[str(item.getUserData())].onChanging(1)
            # self.sliders[key_code].update()
            # self.sliders[key_code].setValue(intensity_button_value)
            # self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            
        @self.reset_au_widgets_button.mhEvent
        def onClicked(event):
            G.app.prompt('Confirmation',
                    'Do you really want to reset your Facial animation ?',
                    'Yes', 'Cancel', self.resetAnimation)

##########################################################################
# Animation test slider definition
##########################################################################
 
        @self.animation_test.mhEvent
        def onChanging(value):
            self.slidersSequencerRenderImageSet(value)
            
###########################################################################################
# Load and render button for .fani file's type (json format) Timeline for AUs animation
###########################################################################################     

        @self.load_animation_button.mhEvent
        def onClicked(path):
            if path:
               self.resetFacialCodes()
               self.loadAusTimelineFile(path)
               
###########################################################################################
# Save .fani file's type (json format) Timeline for AUs animation
###########################################################################################     

        @self.save_animation_button.mhEvent
        def onClicked(path):
            if path:
               self.saveAusTimelineFile(path)


###########################################################################################
# Load and render button for .fani file's type (json format) Timeline for AUs animation
###########################################################################################     

        @self.load_facs_button.mhEvent
        def onClicked(path):
            if path:
               self.loadFacsFile(path)
               
##########################################################################
# Update of the slider maximum animation_test
##########################################################################
            
        @self.images_number_to_render.mhEvent
        def onChange(value):
            try:
                self.animation_test.setMax(int(value))
            except:  # The user hasn't typed the value correctly yet.
                self.animation_test.setMax(25)

##########################################################################
# Reset button for camera's orientation to have full face view
# in order to have constant point of view for experiments
##########################################################################
                
        @self.reset_camera_button.mhEvent
        def onClicked(event):
            self.resetCamera()

##########################################################################
# Refresh smooth mesh if is set to on function
# Use the setSubdivided method instead of
# updateSubdivisionMesh because of the memory
# problem usage on windows (see guicommon):
# self.__subdivisionMesh = self.__proxySubdivisionMesh = None
# Garbage collector problem ?
##########################################################################
        
    def refreshAuSmoothSetting(self):
        if self.facs_human.isSubdivided():
            self.facs_human.setSubdivided(False)
            self.facs_human.setSubdivided(True)

    def resetAnimation(self):
        log.message('au_timeline_box %s', self.au_timeline_box)
        for event_key, event_au in self.au_timeline_box.items():
            event_au.removeAu()
        self.resetFacialCodes()
        self.au_timeline_values = {}
#################################################################################

    def slidersSequencerRenderImageSet(self, index_image, nb_images = ''):
        
        if len(nb_images) == 0:
           nb_images = float(self.images_number_to_render.getText())
        else:
           nb_images = float(nb_images)

        index_au = float(index_image) / nb_images
        intensity_button_value = 0
        
        for au_timeline in self.au_timeline_values.keys():
            au_timeline = str(au_timeline)
            if self.mix_toggle_button.selected:
                intensity_button_value = 0
                for au_event in self.au_timeline_values[au_timeline].keys():
                    image_start = float(self.au_timeline_values[au_timeline][au_event]['image_start'])
                    image_stop = float(self.au_timeline_values[au_timeline][au_event]['image_stop'])
                    intensity_start = float(self.au_timeline_values[au_timeline][au_event]['intensity_start'])
                    intensity_stop = float(self.au_timeline_values[au_timeline][au_event]['intensity_stop'])
                    apex_start = float(self.au_timeline_values[au_timeline][au_event]['apex_start'])
                    apex_stop = float(self.au_timeline_values[au_timeline][au_event]['apex_stop'])
                    apex_intensity_start = float(self.au_timeline_values[au_timeline][au_event]['apex_intensity_start'])
                    apex_intensity_stop = float(self.au_timeline_values[au_timeline][au_event]['apex_intensity_stop'])
                
                    if (index_au >= image_start and index_au <= apex_start) or (index_au >= apex_start and index_au <= apex_stop) or (index_au >= apex_stop and index_au <= image_stop):
                    
                       if (index_au >= image_start and index_au <= apex_start):
                          intensity_button_value = intensity_button_value + self.calcIntensityMix(nb_images, index_image, intensity_start, apex_intensity_start, image_start, apex_start)
                       elif (index_au >= apex_start and index_au <= apex_stop):
                          intensity_button_value = intensity_button_value + self.calcIntensityMix(nb_images, index_image, apex_intensity_start, apex_intensity_stop, apex_start, apex_stop)
                       elif (index_au >= apex_stop and index_au <= image_stop):
                          intensity_button_value = intensity_button_value + self.calcIntensityMix(nb_images, index_image, apex_intensity_stop, intensity_stop, apex_stop, image_stop)
      
                if intensity_button_value >= 0:
                   intensity_button_value = intensity_button_value / len(self.au_timeline_values[au_timeline])
                   gui3d.app.statusPersist(str(intensity_button_value))
                   self.modifiers_sliders[au_timeline].onChanging(intensity_button_value)
                   self.modifiers_sliders[au_timeline].update()
                   self.modifiers_sliders[au_timeline].setValue(intensity_button_value)
            else:
                for au_event in self.au_timeline_values[au_timeline].keys():
                    image_start = float(self.au_timeline_values[au_timeline][au_event]['image_start'])
                    image_stop = float(self.au_timeline_values[au_timeline][au_event]['image_stop'])
                    intensity_start = float(self.au_timeline_values[au_timeline][au_event]['intensity_start'])
                    intensity_stop = float(self.au_timeline_values[au_timeline][au_event]['intensity_stop'])
                    apex_start = float(self.au_timeline_values[au_timeline][au_event]['apex_start'])
                    apex_stop = float(self.au_timeline_values[au_timeline][au_event]['apex_stop'])
                    apex_intensity_start = float(self.au_timeline_values[au_timeline][au_event]['apex_intensity_start'])
                    apex_intensity_stop = float(self.au_timeline_values[au_timeline][au_event]['apex_intensity_stop'])

                    if (index_au >= image_start and index_au <= apex_start) or (index_au >= apex_start and index_au <= apex_stop) or (index_au >= apex_stop and index_au <= image_stop):
                    
                       if (index_au >= image_start and index_au <= apex_start):
                          intensity_button_value = self.calcIntensity(nb_images, index_image, intensity_start, apex_intensity_start, image_start, apex_start)
                       elif (index_au >= apex_start and index_au <= apex_stop):
                          intensity_button_value = self.calcIntensity(nb_images, index_image, apex_intensity_start, apex_intensity_stop, apex_start, apex_stop)
                       elif (index_au >= apex_stop and index_au <= image_stop):
                          intensity_button_value = self.calcIntensity(nb_images, index_image, apex_intensity_stop, intensity_stop, apex_stop, image_stop)
                      
                       if intensity_button_value >= 0:
                          self.modifiers_sliders[au_timeline].onChanging(intensity_button_value)
                          self.modifiers_sliders[au_timeline].update()
                          self.modifiers_sliders[au_timeline].setValue(intensity_button_value)
                

    def calcIntensity(self, nb_images, index_image, intensity_start, intensity_stop, image_start, image_stop):
        nb_images, index_image, intensity_start, intensity_stop, image_start, image_stop = \
            float(nb_images), float(index_image), float(intensity_start), float(intensity_stop), float(image_start), float(image_stop)
        
        au_intensity = intensity_start + (((intensity_stop - intensity_start)/((image_stop*nb_images)-(image_start*nb_images))) * (index_image - (image_start*nb_images)))

        return au_intensity

    def calcIntensityMix(self, nb_images, index_image, intensity_start, intensity_stop, image_start, image_stop):
        nb_images, index_image, intensity_start, intensity_stop, image_start, image_stop = \
            float(nb_images), float(index_image), float(intensity_start), float(intensity_stop), float(image_start), float(image_stop)
    
        au_intensity = intensity_start + (((intensity_stop - intensity_start)/((image_stop*nb_images)-(image_start*nb_images))) * (index_image - (image_start*nb_images)))

        return au_intensity
          
##########################################################################
# Set position and intensity form anim file 
# for the start and stop position
##########################################################################

    def sliderIntensitySetFromAnim(self, position="start"):
        progress_loadFaniFile = Progress(len(self.au_timeline_values))

        for au_timeline in self.au_timeline_values.keys():
            aus_image_start = 1
            aus_image_stop  = 0

            for au_event in self.au_timeline_values[au_timeline].keys():
                
                if position == 'start':
                   if float(self.au_timeline_values[au_timeline][au_event]['image_start']) <= aus_image_start:
                      aus_image_start  = float(self.au_timeline_values[au_timeline][au_event]['image_start'])
                      slider_intensity = float(self.au_timeline_values[au_timeline][au_event]['intensity_start'])
                else:   
                   if float(self.au_timeline_values[au_timeline][au_event]['image_stop']) >= aus_image_stop:
                      aus_image_stop   = float(self.au_timeline_values[au_timeline][au_event]['image_stop'])
                      slider_intensity = float(self.au_timeline_values[au_timeline][au_event]['intensity_stop'])

            self.modifiers_sliders[au_timeline].onChanging(slider_intensity)
            self.modifiers_sliders[au_timeline].update()
            self.modifiers_sliders[au_timeline].setValue(slider_intensity)
            # self.slidersValues[au_timeline] = slider_intensity
            # self.labelSlider[au_timeline].setTextFormat( 'Intensity: %.2f%%', slider_intensity*100)
            gui3d.app.statusPersist('Loading : ' + au_timeline)
            progress_loadFaniFile.step()

        self.facs_human.applyAllTargets()
        self.refreshAuSmoothSetting()
        
 
##########################################################################
# Load Aus Timeline .fani (json file)
# Get files from facsanim directory in user data MH
##########################################################################

    def loadAusTimelineFile(self, path_to_file):
        for event_key, event_au in self.au_timeline_box.items():
            event_au.removeAu()
        self.au_timeline_values = {}
        
        self.au_timeline_values = json.loads(open(path_to_file).read())
        (dir_f, file_f) = os.path.split(path_to_file)
        self.txt_animatiom_file_loaded.setText('File: ' + file_f)
        
        self.sliderIntensitySetFromAnim('start')
        
        self.animation_test.onChange(0)
        self.animation_test.setValue(0)
        self.animation_test.update()
        
        self.createAuSliderFromFani(self)
        #self.general_intensity_progress_bar.setProgress(1)
        # self.au_coding.setText(self.getAuFacialCode())
        gui3d.app.statusPersist(path_to_file + ' loaded')
        self.facs_human.applyAllTargets()
        self.refreshAuSmoothSetting()
        
    def createAuSliderFromFani(self, this_task_view):
        log.message('autime %s', sorted(self.au_timeline_values.keys()))
        for au_timeline in sorted(self.au_timeline_values.keys()):
            for au_event in self.au_timeline_values[au_timeline].keys():
                image_start = float(self.au_timeline_values[au_timeline][au_event]['image_start'])
                image_stop = float(self.au_timeline_values[au_timeline][au_event]['image_stop'])
                intensity_start = float(self.au_timeline_values[au_timeline][au_event]['intensity_start'])
                intensity_stop = float(self.au_timeline_values[au_timeline][au_event]['intensity_stop'])
                apex_start = float(self.au_timeline_values[au_timeline][au_event]['apex_start'])
                apex_stop = float(self.au_timeline_values[au_timeline][au_event]['apex_stop'])
                apex_intensity_start = float(self.au_timeline_values[au_timeline][au_event]['apex_intensity_start'])
                apex_intensity_stop = float(self.au_timeline_values[au_timeline][au_event]['apex_intensity_stop'])

                self.au_timeline_box[str(au_event)] = FacsTimeLineSlider(this_task_view, au_timeline, au_event,
                                                                         image_start, image_stop,
                                                                         intensity_start, intensity_stop,
                                                                         apex_start, apex_stop,
                                                                         apex_intensity_start, apex_intensity_stop)

##########################################################################
# Load and save buttons definition
# Use the facs's file format
# Get files from facs directory in user data MH
##########################################################################

    def loadFacsFile(self, path_to_file):
        try:
            au_facs_loaded_file_values = json.loads(open(path_to_file).read())
        except IOError as e:
            log.message("I/O error(%s): %s", e.errno, e.strerror)
            gui3d.app.statusPersist('Nothing to render')
        else:
            au_facs_loaded_file_values = json.loads(open(path_to_file).read())
            progress_loadFacsFile = Progress(len(au_facs_loaded_file_values))
            for au_key, au_key_value in sorted(au_facs_loaded_file_values.items()):
                au_event = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
                # self.user_add_facs_intesity_pattern = 'all' # all = all ; zerotofull = 0 to full ; fulltozero = full to 0
                # if self.user_add_facs_intesity_pattern == 'zerotofull':
                   # facs_intensity_start = 0
                   # facs_intensity_stop = float(au_key_value)
                   # facs_apex_intensity_start = float(au_key_value/3)
                   # facs_apex_intensity_stop = float(au_key_value*2/3)
                # elif self.user_add_facs_intesity_pattern == 'fulltozero':
                   # facs_intensity_start = float(au_key_value)
                   # facs_intensity_stop = float(0)
                   # facs_apex_intensity_start = float(au_key_value*2/3)
                   # facs_apex_intensity_stop = float(au_key_value/3)
                # else:
                   # facs_intensity_start = float(au_key_value)
                   # facs_intensity_stop = float(au_key_value)
                   # facs_apex_intensity_start = float(au_key_value)
                   # facs_apex_intensity_stop = float(au_key_value)
                   
# To do refaire les calculs d'intensités                   
                   
                self.au_timeline_box[str(au_event)] = FacsTimeLineSlider(self, au_key, au_event, image_start = self.slider_image_start_tool.getValue(),
                                                                                                 image_stop= self.slider_image_stop_tool.getValue(),
                                                                                                 intensity_start = float(au_key_value*self.slider_intensity_start_tool.getValue()),
                                                                                                 intensity_stop = float(au_key_value*self.slider_intensity_stop_tool.getValue()),
                                                                                                 apex_start = self.slider_apex_start_tool.getValue(),
                                                                                                 apex_stop = self.slider_apex_stop_tool.getValue(),
                                                                                                 apex_intensity_start = float(au_key_value*self.slider_apex_intensity_start_tool.getValue()),
                                                                                                 apex_intensity_stop = float(au_key_value*self.slider_apex_intensity_stop_tool.getValue()))

                # self.au_timeline_box[str(au_event)] = FacsTimeLineSlider(self, au_key, au_event, intensity_start = facs_intensity_start, intensity_stop = facs_intensity_stop, apex_intensity_start = facs_apex_intensity_start, apex_intensity_stop = facs_apex_intensity_stop)
                self.addAuTimelineValues(au_key, au_event, image_start = self.slider_image_start_tool.getValue(),
                                                           image_stop= self.slider_image_stop_tool.getValue(),
                                                           intensity_start = float(au_key_value*self.slider_intensity_start_tool.getValue()),
                                                           intensity_stop = float(au_key_value*self.slider_intensity_stop_tool.getValue()),
                                                           apex_start = self.slider_apex_start_tool.getValue(),
                                                           apex_stop = self.slider_apex_stop_tool.getValue(),
                                                           apex_intensity_start = float(au_key_value*self.slider_apex_intensity_start_tool.getValue()),
                                                           apex_intensity_stop = float(au_key_value*self.slider_apex_intensity_stop_tool.getValue()))
                gui3d.app.statusPersist('Loading : ' + au_key)
                progress_loadFacsFile.step()
            self.sliderIntensitySetFromAnim('start')
            self.facs_human.applyAllTargets()
            self.refreshAuSmoothSetting()
            gui3d.app.statusPersist(path_to_file + ' loaded')

##########################################################################
# Save Aus Timeline .fani (json file)
# Get files from facsanim directory in user data MH
##########################################################################

    def saveAusTimelineFile(self, path_to_file):
        if len(self.au_timeline_values) > 0:
           json.dump(self.au_timeline_values, open(path_to_file, 'w'), indent=4)
           log.message("Saved FACS animation as %s" % path_to_file)
           gui3d.app.statusPersist(path_to_file + ' saved')
        else:
            G.app.prompt('Warning',
                         'Nothing to save.',
                         'Ok')


##########################################################################
# Retreive AU Timeline Values from AU's event
##########################################################################

    def getAuTimelineValues(self, au_timeline, event_timeline):
        return self.au_timeline_values[au_timeline][event_timeline]

##########################################################################
# Set AU Timeline Values from AU's event
##########################################################################
    
    def setAuTimelineValues(self, au_timeline, event_timeline,
                                  image_start = 0, image_stop= 1,
                                  intensity_start = 0, intensity_stop = 1,
                                  apex_start = 0.33, apex_stop = 0.66,
                                  apex_intensity_start = 0.25, apex_intensity_stop = 0.75):
                                  
        self.au_timeline_values[au_timeline][au_event]['image_start']  = float(image_start)    
        self.au_timeline_values[au_timeline][au_event]['image_stop'] = float(image_stop)      
        self.au_timeline_values[au_timeline][au_event]['intensity_start'] = float(intensity_start)
        self.au_timeline_values[au_timeline][au_event]['intensity_stop'] = float(intensity_stop)  
        self.au_timeline_values[au_timeline][au_event]['apex_start'] = float(apex_start)      
        self.au_timeline_values[au_timeline][au_event]['apex_stop'] = float(apex_stop)        
        self.au_timeline_values[au_timeline][au_event]['apex_intensity_start'] = float(apex_intensity_start)
        self.au_timeline_values[au_timeline][au_event]['apex_intensity_stop'] = float(apex_intensity_stop)

        
##########################################################################
# Add event Timeline Values to AU list
##########################################################################
    
    def addAuTimelineValues(self, au_timeline, au_event = 0,
                                  image_start = 0, image_stop= 1,
                                  intensity_start = 0, intensity_stop = 1,
                                  apex_start = 0.33, apex_stop = 0.66,
                                  apex_intensity_start = 0.25, apex_intensity_stop = 0.75):
        
        if au_timeline not in self.au_timeline_values:
           self.au_timeline_values[au_timeline] = {au_event: {"image_start": float(image_start),
                                                              "image_stop": float(image_stop),
                                                              "intensity_start": float(intensity_start),
                                                              "intensity_stop": float(intensity_stop),
                                                              "apex_start": float(apex_start),
                                                              "apex_stop": float(apex_stop),
                                                              "apex_intensity_start": float(apex_intensity_start),
                                                              "apex_intensity_stop": float(apex_intensity_stop)}}
        else:
            self.au_timeline_values[au_timeline][au_event] = {"image_start": float(image_start),
                                                              "image_stop": float(image_stop),
                                                              "intensity_start": float(intensity_start),
                                                              "intensity_stop": float(intensity_stop),
                                                              "apex_start": float(apex_start),
                                                              "apex_stop": float(apex_stop),
                                                              "apex_intensity_start": float(apex_intensity_start),
                                                              "apex_intensity_stop": float(apex_intensity_stop)}
                                                  
        
        # self.au_timeline_values[au_timeline][au_event]['image_start']  =     
        # self.au_timeline_values[au_timeline][au_event]['image_stop'] = float(image_stop)      
        # self.au_timeline_values[au_timeline][au_event]['intensity_start'] = float(intensity_start)
        # self.au_timeline_values[au_timeline][au_event]['intensity_stop'] = float(intensity_stop)  
        # self.au_timeline_values[au_timeline][au_event]['apex_start'] = float(apex_start)      
        # self.au_timeline_values[au_timeline][au_event]['apex_stop'] = float(apex_stop)        
        # self.au_timeline_values[au_timeline][au_event]['apex_intensity_start'] = float(apex_intensity_start)
        # self.au_timeline_values[au_timeline][au_event]['apex_intensity_stop'] = float(apex_intensity_stop)

##########################################################################
# Add event Timeline Values to AU list
##########################################################################
    
    def delAuTimelineEvent(self, au_timeline, au_event = 0):
        if au_event in self.au_timeline_values[au_timeline]:
           del self.au_timeline_values[au_timeline][au_event]
           log.message('self.au_timeline_values[au_timeline] %s', self.au_timeline_values[au_timeline])
           if len(self.au_timeline_values[au_timeline]) == 0:
              del self.au_timeline_values[au_timeline]
##########################################################################
# Set AU Timeline Values for one AU's event and one parameter
##########################################################################
    
    def setOneAuTimelineValue(self, au_timeline, au_event, event_parameter, value_parameter):
        self.au_timeline_values[au_timeline][au_event][event_parameter]  = float(value_parameter)    

##########################################################################
# Reset button function, if erase_all == True erase the anim dict
##########################################################################

    def resetFacialCodes(self, erase_all='True'):
        progress_reset_button = Progress(len(self.modifiers_sliders))
        for aSlider in self.modifiers_sliders.keys():
            #if self.slidersValues[aSlider] >= 0:
            self.modifiers_sliders[aSlider].resetValue()
            self.modifiers_sliders[aSlider].update()
            gui3d.app.statusPersist('Reseting : ' + aSlider)
            progress_reset_button.step()

        if erase_all:
           self.au_timeline_values = {}
           self.au_facs_loaded_file_values = {}
           self.txt_animatiom_file_loaded.setText('No animation file loaded')

        progress_reset_button.step()
        self.animation_test.onChange(0)
        self.animation_test.setValue(0)
        self.animation_test.update()

        # self.au_coding.setText('Neutral')
        # self.txt_file_loaded.setText('- New facial code -')        
        self.facs_human.applyAllTargets()
        self.refreshAuSmoothSetting()
        gui3d.app.statusPersist('Reset is done, now in neutral facial expression setting')

##########################################################################
# Reset button for camera's orientation to have full face view
# in order to have constant point of view for experiments
##########################################################################
    def resetCamera(self):
        gui3d.app.setTargetCamera(131, 9, False)
        gui3d.app.axisView([0.0, 0.0, 0.0])
        gui3d.app.statusPersist('Camera updated')            

##########################################################################
# System calls
##########################################################################
        
    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)
        
        #gui3d.app.setTargetCamera(131, 9)
        #gui3d.app.axisView([0.0, 0.0, 0.0])
        gui3d.app.statusPersist('FACSHuman a tool to create facial expression based on the Paul Ekman Facial Action Coding System')
        gui3d.app.backplaneGrid.setVisibility(False)
        gui3d.app.backgroundGradient.mesh.setColors([0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0])
        #G.app.setScene(scene.Scene(G.app.scene.file.path))
        # self.resetCamera()
        #facs_human.material.shader = getpath.getSysDataPath(self.taskViewShader) if self.taskViewShader else None array([  0.        ,   7.22596645,  18.91166067])

        
    def onHide(self, event):
        gui3d.app.statusPersist('')

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addTask(FACSTest(category, app))


def unload(app):
    pass

    
