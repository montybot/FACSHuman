#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

""" 
**Project Name:**      FACSHuman main plugin
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

import camera
from OpenGL.GL import *
import numpy as np

import datetime
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
import glmodule
import image
from image import Image
import image_operations as imgop
# import guirender
from core import G
from progress import Progress

##########################################################################
# Class definiton for each sliders mhEvent
##########################################################################
class FACSslider(object):

      def __init__(self, slider, labelSlider, slidersValues, label_create):
                  
          @slider.mhEvent
          def onChange(value):
              #log.message('toto %s %s %s', labelSlider, slider, slidersValues)
              labelSlider.setTextFormat( 'Intensity: %.2f%%', value*100)
              slidersValues[label_create] = value
              #log.message('titi %s, %s', slidersValues, slidersValues[label_create])

              
##########################################################################
# Main Class for FACSHuman plugin
##########################################################################

class FACSHumanTaskView2(gui3d.TaskView):

    def __init__(self, category, appFacs):
        gui3d.TaskView.__init__(self, category, 'FACSHuman 0.1')
        self.facs_human = appFacs.selectedHuman
        camera = G.app.modelCamera
        self.app = appFacs
#For the ffmpeg video generation
        self.last_directory_rendering = ''
        self.images_to_convert = ''
        self.video_destination = ''
        #self.video_background = 'black.jpg'
        self.renderingWidth = '500'
        self.renderingHeight = '500'
        self.images_set_dir_destination = ''
        
##########################################################################
# Targets paths definition MH user data directory
##########################################################################

        self.targets_path_emotions_blender = getpath.getPath('data/FACSHuman/00 Emotions')
        self.targets_path_upper_face = getpath.getPath('data/FACSHuman/01 Upper Face AUs')
        self.targets_path_lower_face = getpath.getPath('data/FACSHuman/02 Lower Face AUs')
        self.targets_path_lip_jaw = getpath.getPath('data/FACSHuman/03 Lip Parting and Jaw Opening')
        self.targets_path_eye = getpath.getPath('data/FACSHuman/04 Eye Positions')
        self.targets_path_head = getpath.getPath('data/FACSHuman/05 Head Positions')
        self.targets_path_misc = getpath.getPath('data/FACSHuman/06 Miscellaneous AUs')

##########################################################################
# GroupBox definitions for widgets
##########################################################################
        
        box_emotions_blender = self.addLeftWidget(gui.GroupBox('Emotions blender'))
        box_upper = self.addLeftWidget(gui.GroupBox('Upper Face AUs'))
        box_lower = self.addLeftWidget(gui.GroupBox('Lower Face AUs'))
        box_head = self.addLeftWidget(gui.GroupBox('Head Positions'))
        box_eye = self.addLeftWidget(gui.GroupBox('Eye Positions'))
        box_lip = self.addLeftWidget(gui.GroupBox('Lip Parting and Jaw Opening'))
        box_misc = self.addLeftWidget(gui.GroupBox('Miscellaneous AUs'))
        box_tools = self.addRightWidget(gui.GroupBox('Tools'))
        box_aus_code = self.addRightWidget(gui.GroupBox('Action Units coding'))
        box_images_rendering = self.addRightWidget(gui.GroupBox('Images set creation'))
        box_animation = self.addRightWidget(gui.GroupBox('Animation'))
        box_videos_rendering = self.addRightWidget(gui.GroupBox('Video creation'))

##########################################################################
# Widgets definitions for Box Tools
##########################################################################

# AUs box
        self.general_intensity = box_aus_code.addWidget(gui.Slider(value=100, min=0, max=100, label=['General Intensity : ','%d%%']), columnSpan = 2)
        #self.general_intensity_progress_bar = box_tools.addWidget(gui.ProgressBar())
        #self.general_intensity_progress_bar.setProgress(1)
        self.txt_file_loaded = box_aus_code.addWidget(gui.TextView('- New facial code -'), columnSpan = 2)
        self.load_facs_button = box_aus_code.addWidget(gui.BrowseButton('open', "Load FACS Code"), 3, 0)
        self.save_facs_button = box_aus_code.addWidget(gui.BrowseButton('save', "Save FACS Code"), 3, 1)
        # self.save_target_button = box_aus_code.addWidget(gui.BrowseButton('save', "Save target"))
        self.generate_au_coding_button = box_aus_code.addWidget(gui.Button('Get AU\'s Code'), columnSpan = 2)
        self.txt_coding = box_aus_code.addWidget(gui.TextView('AU\'s code generated :'), columnSpan = 2)
        self.au_coding = box_aus_code.addWidget(gui.DocumentEdit(text='Neutral'), columnSpan = 2)

# Tools box
        self.reset_camera_button = box_tools.addWidget(gui.Button('Full face camera view'), columnSpan = 2)
        #self.txt_reset_button_warning = box_tools.addWidget(gui.TextView('Be careful with this button !'))
        #self.test_button = box_tools.addWidget(gui.BrowseButton('open', "Set scene"))
        #self.refresh_button = box_tools.addWidget(gui.Button('Refresh True'))
        #self.refresha_button = box_tools.addWidget(gui.Button('Refresh False'))
        self.one_shot_button = box_tools.addWidget(gui.Button('Take one shot'), 1, 0)
        self.one_shot_stereo_button = box_tools.addWidget(gui.Button('Stereoscopic shot'),1, 1)
        self.au_set_gen_button = box_tools.addWidget(gui.BrowseButton('open', "Dir to img"), 2, 0)
        self.material_gen_button = box_tools.addWidget(gui.BrowseButton('open', "Images set"), 2, 1)
        self.material_gen_dir_button = box_tools.addWidget(gui.FileEntryView('Browse', mode='dir'), columnSpan = 2)
        self.camera_slider_x = box_tools.addWidget(gui.Slider(value=0, min=-1, max=1, label=['camera x: ','%2f']), columnSpan = 2)
        self.camera_slider_y = box_tools.addWidget(gui.Slider(value=0, min=-1, max=1, label=['camera y: ','%2f']), columnSpan = 2)
        self.camera_slider_zoom = box_tools.addWidget(gui.Slider(value=0, min=4, max=9, label=['Zoom: ','%2f']), columnSpan = 2)
        self.rotation_slider_z = box_tools.addWidget(gui.Slider(value=0, min=-90, max=90, label=['rotation z: ','%2f']), columnSpan = 2)
        self.reset_button = box_tools.addWidget(gui.Button('Reset Facial Code'), columnSpan = 2)
        self.full_set_button = box_tools.addWidget(gui.Button('Full set generation'), columnSpan = 2)
        self.facsvatar_set_button = box_tools.addWidget(gui.BrowseButton('open', 'FACAvatar rendering'), columnSpan = 2)
       
# Image rendering box
        self.txt_image_number_to_render = box_images_rendering.addWidget(gui.TextView('Number of images to generate'))
        self.images_number_to_render = box_images_rendering.addWidget(gui.TextEdit(text='25'))
        self.txt_image_size_to_render = box_images_rendering.addWidget(gui.TextView('Image size'))
        self.images_size_to_render = box_images_rendering.addWidget(gui.TextEdit(text='500x500'))
        #self.scene_activation_button = box_tools.addWidget(gui.Button('Use scene for rendering'))
        self.scene_reverse_chekbox = box_images_rendering.addWidget(gui.CheckBox('Neutral to neutral image rendering'))
        self.render_timelined_video_chekbox = box_images_rendering.addWidget(gui.CheckBox('Render timelined animation'))
        self.render_images_set_button = box_images_rendering.addWidget(gui.Button('Render images'))

# Animation box
        self.txt_animatiom_file_loaded = box_animation.addWidget(gui.TextView('No animation file loaded'))
        self.txt_images_number_neutral_to_anim_start = box_animation.addWidget(gui.TextView('Images number from neutral to start anim'))
        self.images_number_neutral_to_anim_start = box_animation.addWidget(gui.TextEdit(text='0'))
        self.txt_images_number_neutral_to_anim_stop = box_animation.addWidget(gui.TextView('Images number from stop to neutral anim'))
        self.images_number_neutral_to_anim_stop = box_animation.addWidget(gui.TextEdit(text='0'))
        self.load_animation_button =  box_animation.addWidget(gui.BrowseButton('open', "Load AUs animation timeline"))
        #self.render_timelined_video_button = box_images_rendering.addWidget(gui.Button('Render timelined animation'))
        #self.index_timeline = box_images_rendering.addWidget(gui.TextEdit(text='1'))
        self.animation_test = box_animation.addWidget(gui.Slider(value=0.00, min=0.00, max=25, label=['Animation frame test : ','%d']))

# Video box     
        self.render_video_frame_rate_label = box_videos_rendering.addWidget(gui.TextView('Images by seconde'))
        self.render_video_frame_rate = box_videos_rendering.addWidget(gui.TextEdit(text='25'))
        self.frame_number_pause_label = box_videos_rendering.addWidget(gui.TextView('Number of frames to pause'))
        self.frame_number_pause = box_videos_rendering.addWidget(gui.TextEdit(text='0'))
        self.number_of_time_pause_label = box_videos_rendering.addWidget(gui.TextView('Number of loops to pause'))
        self.number_of_time_pause = box_videos_rendering.addWidget(gui.TextEdit(text='0'))
        self.starting_frame_pause_label = box_videos_rendering.addWidget(gui.TextView('Index of the first pause frame'))
        self.starting_frame_pause = box_videos_rendering.addWidget(gui.TextEdit(text='0'))
        self.render_video_button = box_videos_rendering.addWidget(gui.Button('Render video'))
        self.play_last_rendered_video_button = box_videos_rendering.addWidget(gui.Button('Play last rendered video'))

##########################################################################
# .json Au's list loading
##########################################################################

        self.facs_code_names_path = getpath.getDataPath('FACSHuman')
        self.facs_code_names_file = self.facs_code_names_path + '/au.json'
        self.facs_code_names = json.loads(open(self.facs_code_names_file).read())
        # log.message("aujson %s", self.facs_code_names)

##########################################################################
# Sliders / modifiers / Label dictionnaries
##########################################################################

        self.slidersValues = {} #Keep a trace of values in the General intensity sliders function
        self.sliders = {}
        self.sliders_order = []
        self.labelSlider = {}
        #self.modifiers = {}
        self.au_timeline_values = {} # For the animation functionality
        self.au_facs_loaded_file_values = {} # For the animation functionality
        

###########################################################################################
# Sliders creation with targets files in FACSHuman directory in user data directory
###########################################################################################     
        
        self.searchTargets(self.targets_path_emotions_blender, box_emotions_blender, 'Emotions Blender')
        self.searchTargets(self.targets_path_upper_face, box_upper, 'Upper Face AUs')
        self.searchTargets(self.targets_path_lower_face, box_lower, 'Lower Face AUs')
        self.searchTargets(self.targets_path_lip_jaw, box_lip, 'Lip Parting and Jaw Opening')
        self.searchTargets(self.targets_path_eye, box_eye, 'Eye Positions')
        self.searchTargets(self.targets_path_head, box_head, 'Head Positions')
        self.searchTargets(self.targets_path_misc, box_misc, 'Miscellaneous AUs')

##########################################################################
# Load and save button for .facs file's type (json format)
##########################################################################

        self.load_facs_button.setFilter("FACS code file (*.facs)")
        self.save_facs_button.setFilter("FACS code file (*.facs)")
        self.load_animation_button.setFilter("Aus animation timeline (*.fani)")
        self.save_path = getpath.getDataPath('facs')
        
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        self.load_facs_button.setDirectory(self.save_path )
        self.load_animation_button.setDirectory(self.save_path )
        self.save_facs_button.setDirectory(self.save_path )
        
#        @self.refresh_button.mhEvent
#        def onClicked(path):
#            self.facs_human.updateSubdivisionMesh(True)
            #self.facs_human.mesh.calcNormals()
            #self.facs_human.mesh.update()
            #self.facs_human.setSubdivided(True)

##########################################################################
# Generate all AUs images
##########################################################################

        @self.camera_slider_x.mhEvent
        def onChanging(value):
            pos = self.facs_human.getPosition()
            pos[0] = value
            self.facs_human.setPosition(pos)
            mh.redraw()
            
        @self.camera_slider_y.mhEvent
        def onChanging(value):
            pos = self.facs_human.getPosition()
            pos[1] = value
            self.facs_human.setPosition(pos)
            mh.redraw()

        @self.camera_slider_zoom.mhEvent
        def onChanging(value):
            camera.setZoomFactor(value)

        @self.rotation_slider_z.mhEvent
        def onChanging(value):
            pos = self.facs_human.getRotation()
            pos[1] = value
            self.facs_human.setRotation(pos)
            mh.redraw()
           
##########################################################################
# Generate all AUs images
##########################################################################

        @self.facsvatar_set_button.mhEvent
        def onClicked(path):
            self.generateFacsvatarDirSet(path)

##########################################################################
# Generate all AUs images
##########################################################################

        @self.au_set_gen_button.mhEvent
        def onClicked(path):
            self.generateDirSet(path)

##########################################################################
# Generate material images
##########################################################################

        @self.material_gen_button.mhEvent
        def onClicked(path):
            self.generateCompleteImagesSetFromDir(path)
##########################################################################
# Generate material images
##########################################################################

        @self.material_gen_dir_button.mhEvent
        def onFileSelected(event):
            # self.images_set_dir_destination = os.path.dirname(path)
            self.images_set_dir_destination = event.path
            # self.images_set_dir_destination = os.path.dirname(path)
            gui3d.app.statusPersist('Images destination : ' + str(self.images_set_dir_destination))

# Load Button
        @self.load_facs_button.mhEvent
        def onClicked(path):
            if path:
               self.resetFacialCodes()
               self.loadFacsFile(path)
# Save Button
        @self.save_facs_button.mhEvent
        def onClicked(path):
            if path:
                if not os.path.splitext(path)[1]:
                    path = path + ".facs"
                self.saveCurrentFACS(path)        
                
                
# Save target Button
        # @self.save_target_button.mhEvent
        # def onClicked(path):
            # if path:
                # if not os.path.splitext(path)[1]:
                    # path = path + ".target"
                # G.app.saveTarget(path)
                
###########################################################################################
# Load and render button for .fani file's type (json format) Timeline for AUs animation
###########################################################################################     

        @self.load_animation_button.mhEvent
        def onClicked(path):
            if path:
               self.resetFacialCodes()
               self.loadAusTimelineFile(path)

        #@self.render_timelined_video_button.mhEvent
        #def onClicked(event):
        #    self.slidersSequencerRenderImageSet(self.index_timeline.getText())
        #    #self.renderImagesSet(True)
        

##########################################################################
# Reset button for camera's orientation to have full face view
# in order to have constant point of view for experiments
##########################################################################
                
        @self.reset_camera_button.mhEvent
        def onClicked(event):
            gui3d.app.setTargetCamera(131, 9, False)
            gui3d.app.axisView([0.0, 0.0, 0.0])
            pos = [0, 0.2, 0]
            self.facs_human.setPosition(pos)
            self.camera_slider_x.setValue(0) 
            self.camera_slider_y.setValue(0.2)
            self.camera_slider_zoom.setValue(9)
            self.rotation_slider_z.setValue(0)
            self.rotation_slider_z.onChanging(0)
            self.rotation_slider_z.update()
            mh.redraw()
            gui3d.app.statusPersist('Camera updated')

##########################################################################
# Generate an AU's inventory and an intensity evaluation
# See page 8 of the FACS Manual for the definition of the intensity
# For this implementation in MH I choose this % scale value :
# A Trace               -> 10 % Intensity = 10%
# B Slight              -> 10 % Intensity = 20%
# C Marked pronounced   -> 35 % Intensity = 55%
# D Severe extreme      -> 35 % Intensity = 90%
# E Maximum             -> 10 % Intensity = 100%
##########################################################################
 
        @self.generate_au_coding_button.mhEvent
        def onClicked(event):
            self.au_coding.setText(self.getAuFacialCode())

 
##########################################################################
# Reset facial code and AUs button
##########################################################################
       
        @self.reset_button.mhEvent
        def onClicked(event):
            G.app.prompt('Confirmation',
                    'Do you really want to reset your Facial code ?',
                    'Yes', 'Cancel', self.resetFacialCodes)
                    
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
# General intensity slider definition
##########################################################################

        @self.general_intensity.mhEvent
        def onChange(value):
            self.generalIntensitySliderRender(value, True)
            # self.facs_human.applyAllTargets()
            # self.refreshAuSmoothSetting()

##########################################################################
# Animation test slider definition
##########################################################################
 
        @self.animation_test.mhEvent
        def onChanging(value):
            self.slidersSequencerRenderImageSet(value)

##########################################################################
# Image / picture size definition
##########################################################################

        @self.images_size_to_render.mhEvent
        def onChange(value):
            #log.message('picturesize : %s %s %s', self.renderingWidth, self.renderingHeight, value)
            try:
                value = value.replace(" ", "")
                res = [x for x in value.split("x")]
                self.renderingWidth = res[0]
                self.renderingHeight = res[1]
                #log.message('picturesize : %s %s', self.renderingWidth, self.renderingHeight)
            except:  # The user hasn't typed the value correctly yet.
                pass

##########################################################################
# self.one_shot_button Button
##########################################################################

        @self.one_shot_button.mhEvent
        def onClicked(event):
            self.renderFacsPicture()
 
        @self.one_shot_stereo_button.mhEvent
        def onClicked(event):
            dir_images = datetime.datetime.now().strftime('stereo_%Y-%m-%d_%H_%M_%S')
            self.renderFacsPictureStereo(dir_images)
            
        @self.render_video_button.mhEvent
        def onClicked(event):
            log.message('Video')
            if os.path.exists(self.video_destination):
                G.app.prompt('Confirmation',
                    'A movie file already exists, overwrite it ?',
                    'Yes', 'Cancel', self.createVideoFromImages)
            else:
                self.createVideoFromImages() 

        @self.play_last_rendered_video_button.mhEvent
        def onClicked(event):
            self.play_last_rendered_video()

########################################################################
# Pictures series button definition
########################################################################

        @self.render_images_set_button.mhEvent
        def onClicked(event):
            self.renderImagesSet()
  
        @self.full_set_button.mhEvent
        def onClicked(event):
            self.generateFullSet()
  
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

         
#################################################################################
# Calculate each sliders intensity in animated rendering
#
#################################################################################
            
    def generalIntensitySliderRender(self, general_intensity_value, general_intensity_slider = False):
    
        for key_code in self.slidersValues.keys():
            if self.slidersValues[key_code] > 0:
               gi = float(general_intensity_value)
               sv = float(self.slidersValues[key_code])
               intensity_button_value = float(gi*sv/100)
               self.sliders[key_code].onChanging(intensity_button_value)
               self.sliders[key_code].update()
               self.sliders[key_code].setValue(intensity_button_value)
               self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', self.sliders[key_code].getValue()*100)
            # for key_code in self.sliders.keys():
                # if self.slidersValues[key_code] > 0:
                   # intensity_button_value = float(value*self.slidersValues[key_code]/100)
                   # self.sliders[key_code].onChanging(intensity_button_value)
                   # self.sliders[key_code].update()
                   # self.sliders[key_code].setValue(intensity_button_value)
                   # self.labelSlider[key_code].setTextFormat( 'Intensity: %.2f%%', intensity_button_value*100)
        if general_intensity_slider:
           # self.facs_human.applyAllTargets()
           self.refreshAuSmoothSetting()
           
           
        # if self.slider.isSliderDown():
            # Don't do anything when slider is being clicked or dragged (onRelease triggers it)
            # return

        # value = self.getValue()
        # human = self.modifier.human
        # if self.value is None:
            # self.value = self.modifier.getValue()
        # action = humanmodifier.ModifierAction(self.modifier, self.value, value, self.update)
        # if self.value != value:
            # G.app.do(action)
        # else:
            # Apply the change anyway, to make sure everything's updated
            # Perform the action without adding it to the undo stack
            # action.do()

        # if human.isSubdivided():
            # if human.isProxied():
                # human.getProxyMesh().setVisibility(0)
            # else:
                # human.getSeedMesh().setVisibility(0)
            # human.getSubdivisionMesh(False).setVisibility(1)
        # self.value = None
           
           
           
           
           
           
           

#################################################################################
# Calculate each sliders intensity in animated rendering
#
#                                               
#  intensity = I1 + ((I2-I1)/((Fd2xNbF)-(Fd1xNbF))) x Index - (I1xNbF)
#
#log.message('key_code : %s', type(self.sliders[key_code]))
#
#        "intensity_start": "0",
#        "intensity_stop": "1",
#        "start": "0.5",
#        "stop": "1"
#
        # for au_timeline in self.au_timeline_values.keys():
            # for au_events in self.au_timeline_values[au_timeline].keys():
                # if self.au_timeline_values[au_timeline][au_events]['image_start'] == '0':
                   # intensity_start = float(self.au_timeline_values[au_timeline][au_events]['intensity_start'])
#################################################################################

    def slidersSequencerRenderImageSet(self, index_image, nb_images = ''):
        
        if len(nb_images) == 0:
           nb_images = float(self.images_number_to_render.getText())
        else:
           nb_images = float(nb_images)

        index_au = float(index_image) / nb_images
        intensity_button_value = 0
        
        for au_timeline in self.au_timeline_values.keys():
            for au_events in self.au_timeline_values[au_timeline].keys():
                image_start = float(self.au_timeline_values[au_timeline][au_events]['image_start'])
                image_stop = float(self.au_timeline_values[au_timeline][au_events]['image_stop'])
                intensity_start = float(self.au_timeline_values[au_timeline][au_events]['intensity_start'])
                intensity_stop = float(self.au_timeline_values[au_timeline][au_events]['intensity_stop'])
                apex_start = float(self.au_timeline_values[au_timeline][au_events]['apex_start'])
                apex_stop = float(self.au_timeline_values[au_timeline][au_events]['apex_stop'])
                apex_intensity_start = float(self.au_timeline_values[au_timeline][au_events]['apex_intensity_start'])
                apex_intensity_stop = float(self.au_timeline_values[au_timeline][au_events]['apex_intensity_stop'])
                
                if (index_au >= image_start and index_au <= apex_start) or (index_au >= apex_start and index_au <= apex_stop) or (index_au >= apex_stop and index_au <= image_stop):
                
                   if (index_au >= image_start and index_au <= apex_start):
                      intensity_button_value = self.calcIntensity(nb_images, index_image, intensity_start, apex_intensity_start, image_start, apex_start)
                   elif (index_au >= apex_start and index_au <= apex_stop):
                      intensity_button_value = self.calcIntensity(nb_images, index_image, apex_intensity_start, apex_intensity_stop, apex_start, apex_stop)
                   elif (index_au >= apex_stop and index_au <= image_stop):
                      intensity_button_value = self.calcIntensity(nb_images, index_image, apex_intensity_stop, intensity_stop, apex_stop, image_stop)
                  
                   if intensity_button_value >= 0:
                      self.sliders[au_timeline].onChanging(intensity_button_value)
                      self.sliders[au_timeline].update()
                      self.sliders[au_timeline].setValue(intensity_button_value)
                      self.slidersValues[au_timeline] = intensity_button_value
                      self.labelSlider[au_timeline].setTextFormat( 'Intensity: %.2f%%', intensity_button_value*100)
                
        # gui3d.app.statusPersist('i: %s s: ', self.au_timeline_values)

    def calcIntensity(self, nb_images, index_image, intensity_start, intensity_stop, image_start, image_stop):
        nb_images, index_image, intensity_start, intensity_stop, image_start, image_stop = \
            float(nb_images), float(index_image), float(intensity_start), float(intensity_stop), float(image_start), float(image_stop)
        au_intensity = intensity_start + (((intensity_stop - intensity_start)/((image_stop*nb_images)-(image_start*nb_images))) * (index_image - (image_start*nb_images)))

        
        # intensity_start 1.0 intensity_stop 1.0 image_stop 0.0 nb_images 25.0 image_start 0.0 index_image 0.0

        return au_intensity
##########################################################################
# Render images set method
##########################################################################

    def renderImagesSet(self, timeline=False, dir_destination = None, dir_name = None):
        nb_images = int(self.images_number_to_render.getText())
        if nb_images > 0:
           #gui3d.app.statusPersist('%s %s', self.images_number_to_render.getText(), type(nb_images))
           if dir_destination is None:
              if self.images_set_dir_destination != '':
                 dir_images_path = self.images_set_dir_destination
                 dir_images = datetime.datetime.now().strftime('images_%Y-%m-%d_%H_%M_%S')
              else:
                dir_images = datetime.datetime.now().strftime('images_%Y-%m-%d_%H_%M_%S')
                dir_images_path = mh.getPath('grab')
           else:
              dir_images = dir_name
              dir_images_path = dir_destination


           self.last_directory_rendering = dir_images_path + '/' + dir_images
           dir_images_path = os.path.join(dir_images_path, dir_images)

           if not os.path.exists(dir_images_path):
              os.makedirs(dir_images_path)

           nb_image_neutral_timeline_start = int(self.images_number_neutral_to_anim_start.getText())
           nb_image_neutral_timeline_stop  = int(self.images_number_neutral_to_anim_stop.getText())
 

           if self.render_timelined_video_chekbox.selected and self.scene_reverse_chekbox.selected and len(self.au_timeline_values) > 0:
              
              self.resetFacialCodes(False)
              self.sliderIntensitySetFromAnim("start")
              
              self.generalIntensitySliderRender(0) # self.general_intensity.onChange(0)   
              self.renderFacsPicture(dir_images_path, '0')
              progress_render_images = Progress(nb_image_neutral_timeline_start)

              # Render neutral images before timeline
              for i in range(1, nb_image_neutral_timeline_start + 1):
                  value_intensity = i*100/nb_image_neutral_timeline_start
                  self.generalIntensitySliderRender(value_intensity) #self.general_intensity.onChange(value_intensity)
                  gui3d.app.statusPersist("Rendering neutral to animation images %s of %s", i ,nb_image_neutral_timeline_start)
                  picture_name = str(i)
                  self.renderFacsPicture(dir_images_path, picture_name)
                  progress_render_images.step()

              self.generalIntensitySliderRender(100) #self.general_intensity.onChange(100)
              progress_render_images = Progress(nb_images)

              # Render the Timeline
              for i in range(1, nb_images + 1):
                  self.slidersSequencerRenderImageSet(i)
                  gui3d.app.statusPersist("Rendering timeline images %s of %s", i ,nb_images)
                  picture_name = str(i+nb_image_neutral_timeline_start)
                  self.renderFacsPicture(dir_images_path, picture_name)
                  progress_render_images.step()

              self.sliderIntensitySetFromAnim("stop")
              progress_render_images = Progress(nb_image_neutral_timeline_stop)

              # Render neutral images after timeline
              for i in range(nb_images + 1, nb_images + nb_image_neutral_timeline_stop + 1):
                  value_intensity = 100-((i - nb_images + 1)*100)/((nb_images + nb_image_neutral_timeline_stop + 1)-nb_images+1)
                  self.generalIntensitySliderRender(value_intensity) #self.general_intensity.onChange(value_intensity)
                  gui3d.app.statusPersist("Rendering animation to neutral images %s of %s", i - nb_images , nb_image_neutral_timeline_stop)
                  picture_name = str(i + nb_image_neutral_timeline_start)
                  self.renderFacsPicture(dir_images_path, picture_name)
                  progress_render_images.step()
           else:
               progress_render_images = Progress(nb_images)

               if self.render_timelined_video_chekbox.selected :
                  self.resetFacialCodes(False)
               else:
                  self.generalIntensitySliderRender(0) # self.general_intensity.onChange(0)   
                  self.renderFacsPicture(dir_images_path, '0')

               for i in range(1, nb_images + 1):
                   
                   if self.render_timelined_video_chekbox.selected :
                      self.slidersSequencerRenderImageSet(i)
                   else:
                       value_intensity = i*100/nb_images
                       self.generalIntensitySliderRender(value_intensity) #self.general_intensity.onChange(value_intensity)

                   picture_name = str(i)
                   
                   if self.scene_reverse_chekbox.selected:
                      picture_name_reverse = str((nb_images*2+1)-i)
                      self.renderFacsPicture(dir_images_path, picture_name, picture_name_reverse)
                   else:
                       self.renderFacsPicture(dir_images_path, picture_name)

                   gui3d.app.statusPersist("Rendering picture %s of %s", i ,nb_images)
                   progress_render_images.step()
                
           gui3d.app.statusPersist('Rendered images saved in %s', dir_images_path)
        else:
            G.app.prompt('Warning',
                         'Nothing to render check the number of images.',
                         'Ok')
       
        self.facs_human.applyAllTargets()
        self.refreshAuSmoothSetting()

##########################################################################
# Set position and intensity form anim file 
# for the start and stop position
##########################################################################

    def sliderIntensitySetFromAnim(self, position="start"):
        progress_loadFaniFile = Progress(len(self.au_timeline_values))

        for au_timeline in self.au_timeline_values.keys():
            aus_image_start = 1
            aus_image_stop  = 0

            for au_events in self.au_timeline_values[au_timeline].keys():
                
                if position == 'start':
                   if float(self.au_timeline_values[au_timeline][au_events]['image_start']) <= aus_image_start:
                      aus_image_start  = float(self.au_timeline_values[au_timeline][au_events]['image_start'])
                      slider_intensity = float(self.au_timeline_values[au_timeline][au_events]['intensity_start'])
                else:   
                   if float(self.au_timeline_values[au_timeline][au_events]['image_stop']) >= aus_image_stop:
                      aus_image_stop   = float(self.au_timeline_values[au_timeline][au_events]['image_stop'])
                      slider_intensity = float(self.au_timeline_values[au_timeline][au_events]['intensity_stop'])

            self.sliders[au_timeline].onChanging(slider_intensity)
            self.sliders[au_timeline].update()
            self.sliders[au_timeline].setValue(slider_intensity)
            self.slidersValues[au_timeline] = slider_intensity
            self.labelSlider[au_timeline].setTextFormat( 'Intensity: %.2f%%', slider_intensity*100)
            gui3d.app.statusPersist('Loading : ' + au_timeline)
            progress_loadFaniFile.step()

        self.facs_human.applyAllTargets()
        self.refreshAuSmoothSetting()
        
##########################################################################
# Reset button function, if erase_all == True erase the anim dict
##########################################################################

    def resetFacialCodes(self, erase_all='True'):
        progress_reset_button = Progress(len(self.sliders))
        was_subdivided = False
        if self.facs_human.isSubdivided():
            was_subdivided = True
            self.facs_human.setSubdivided(False)
        for aSlider in self.sliders.keys():
            #if self.slidersValues[aSlider] >= 0:
            self.sliders[aSlider].resetValue()
            self.sliders[aSlider].update()
            self.slidersValues[aSlider] = 0
            self.labelSlider[aSlider].setTextFormat('Intensity: 0%%')
            gui3d.app.statusPersist('Reseting : ' + aSlider)
            progress_reset_button.step()

        if erase_all:
           self.au_timeline_values = {}
           self.au_facs_loaded_file_values = {}
           self.txt_animatiom_file_loaded.setText('No animation file loaded')

        self.animation_test.onChange(0)
        self.animation_test.update()
        self.animation_test.setValue(0)

        self.general_intensity.onChange(100)   
        self.general_intensity.update()
        self.general_intensity.setValue(100)

        self.au_coding.setText('Neutral')
        self.txt_file_loaded.setText('- New facial code -')        
        self.facs_human.applyAllTargets()
        # self.refreshAuSmoothSetting()
        if was_subdivided == True:
            self.facs_human.setSubdivided(True)
        gui3d.app.statusPersist('Reset is done, now in neutral facial expression setting')
############################################################################################################
# Render video button definition (ffmpeg.exe -f image2 -r 60 -i %%02d.png -vcodec mpeg4 -y movie.mp4)
############################################################################################################

    def createStereoFromImages(self):
        if self.last_directory_rendering != '':
           import subprocess as sp
           import locale
           import sys
        
           encoding = locale.getpreferredencoding()

           if sys.platform == 'win32':
              console_encoding = 'cp850'
           elif sys.platform in ('linux2', 'darwin'):
              console_encoding = 'utf-8'
         
           self.images_to_convert_left = os.path.join(self.last_directory_rendering,'L.png').encode(encoding)
           self.images_to_convert_right = os.path.join(self.last_directory_rendering,'R.png').encode(encoding)
           self.image_destination = os.path.join(self.last_directory_rendering,'stereo.png').encode(encoding)
        
           FFMPEG_BIN = "ffmpeg" # on Windows
           # color_bg_video_duration = str(0.001)
           # picture_size = str(self.renderingWidth) + 'x' + str(self.renderingHeight)
           #loop=Number of frame, Number of time, Frame index
           # ffmpeg -i L.png -i R.png -filter_complex "[0:v:0]pad=iw*2:ih[bg]; [bg][1:v:0]overlay=w" stereo.png
           
           command = [FFMPEG_BIN, '-i', self.images_to_convert_left,
                                  '-i', self.images_to_convert_right,
                                  '-filter_complex', "[0:v:0]pad=iw*2:ih[bg]; [bg][1:v:0]overlay=w", self.image_destination]

           pipe = sp.Popen(command, stdout = sp.PIPE, stderr=sp.PIPE)
           a, b = pipe.communicate()
           log.message('command : %s',command)
           log.message('pipe : %s, le dir : %s',a, b)
           #self.last_directory_rendering = ''
           gui3d.app.statusPersist("Video saved to %s", self.image_destination)
        else:
            G.app.prompt('Warning',
                         'Nothing to render check the number of images.',
                         'Ok')
        
###########################################################################################################
# Render video button definition (ffmpeg.exe -f image2 -r 60 -i %%02d.png -vcodec mpeg4 -y movie.mp4)
############################################################################################################

    def createVideoFromImages(self, video_name = 'movie.mp4'):
        if self.last_directory_rendering != '':
           import subprocess as sp
           import locale
           import sys
        
           encoding = locale.getpreferredencoding()

           if sys.platform == 'win32':
              console_encoding = 'cp850'
           elif sys.platform in ('linux2', 'darwin'):
              console_encoding = 'utf-8'
         
           self.images_to_convert = os.path.join(self.last_directory_rendering,'%d.png').encode(encoding)
           self.video_destination = os.path.join(self.last_directory_rendering, str(video_name)).encode(encoding)
        
           FFMPEG_BIN = "ffmpeg" # on Windows
           color_bg_video_duration = str(0.001)
           picture_size = str(self.renderingWidth) + 'x' + str(self.renderingHeight)
           #loop=Number of frame, Number of time, Frame index
           command = [FFMPEG_BIN, '-f', 'lavfi', '-i', "color=c=black:s="+picture_size.encode(encoding)+":d="+color_bg_video_duration,
                                  '-framerate', self.render_video_frame_rate.getText().encode(encoding),
                                  '-f', 'image2', '-i', self.images_to_convert,
                                  '-filter_complex', "[0:v][1:v] overlay=0:0, loop="+self.frame_number_pause.getText().encode(encoding)+":"+self.number_of_time_pause.getText().encode(encoding)+":"+self.starting_frame_pause.getText().encode(encoding), '-vcodec', 'libx264',
                                  '-crf', '10', '-pix_fmt', 'yuv420p', '-y', self.video_destination]

           pipe = sp.Popen(command, stdout = sp.PIPE, stderr=sp.PIPE)
           a, b = pipe.communicate()
           log.message('command : %s',command)
           log.message('pipe : %s, le dir : %s',a, b)
           #self.last_directory_rendering = ''
           gui3d.app.statusPersist("Video saved to %s", self.video_destination)
        else:
            G.app.prompt('Warning',
                         'Nothing to render check the number of images.',
                         'Ok')
############################################################################################################
# Play last rendered video button definition (ffmpeg.exe -f image2 -r 60 -i %%02d.png -vcodec mpeg4 -y movie.mp4)
############################################################################################################

    def play_last_rendered_video(self):                      
        if self.last_directory_rendering != '':
           import subprocess as sp
           import locale
           import sys
        
           encoding = locale.getpreferredencoding()

           if sys.platform == 'win32':
              console_encoding = 'cp850'
           elif sys.platform in ('linux2', 'darwin'):
              console_encoding = 'utf-8'
         
           self.video_destination = os.path.join(self.last_directory_rendering,'movie.mp4').encode(encoding)
        
           FFMPEG_BIN = "ffplay" # on Windows
           #loop=Number of frame, Number of time, Frame index
           command = [FFMPEG_BIN, '-fs', '-loop','0', self.video_destination]

           pipe = sp.Popen(command, stdout = sp.PIPE, stderr=sp.PIPE)
           a, b = pipe.communicate()
           log.message('command : %s',command)
           log.message('pipe : %s, le dir : %s',a, b)
           #self.last_directory_rendering = ''
        else:
            G.app.prompt('Warning',
                         'Nothing to render check the number of images.',
                         'Ok')
                 
##########################################################################
# getAuFacialCode function to retreive Aus codes
##########################################################################
 
    def getAuFacialCode(self):
        au_code_txt = ''
        au_intensity = ''
        for au_key in self.sliders_order:
            au_key = str(au_key)
            #log.message("toto %s %s \n", au_key, self.sliders[au_key].getValue())
            if str(au_key) in self.sliders:
               if self.sliders[au_key].getValue() > 0.03:
                  if 0.03 < self.sliders[au_key].getValue() <= 0.1:
                     au_intensity = 'A'
                  if 0.1 < self.sliders[au_key].getValue() <= 0.2:
                     au_intensity = 'B'
                  if 0.2 < self.sliders[au_key].getValue() <= 0.55:
                     au_intensity = 'C'
                  if 0.55 < self.sliders[au_key].getValue() <= 0.9:
                     au_intensity = 'D'
                  if 0.9 < self.sliders[au_key].getValue() <= 1:
                     au_intensity = 'E'
                  au_code_slider = '[' + self.facs_code_names[au_key] + ']['+ au_intensity+ ']\n'
               else:
                    au_code_slider = ''
            au_code_txt = au_code_txt + au_code_slider
        
        if au_code_txt == '':
           au_code_txt = 'Neutral'

        return au_code_txt
  
  
######################################################################################################
# Create sliders, link it to the target files
# Target files are in the FACSHuman directory in user data MH directory
######################################################################################################
        
    def searchTargets(self, facsTargetFolder, boxDestination, boxName):
        au_order_file = facsTargetFolder + '/auorder.json'
        au_order = json.loads(open(au_order_file).read())
        # log.message("au_order %s %s", au_order_file, au_order)
        for the_file_name in au_order:
            file_to_load = os.path.join(facsTargetFolder, the_file_name + '.target')
            self.createTargetControls(boxDestination, file_to_load, facsTargetFolder, boxName)
            self.sliders_order.append(the_file_name)

    def createTargetControls(self, box, targetFile, facsTargetFolder, boxName):
        targetFile = os.path.relpath(targetFile, facsTargetFolder)
        facs_modifier = humanmodifier.SimpleModifier(boxName, facsTargetFolder, targetFile)
        facs_modifier.setHuman(self.facs_human)
        self.label_create = str(facs_modifier.name)
        self.labelSlider[self.label_create] = box.addWidget(gui.TextView("Intensity: 0%"))
        self.slidersValues[self.label_create] = 0
        self.sliders[self.label_create] = box.addWidget(modifierslider.ModifierSlider(modifier=facs_modifier, label=self.facs_code_names[self.label_create]))
        # Create object for mhEvent on sliders to catch values and update labeltxt
        FACSslider(self.sliders[self.label_create], self.labelSlider[self.label_create], self.slidersValues, self.label_create)  

        #self.leSlider = self.sliders[self.label_create]

##########################################################################
# Load Aus Timeline .fani (json file)
# Get files from facsanim directory in user data MH
##########################################################################

    def loadAusTimelineFile(self, path_to_file):
        self.au_timeline_values = {}
        
        self.au_timeline_values = json.loads(open(path_to_file).read())
        (dir_f, file_f) = os.path.split(path_to_file)
        self.txt_animatiom_file_loaded.setText('File: ' + file_f)
        
        # log.message("intensity_start: %s", self.au_timeline_values)

        # for au_timeline in self.au_timeline_values.keys():
            # for au_events in self.au_timeline_values[au_timeline].keys():
                # if self.au_timeline_values[au_timeline][au_events]['image_start'] == '0':
                   # intensity_start = float(self.au_timeline_values[au_timeline][au_events]['intensity_start'])
                   # log.message("intensity_start: %s", intensity_start)
                   # self.sliders[au_timeline].onChanging(intensity_start)
                   # self.sliders[au_timeline].update()
                   # self.sliders[au_timeline].setValue(intensity_start)
                   # self.slidersValues[au_timeline] = intensity_start

        self.sliderIntensitySetFromAnim('start')

        
        self.animation_test.onChange(0)
        self.animation_test.setValue(0)
        self.animation_test.update()
        
        self.general_intensity.onChange(100)
        self.general_intensity.update()
        self.general_intensity.setValue(100)
        #self.general_intensity_progress_bar.setProgress(1)
        self.au_coding.setText(self.getAuFacialCode())
        gui3d.app.statusPersist(path_to_file + ' loaded')
        self.facs_human.applyAllTargets()
        self.refreshAuSmoothSetting()

##########################################################################
# Load and save buttons definition
# Use the facs's file format
# Get files from facs directory in user data MH
##########################################################################

    def loadFacsFile(self, path_to_file):
        self.au_facs_loaded_file_values = {}
        
        try:
            self.au_facs_loaded_file_values = json.loads(open(path_to_file).read())
        except IOError as e:
            log.message("I/O error(%s): %s", e.errno, e.strerror)
            gui3d.app.statusPersist('Nothing to render')
        else:
            self.au_facs_loaded_file_values = json.loads(open(path_to_file).read())
            progress_loadFacsFile = Progress(len(self.au_facs_loaded_file_values))
            for key_code, value_code in self.au_facs_loaded_file_values.items():
                key_code = str(key_code)
                self.sliders[key_code].onChanging(value_code)
                self.sliders[key_code].update()
                self.sliders[key_code].setValue(value_code)
                self.slidersValues[key_code] = value_code
                self.labelSlider[key_code].setTextFormat( 'Intensity: %d%%', value_code*100)
                gui3d.app.statusPersist('Loading : ' + key_code)
                progress_loadFacsFile.step()
            self.general_intensity.onChange(100)   
            self.general_intensity.update()
            self.general_intensity.setValue(100)
            #self.general_intensity_progress_bar.setProgress(1)
            self.au_coding.setText(self.getAuFacialCode())
            gui3d.app.statusPersist(path_to_file + ' loaded')
            (dir_f, file_f) = os.path.split(path_to_file)
            self.txt_file_loaded.setText('File: ' + file_f)
            self.facs_human.applyAllTargets()
            self.refreshAuSmoothSetting()
        
    # To do : create checkbox to choose full or general slider values
    # Save the current sliders values with general intensity settings
    def saveCurrentFACS(self, path_to_file):

        sliders_value_to_save = {}
        for s_key, s_value in self.slidersValues.items():
            if s_value > 0:
                sliders_value_to_save[s_key] = self.sliders[s_key].getValue()
        
        json.dump(sliders_value_to_save, open(path_to_file, 'w'), indent=4)
        self.txt_file_loaded.setText('File: ' + os.path.basename(path_to_file))
        log.message("Saved FACS code as %s" % path_to_file)
        gui3d.app.statusPersist(path_to_file + ' saved')

        
        
##########################################################################
# Load FACSvatar data exported with openFace
# Use the facs's file format
# Get files from facs directory in user data MH
##########################################################################

    def loadFacsVatarFile(self, path_to_file):
        self.au_facs_loaded_file_values = {}
        
        try:
            self.au_facs_loaded_file_values = json.loads(open(path_to_file).read())
        except IOError as e:
            log.message("I/O error(%s): %s", e.errno, e.strerror)
            gui3d.app.statusPersist('Nothing to render')
        else:
            self.au_facs_loaded_file_values = json.loads(open(path_to_file).read())
            progress_loadFacsFile = Progress(len(self.au_facs_loaded_file_values))
            for key_code, value_code in self.au_facs_loaded_file_values.items():
                key_code = key_code.replace("AU","")
                key_code = key_code.replace("45","43") # Replace AU45 by AU43 same AU but different intensity 
                log.message("FACSvatar AU1 %s" % key_code) #### Log message
                if key_code.startswith('0'):
                   key_code = key_code[1:]
                log.message("FACSvatar AU2 %s" % key_code) #### Log message
                self.sliders[key_code].onChanging(value_code)
                self.sliders[key_code].update()
                self.sliders[key_code].setValue(value_code)
                self.slidersValues[key_code] = value_code
                self.labelSlider[key_code].setTextFormat( 'Intensity: %d%%', value_code*100)
                gui3d.app.statusPersist('Loading : ' + key_code)
                progress_loadFacsFile.step()
            self.general_intensity.onChange(100)   
            self.general_intensity.update()
            self.general_intensity.setValue(100)
            #self.general_intensity_progress_bar.setProgress(1)
            self.au_coding.setText(self.getAuFacialCode())
            gui3d.app.statusPersist(path_to_file + ' loaded')
            (dir_f, file_f) = os.path.split(path_to_file)
            self.txt_file_loaded.setText('File: ' + file_f)
            self.facs_human.applyAllTargets()
            self.refreshAuSmoothSetting()
        
        
        
##########################################################################
# Render image(s) in the grab directory
##########################################################################
        
    def renderFacsPicture(self, dir_images = None, pic_file = None, pic_file_reverse = None):
        self.facs_human.applyAllTargets()
        self.refreshAuSmoothSetting()

        grabPath = mh.getPath('grab')
        if not os.path.exists(grabPath):
           os.makedirs(grabPath)
       
        if pic_file is not None:
           dir_pic_file = os.path.join(grabPath, dir_images)
           pic_file = pic_file + '.png'
           pic_file = os.path.join(dir_pic_file, pic_file)
           if pic_file_reverse is not None:
              pic_file_reverse = pic_file_reverse + '.png'
              pic_file_reverse = os.path.join(dir_pic_file, pic_file_reverse)
        else:
            grabName = datetime.datetime.now().strftime('grab_%Y-%m-%d_%H.%M.%S.png')
            pic_file = os.path.join(grabPath, grabName)
        
        
        if self.renderingWidth == '' or self.renderingHeight == '' :
           G.app.prompt('Warning',
                         'Nothing to render check the image size.',
                         'Ok')
        else:
            img_width, img_height  = int(self.renderingWidth), int(self.renderingHeight)
            glmodule.draw(False)
            img = glmodule.renderToBuffer(img_width, img_height)
            alphaImg = glmodule.renderAlphaMask(img_width, img_height)
            img = imgop.addAlpha(img, imgop.getChannel(alphaImg, 0))
            img = img.toQImage()
            if pic_file is not None:
                img.save(pic_file)
                log.message("Image saved to %s", pic_file)
            if pic_file_reverse is not None:
                img.save(pic_file_reverse)
                log.message("Image saved to %s", pic_file_reverse)
            del alphaImg
            del img

            gui3d.app.statusPersist("Image saved to %s", pic_file)

##########################################################################
# Render stereo image(s) in the grab directory
##########################################################################
        
    def renderFacsPictureStereo(self, dir_images = None, pic_file = None, pic_file_reverse = None):
        dir_images_path = mh.getPath('grab')
        
        if dir_images is not None:
           dir_images_path = os.path.join(dir_images_path, dir_images)
           if not os.path.exists(dir_images_path):
              os.makedirs(dir_images_path)

        self.last_directory_rendering = dir_images_path

        self.zHumanRotation(0)
        self.renderFacsPicture(str(dir_images), "center")
        self.zHumanRotation(3)
        self.renderFacsPicture(str(dir_images), "L")
        self.zHumanRotation(-3)
        self.renderFacsPicture(str(dir_images), "R")
        self.zHumanRotation(0)
        self.createStereoFromImages()

##########################################################################
# Function to create stereoscopic perspective
##########################################################################
       
    def zHumanRotation(self, z_rotation = 1):
        pos = self.facs_human.getRotation()
        pos[1] = z_rotation
        self.facs_human.setRotation(pos)
        mh.redraw()
        
    def xHumanSlide(self, x_slide = 1):
        pos = self.facs_human.getPosition()
        pos[0] = x_slide #self.camera_slider_x.getValue()
        self.facs_human.setPosition(pos)
        mh.redraw()

##########################################################################
# Render image set for each AUs
##########################################################################
    def generateFullSet2(self):
        # for key_code in self.sliders.keys():
        nb_images = int(self.images_number_to_render.getText())
        nb_aus = len(self.sliders.keys())
        progress_render_images = Progress(nb_images*nb_aus)     
        dir_dest_images_path = self.images_set_dir_destination

        
        # self.sliders['1'].onChanging(1)
        # self.sliders['1'].update()
        # self.sliders['1'].setValue(1)
        
        for key_code in sorted(self.sliders.keys()):   
            dir_images = str(key_code) #'AU_' + datetime.datetime.now().strftime('images_%Y-%m-%d_%H_%M_%S')
            # self.last_directory_rendering  = os.path.join(dir_dest_images_path, dir_images)
            #self.last_directory_rendering = dir_dest_images_path + '/' + dir_images

            self.slidersValues[key_code] = 1
        
            self.renderImagesSet(timeline=False, dir_destination = dir_dest_images_path+'/', dir_name = key_code)
            # self.renderImagesSet(timeline=False, dir_destination = dir_dest_images_path, dir_name = key_code)
            
            progress_render_images.step()
            self.createVideoFromImages(key_code+'.mp4')
            self.sliders[key_code].onChanging(0)
            self.sliders[key_code].update()
            self.sliders[key_code].setValue(0)
            self.slidersValues[key_code] = 0


    def generateFullSet(self):
        # for key_code in self.sliders.keys():
        nb_images = int(self.images_number_to_render.getText())
        nb_aus = len(self.sliders.keys())
        progress_render_images = Progress(nb_images*nb_aus)     
        dir_dest_images_path = self.images_set_dir_destination

        
        # self.sliders['1'].onChanging(1)
        # self.sliders['1'].update()
        # self.sliders['1'].setValue(1)
        sliders_to_use  = ['24', '25', '26', '20', '23', '28', '29', '4', '58', '4_b', '54', '57', '4_a', '51', '53', '52', '55', '56', '7', '39', '38', '12_a', '33', '32', '31', '35', '34', '61', '62', '63', '64', '65', '66', '2', '6', '26_tongue_out', '11', '10', '13', '12', '15', '14', '17', '16', '18', '43', '1', '5', '9', '12_b']
        for key_code in sorted(sliders_to_use):
            dir_images = str(key_code)
            self.slidersValues[key_code] = 1
            self.renderImagesSet(timeline=False, dir_destination = dir_dest_images_path, dir_name = key_code)
            log.message("Create image + videos of : %s", key_code)
            self.createVideoFromImages(key_code+'.mp4')
            self.sliders[key_code].onChanging(0)
            self.sliders[key_code].update()
            self.sliders[key_code].setValue(0)
            self.slidersValues[key_code] = 0
            progress_render_images.step()

            
            
            
            
 

##########################################################################
# Render image with FACSvatar data 
##########################################################################
    def generateFacsvatarDirSet(self, path):
        dir_list = os.path.dirname(path)
        
        for root, dirs, files in os.walk(dir_list):
            progress_render_images = Progress(len(files))
            for f in files:
                if f.endswith(".json"):
                   self.resetFacialCodes()
                   self.loadFacsVatarFile(os.path.join(root, f))   
                   self.renderFacsPicture(dir_list, f.split(".")[0])
                progress_render_images.step()

 
##########################################################################
# Render image set for a specific directory 
##########################################################################
    def generateDirSet(self, path):
        dir_list = os.path.dirname(path)
        
        for root, dirs, files in os.walk(dir_list):
            progress_render_images = Progress(len(files))
            for f in files:
                if f.endswith(".facs"):
                   self.resetFacialCodes()
                   self.loadFacsFile(os.path.join(root, f))   
                   self.renderFacsPicture(dir_list, f.split(".")[0])
                progress_render_images.step()
        
        # nb_images = int(self.images_number_to_render.getText())
        # nb_aus = len(self.sliders.keys())
        # progress_render_images = Progress(nb_images)     
        # dir_images = 'AU_' + datetime.datetime.now().strftime('images_%Y-%m-%d_%H_%M_%S')
        # dir_images_path = mh.getPath('grab')
        # for key_code in sorted(self.sliders.keys()):   
            # for intensity_value in range(0, nb_images + 1):
                # self.sliders[key_code].onChanging(float(intensity_value)/nb_images)
                # self.sliders[key_code].update()
                # self.sliders[key_code].setValue(float(intensity_value)/nb_images)
                # self.renderFacsPicture(dir_images, key_code+'_'+str(intensity_value))
                
                # i = i+1
                # progress_render_images.step()
            # self.sliders[key_code].onChanging(0)
            # self.sliders[key_code].update()
            # self.sliders[key_code].setValue(0)
            
##########################################################################
# Render image set for a specific directory 
##########################################################################
    def generateCompleteImagesSetFromDir(self, path):
        nb_images = int(self.images_number_to_render.getText())
        if (self.images_set_dir_destination != '') and (path != ''):
            dir_destination = self.images_set_dir_destination + '/'
            dir_list = os.path.dirname(path) + '/'
            
            for dirpath, dirnames, filenames in os.walk(dir_list):
                the_destination = os.path.join(dir_destination,os.path.basename(os.path.dirname(dirpath)), os.path.basename(dirpath))

                progress_render_images = Progress(len(filenames))
             
                for fichier in filenames:
                    if fichier.endswith(".facs"):
                       if not os.path.exists(the_destination):
                          os.makedirs(the_destination)
                       self.resetFacialCodes()
                       self.loadFacsFile(os.path.join(dirpath, fichier))
                       file_name_destination = str(os.path.basename(os.path.dirname(dirpath))) + '_' + fichier.split(".")[0]
                       if nb_images > 1:
                          self.renderImagesSet(timeline=False, dir_destination = the_destination, dir_name = file_name_destination)
                          log.message("lesdirs %s %s", the_destination, file_name_destination)
                          self.createVideoFromImages(fichier.split(".")[0]+'.mp4')
                       else:
                          self.renderFacsPicture(the_destination, file_name_destination)
                          
                    gui3d.app.statusPersist('Images destination : ' + str(the_destination))
                    progress_render_images.step()
        else:
             G.app.prompt('Warning',
                         'Nothing to render choose directories before.',
                         'Ok')
           
                
# dir_facs = "C:/Users/Michaël/Documents/makehuman/v1/data/facs/Experimental data/EMFACS_Emotion predictions/"
# dir_dest = "C:/Users/Michaël/Documents/testfacs/"

# for dirpath, dirnames, filenames in os.walk(dir_facs):
    # the_destination = os.path.join(dir_dest,os.path.basename(os.path.dirname(dirpath)), os.path.basename(dirpath))
    # print('----------------------------------------')
    # print(os.path.basename(os.path.dirname(dirpath)))
    # print(' |- ' + os.path.basename(dirpath))
    # print(' + ' + the_destination)
    # print('----------------------------------------')
    # if not os.path.exists(the_destination):
       # os.makedirs(the_destination)

    # for fichier in filenames:
        # if fichier.endswith(".facs"):
           # print(str(fichier))
                
                
                
                
                
        # nb_images = int(self.images_number_to_render.getText())
        # nb_aus = len(self.sliders.keys())
        # progress_render_images = Progress(nb_images)     
        # dir_images = 'AU_' + datetime.datetime.now().strftime('images_%Y-%m-%d_%H_%M_%S')
        # dir_images_path = mh.getPath('grab')
        # for key_code in sorted(self.sliders.keys()):   
            # for intensity_value in range(0, nb_images + 1):
                # self.sliders[key_code].onChanging(float(intensity_value)/nb_images)
                # self.sliders[key_code].update()
                # self.sliders[key_code].setValue(float(intensity_value)/nb_images)
                # self.renderFacsPicture(dir_images, key_code+'_'+str(intensity_value))
                
                # i = i+1
                # progress_render_images.step()
            # self.sliders[key_code].onChanging(0)
            # self.sliders[key_code].update()
            # self.sliders[key_code].setValue(0)
            
            
            
            
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

        #facs_human.material.shader = getpath.getSysDataPath(self.taskViewShader) if self.taskViewShader else None array([  0.        ,   7.22596645,  18.91166067])

        
    def onHide(self, event):
        gui3d.app.statusPersist('')

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addTask(FACSHumanTaskView2(category, app))


def unload(app):
    pass

    
