# Copyright (C) 2012 Petrica Taras
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

## @package app
#  Contains a class defining the main application window.
#
#  The main application instance require the settings, model and state objects.   

from xml.dom import minidom

import os 
import tkinter
import tkinter.tix

import GUI.widgets.menu
import GUI.widgets.uptoolbox
import GUI.widgets.canvas
import GUI.widgets.XMLeditor

# generate application window

class Application(tkinter.tix.Tk):
    """Main app window. Everything starts here.
       Keeps the main widgets (menu, upper and right toolbar, console, canvas, XML editor, etc.
       Initialises or uses the (common) settings object, the state object and the model object."""
    def __init__(self, settings, model, state):
        tkinter.tix.Tk.__init__(self)
        # load registered settings and default empty state (menu)
        
        self.settings = settings
        self.model    = model
        self.state    = state
        
        self.xmlPaths=None  # ????
        self.modulePaths=[] # other directories to import modules from ????

        self.xmlprojfiles={"trunk":    None,
                           "geometry": None,
                           "mesh":     None} # ???? maybe I should move this 

        self.projState = None # if the app starts with a new project, no project, a previously opened one, etc ... TODO
                              # with influence on self.settings (some menu entries have to be disabled with respect to
                              # the settings

        self.widgets = None # holds all widgets in an unified way - maybe in a clear to follow tree ????

        self.menuBar=None

        self.upperFrame=None # general buttons like zoom, new, save, entity hierarchy, open editor (xml, python),

        self.canvasFrame=None # left toolbox + cad widget
        self.notebook=None
        self.leftFrame=None
        self.DrawingArea=None
        self.XMLeditor=None

        self.lowerConsole=None # with tabs possibility
        self.lowerLabelFrame=None # has priority when determining the windows size
        self.lowerLabel=None
        self.lowerlabelstr=[]

        self.AppTitle=tkinter.StringVar()
        self.AppTitle.set("")

        self.readXML() # ??? - settings ???
        self.createApp()

    def createApp(self):
        self.menuBar=GUI.widgets.menu.MenuToolbar(self,
                                                  self.settings["menuXMLPath"],
                                                  self.settings["menuIconsPath"])

        self.upperFrame=GUI.widgets.uptoolbox.UpperToolbox(self,
                                                           self.settings["upperToolBoxXMLPath"],
                                                           self["upperToolBoxIconsPath"])

        self.notebook=tkinter.tix.NoteBook(self)
        self.notebook.pack(side="top", fill="both", expand="yes")

        # more like testing purpose
        self.lowerLabelFrame=tkinter.Frame(self, borderwidth=0)
        self.lowerLabelFrame.pack(side="top", fill="x")
        self.lowerlabelstr.append(tkinter.StringVar())
        self.lowerLabel=tkinter.Label(self.lowerLabelFrame, textvariable=self.lowerlabelstr[0], relief="sunken")
        self.lowerLabel.pack(side="bottom", fill="x")

        # bindings

        self.geometry('%sx%s+0+0' % self.maxsize())

        self.title(self.AppTitle.get())
        self.update_idletasks()
        self.mainloop()

    def initDrawingArea(self): # should be called after the other widgets are initialiazed.

        self.notebook.add(name="canvas", label="Drawing Area")

        self.DrawingArea=GUI.widgets.canvas.DrawingArea(self, os.path.join(self.basedir, "etc/gui/canvas.xml")) # add setting to settings instance
        self.DrawingArea.pack(fill="both", expand="yes", in_=self.notebook.canvas)
        self.update_idletasks()

        self.DrawingArea.bind("<Motion>", self.__cb_lowerlabel, add="+")

        self.notebook.add(name="xml", label="XML")
        self.XMLeditor=GUI.widgets.XMLeditor.XMLeditor(self, os.path.join(self.basedir, "etc/gui/XMLeditor.xml")) # add setting to settings instance
        self.XMLeditor.pack(fill="both", expand="yes", in_=self.notebook.xml)
        self.XMLeditor.insert(tkinter.END, 
                              self.xmlprojfiles["geometry"][0].toprettyxml(indent = '   ', 
                                                                           encoding=self.xmlprojfiles["geometry"][0].encoding))


    def readXML(self):
        self.xmlPaths=minidom.parse(os.path.join(self.basedir, "etc/paths.xml"))

        for i in self.xmlPaths.getElementsByTagName('ModPath'):
            self.modulePaths.append(i.firstChild.data)

        self.lwd=os.path.join(self.basedir, self.xmlPaths.getElementsByTagName("LastWorkingDir")[0].firstChild.data)

    def __cb_lowerlabel(self, event): # to be transformed in a full class widget
        self.lowerlabelstr[0].set("x_int = %d, y_int = %d" % (event.x, event.y))
