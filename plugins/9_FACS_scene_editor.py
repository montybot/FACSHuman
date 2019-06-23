#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

""" 
**Project Name:**      FACSHuman scene
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


import gui3d
import mh
import gui
from core import G
import guirender
import log
import filechooser as fc
import scene


class SceneItem(object):
    def __init__(self, sceneview, label=""):
        # Call this last
        self.sceneview = sceneview
        self.label = label
        self.widget = gui.GroupBox(label)
        self.makeProps()

    def makeProps(self):
        pass

    def showProps(self):
        self.sceneview.propsBox.showWidget(self.widget)
        self.sceneview.activeItem = self

    def update(self):
        pass

    def __del__(self):
        self.widget.destroy()


class SceneItemAdder(SceneItem):
    # Virtual scene item for adding scene items.
    def __init__(self, sceneview):
        SceneItem.__init__(self, sceneview, "Add scene item")

    def makeProps(self):
        SceneItem.makeProps(self)
        self.lightbtn = self.widget.addWidget(gui.Button('Add light'))

        @self.lightbtn.mhEvent
        def onClicked(event):
            self.sceneview.scene.addLight()


class EnvironmentSceneItem(SceneItem):
    def __init__(self, sceneview):
        SceneItem.__init__(self, sceneview, "Environment properties")

    def makeProps(self):
        SceneItem.makeProps(self)

        self.colbox = self.widget.addWidget(
            VectorInput("Ambience",
                self.sceneview.scene.environment.ambience, True))

        self.colboxSlider = self.widget.addWidget(gui.Slider(value=1, min=0, max=1, label=['Light X position',' %.2f']))         

        @self.colbox.mhEvent
        def onChange(value):
            self.sceneview.scene.environment.ambience = value

        @self.colboxSlider.mhEvent
        def onChanging(value):
            self.sceneview.scene.environment.ambience = (value,value,value)
            self.colbox.setValue(self.sceneview.scene.environment.ambience)
    
            
class LightSceneItem(SceneItem):
    def __init__(self, sceneview, light, lid):
        self.lightid = lid
        self.light = light
        SceneItem.__init__(
            self, sceneview, "Light %s properties" % self.lightid)

    def makeProps(self):
        SceneItem.makeProps(self)

        self.posbox = self.widget.addWidget(
            VectorInput("Position", self.light.position))

        self.posboxSliderX = self.widget.addWidget(gui.Slider(value=self.light.position[0], min=-50, max=50, label=['Light X position',' %.2f']))         
        self.posboxSliderY = self.widget.addWidget(gui.Slider(value=self.light.position[1], min=-50, max=50, label=['Light y position',' %.2f']))         
        self.posboxSliderZ = self.widget.addWidget(gui.Slider(value=self.light.position[2], min=-50, max=50, label=['Light Z position',' %.2f']))         
            
            
        # self.focbox = self.widget.addWidget(
            # VectorInput("Focus", self.light.focus))

        # self.focboxSliderX = self.widget.addWidget(gui.Slider(value=self.light.focus[0], min=0, max=1, label=['FocusX',' %.2f']))         
        # self.focboxSliderY = self.widget.addWidget(gui.Slider(value=self.light.focus[0], min=0, max=1, label=['FocusY',' %.2f']))         
        # self.focboxSliderZ = self.widget.addWidget(gui.Slider(value=self.light.focus[0], min=-0, max=1, label=['FocusZ',' %.2f']))         

        self.colbox = self.widget.addWidget(
            VectorInput("Color", self.light.color, True))

        self.specular2 =  (1, 1, 1)
        
        self.specbox = self.widget.addWidget(
            VectorInput("Specular", self.light.specular, True))

        self.specboxSlider = self.widget.addWidget(gui.Slider(value=self.light.specular[0], min=0, max=1, label=['Specular intensity',' %.2f']))         

        # self.fov = self.widget.addWidget(
            # VectorInput("Spot angle", [self.light.fov]))
            
        # self.fovSlider = self.widget.addWidget(gui.Slider(value=0, min=0, max=180, label=['Spot angle',' %.2f']))         

        # self.att = self.widget.addWidget(
            # VectorInput("Attenuation", [self.light.attenuation]))

        # self.soft = self.widget.addWidget(
            # BooleanInput("Soft light", self.light.areaLights > 1))

        # self.size = self.widget.addWidget(
            # VectorInput("Softness", [self.light.areaLightSize]))

        # self.samples = self.widget.addWidget(
            # VectorInput("Samples", [self.light.areaLights]))

        self.removebtn = self.widget.addWidget(
            gui.Button('Remove light ' + str(self.lightid)))

        @self.posbox.mhEvent
        def onChange(value):
            self.light.position = tuple(value)
            #self.posboxSliderX.setValue() 

        @self.posboxSliderX.mhEvent
        def onChanging(value):
            self.light.position = (value,self.posboxSliderY.getValue(),self.posboxSliderZ.getValue())
            self.posbox.setValue(self.light.position)

        @self.posboxSliderY.mhEvent
        def onChanging(value):
            self.light.position = (self.posboxSliderX.getValue(),value,self.posboxSliderZ.getValue())
            self.posbox.setValue(self.light.position)

        @self.posboxSliderZ.mhEvent
        def onChanging(value):
            self.light.position = (self.posboxSliderX.getValue(),self.posboxSliderY.getValue(),value)
            self.posbox.setValue(self.light.position)

        # @self.focbox.mhEvent
        # def onChange(value):
            # self.light.focus = tuple(value)
            
        # @self.focboxSliderX.mhEvent
        # def onChanging(value):
            # self.light.focus = (value,self.focboxSliderY.getValue(),self.focboxSliderZ.getValue())
            # self.focbox.setValue(self.light.focus)

        # @self.focboxSliderY.mhEvent
        # def onChanging(value):
            # self.light.focus = (self.focboxSliderX.getValue(),value,self.focboxSliderZ.getValue())
            # self.focbox.setValue(self.light.focus)

        # @self.focboxSliderZ.mhEvent
        # def onChanging(value):
            # self.light.focus = (self.focboxSliderX.getValue(),self.focboxSliderY.getValue(),value)
            # self.focbox.setValue(self.light.focus)

        @self.colbox.mhEvent
        def onChange(value):
            self.light.color = tuple(value)

        @self.specbox.mhEvent
        def onChange(value):
            self.light.specular = tuple(value)
        
        @self.specboxSlider.mhEvent
        def onChanging(value):
            self.specular2 =  self.specbox.getValue()
            self.light.specular = (self.specular2[0]*value,self.specular2[1]*value,self.specular2[2]*value)
            #self.specbox.setValue(self.light.specular)
        
        # @self.fov.mhEvent
        # def onChange(value):
            # self.light.fov = value[0]
            # log.message('fov : %s', value)

        # @self.fovSlider.mhEvent
        # def onChanging(value):
            # self.light.fov = value
            # self.fov.setValue([value])
            # log.message('titi : %s', value)

        # @self.att.mhEvent
        # def onChange(value):
            # self.light.attenuation = value[0]

        # @self.soft.mhEvent
        # def onChange(value):
            # if value and self.light.areaLights <= 1:
                # self.light.areaLights = 2
                # self.samples.setValue([2])
            # elif self.light.areaLights > 1:
                # self.light.areaLights = 1
                # self.samples.setValue([1])

        # @self.size.mhEvent
        # def onChange(value):
            # self.light.attenuation = value[0]

        # @self.samples.mhEvent
        # def onChange(value):
            # self.light.areaLights = int(value[0])
            # self.soft.setValue(self.light.areaLights > 1)

        @self.removebtn.mhEvent
        def onClicked(event):
            self.sceneview.scene.removeLight(self.light)


class FACSSceneEditorTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'FACS Scene Editor')

        # Declare settings
        G.app.addSetting('Scene_Editor_FileDlgPath', mh.getDataPath('scenes'))

        sceneBox = self.addLeftWidget(gui.GroupBox('Scene'))
        self.fnlbl = sceneBox.addWidget(gui.TextView('<New scene>'))
        self.saveButton = sceneBox.addWidget(gui.Button('Save'), 1, 0)
        self.loadButton = sceneBox.addWidget(gui.Button('Load ...'), 1, 1)
        self.saveAsButton = sceneBox.addWidget(gui.Button('Save As...'), 2, 0)
        self.closeButton = sceneBox.addWidget(gui.Button('Close'), 2, 1)

        itemBox = self.addLeftWidget(gui.GroupBox('Items'))
        self.itemList = itemBox.addWidget(gui.ListView())
        self.itemList.setSizePolicy(
            gui.SizePolicy.Ignored, gui.SizePolicy.Preferred)

        self.propsBox = gui.StackedBox()
        self.addRightWidget(self.propsBox)

        self.addButton = itemBox.addWidget(gui.Button('Add...'))
        self.adder = SceneItemAdder(self)
        self.propsBox.addWidget(self.adder.widget)
        self.activeItem = None

##################################################################################################################      
        self.filechooser = self.addLeftWidget(
            fc.IconListFileChooser(
                [mh.getDataPath('scenes'), mh.getSysDataPath('scenes')],
                'mhscene', ['thumb', 'png'], 'notfound.thumb', 'Scene'))
        #self.addLeftWidget(self.filechooser.createSortBox())
        self.filechooser.enableAutoRefresh(False)

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            G.app.setScene(scene.Scene(filename))

#    def onShow(self, event):
#        self.filechooser.refresh()
#        self.filechooser.selectItem(G.app.scene.file.path)
#        self.filechooser.setFocus()

##################################################################################################################  
        
        self._scene = None

        def doLoad():
            filename = mh.getOpenFileName(
                G.app.getSetting('Scene_Editor_FileDlgPath'),
                'MakeHuman scene (*.mhscene);;All files (*.*)')
            if filename:
                G.app.setSetting('Scene_Editor_FileDlgPath', filename)
                self.scene.load(filename)

        def doSave(filename):
            ok = self.scene.save(filename)
            if ok and self._scene.file.path is not None \
                and self._scene.file.path == self.scene.file.path:
                # Refresh MH's current scene if it was modified.
                self._scene.load(self._scene.file.path)

        @self.loadButton.mhEvent
        def onClicked(event):
            if self.scene.file.modified:
                G.app.prompt('Confirmation',
                    'Your scene is unsaved. Are you sure you want to close it?',
                    'Close', 'Cancel', doLoad)
            else:
                doLoad()

        @self.saveButton.mhEvent
        def onClicked(event):
            if self.scene.file.path is None:
                self.saveAsButton.callEvent('onClicked', event)
            else:
                doSave(self.scene.file.path)

        @self.closeButton.mhEvent
        def onClicked(event):
            if self.scene.file.modified:
                G.app.prompt('Confirmation',
                    'Your scene is unsaved. Are you sure you want to close it?',
                    'Close', 'Cancel', self.scene.reset)
            else:
                self.scene.reset()

        @self.saveAsButton.mhEvent
        def onClicked(event):
            filename = mh.getSaveFileName(
                G.app.getSetting('Scene_Editor_FileDlgPath'),
                'MakeHuman scene (*.mhscene);;All files (*.*)')
            if filename:
                G.app.setSetting('Scene_Editor_FileDlgPath', filename)
                doSave(filename)

        @self.itemList.mhEvent
        def onClicked(item):
            item.getUserData().showProps()

        @self.addButton.mhEvent
        def onClicked(event):
            self.adder.showProps()

    @property
    def scene(self):
        return G.app.scene

    def readScene(self):
        self.adder.showProps()
        self.itemList.setData([])
        self.itemList.addItem("Environment", data=EnvironmentSceneItem(self))
        for i, light in enumerate(self.scene.lights):
            self.itemList.addItem("Light " + str(i), data=LightSceneItem(self, light, i))
        for item in self.itemList.getItems():
            self.propsBox.addWidget(item.getUserData().widget)

    def updateFileTitle(self, file):
        lbltxt = file.name
        if lbltxt is None:
            lbltxt = '<New scene>'
        if file.modified:
            lbltxt += '*'
        self.fnlbl.setText(lbltxt)

    def onSceneChanged(self, event):
        if not self.isShown():
            return

        self.updateFileTitle(event.file)
        if any(term in event.reasons for term in ("load", "add", "remove")):
            self.readScene()

    def onShow(self, event):
        # Swap to edited scene and store app's scene
        temp = self._scene
        self._scene = G.app.scene
        G.app.scene = temp

        gui3d.TaskView.onShow(self, event)

        # Create edited scene if it does not exist
        if G.app.scene is None:
            from scene import Scene
            G.app.scene = Scene()

        self.filechooser.refresh()
        self.filechooser.selectItem(G.app.scene.file.path)
        self.filechooser.setFocus()
            
    def onHide(self, event):
        gui3d.TaskView.onHide(self, event)

        # Restore app's scene and store edited scene
        temp = self._scene
        self._scene = G.app.scene
        #G.app.scene = temp


class BooleanInput(gui.GroupBox):
    def __init__(self, name, value):
        super(BooleanInput, self).__init__(name)
        self.name = name

        self.widget = gui.CheckBox()
        self.widget.setChecked(value)
        self.addWidget(self.widget, 0, 0)

        @self.widget.mhEvent
        def onClicked(arg=None):
            self.callEvent('onChange', self.getValue())

    def getValue(self):
        return self.widget.selected

    def setValue(self, value):
        self.widget.setChecked(value)


class VectorInput(gui.GroupBox):
    def __init__(self, name, value=[0.0, 0.0, 0.0], isColor=False):
        super(VectorInput, self).__init__(name)
        self.name = name

        self.widgets = []
        for idx, v in enumerate(value):
            w = FloatValue(self, v)
            self.widgets.append(w)
            self.addWidget(w, 0, idx)
        self._value = value

        if isColor:
            self.colorPicker = gui.ColorPickButton(value)

            @self.colorPicker.mhEvent
            def onClicked(color):
                self.setValue(list(color.asTuple()))

            self.addWidget(self.colorPicker, 1, 0)
        else:
            self.colorPicker = None

    def setValue(self, value):
        for idx, w in enumerate(self.widgets):
            w.setValue(value[idx])
        self._value = value
        if self.colorPicker:
            self.colorPicker.color = self.getValue()
        self.callEvent('onChange', self.getValue())

    def getValue(self):
        return self._value

    def onActivate(self, arg=None):
        try:
            self._value = [w.value for w in self.widgets]
            if self.colorPicker:
                self.colorPicker.color = self.getValue()
            self.callEvent('onChange', self.getValue())
        except:
            pass


class NumberValue(gui.TextEdit):
    def __init__(self, parent, value):
        super(NumberValue, self).__init__(str(value), self._validator)
        self.parent = parent

    def sizeHint(self):
        size = self.minimumSizeHint()
        size.width = size.width() * 3
        return size

    def onActivate(self, arg=None):
        try:
            self.parent.callEvent('onActivate', self.value)
        except:
            pass

    def onChange(self, arg=None):
        try:
            self.parent.callEvent('onActivate', self.value)
        except:
            pass

    def setValue(self, value):
        self.setText(str(value))


class FloatValue(NumberValue):
    _validator = gui.floatValidator

    @property
    def value(self):
        return float(self.text)


class IntValue(NumberValue):
    _validator = gui.intValidator

    @property
    def value(self):
        return int(self.text)


def load(app):
    category = app.getCategory('Modelling')
    category.addTask(FACSSceneEditorTaskView(category))


def unload(app):
    pass
