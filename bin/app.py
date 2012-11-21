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

## @namespace app
#  Contains a class defining the main application window.
#
#  The main application instance require the settings, model and state objects.   

import os 
import tkinter
import tkinter.tix

from bin.common import settings
from bin.common import model
from bin.common import state  
     
#from bin.widgets.menu import menu
from bin.widgets.uptoolbox import uppertoolbox
from bin.widgets.middleframe import middleframe

from bin.widgets.canvas import canvas
from bin.widgets.XMLeditor import XMLeditor

## Application() class
#  
#  Instances of this class generates the application window
class Application(tkinter.tix.Tk):
    """Main app window. Everything starts here.
       Keeps the main widgets (menu, upper and left toolbar, console, canvas, XML editor, etc.
       Initialises or uses the (common) settings object, the state object and the model object."""
    ## The constructor. 
    def __init__(self):
        tkinter.tix.Tk.__init__(self)
        # load registered settings and default empty state (menu & co)

        ## @var settings 
        #  A dictionary which holds the settings/options for various widgets
        self.settings = settings(self)

        ## @var model 
        #  A dictionary which holds the model tree structure and the associated files
        self.model    = model()
        
        ## @var state 
        #  A dictionary which accounts for disabled         
        self.state    = state()

        ## @var menuBar 
        #
        #  A menu widget with resources specified in a XML file. The callbacks to 
        #  various menu entries are added when the *Callbacks series of object are 
        #  instantiated. 
        self.menuBar      = None  # children - submenus
        
        ## @var upperToolbox 
        #
        #  A frame widget, grouping several buttons/widgets with resources specified in a XML file. The callbacks 
        #  associated to various buttons are binded when the *Callbacks series of object are instantiated.         
        self.upperToolbox = None  # children - its buttons

        ## @var middleFrame 
        #
        #  A frame widget, serving no other purposes than to group the left toolbox and notebook widgets conveniently     
        self.middleFrame  = None  # children - leftToolbox, notebook
        
        ## @var leftToolbox 
        #
        #  A frame widget, grouping several buttons which are commonly used. The callbacks associated 
        #  to various buttons are binded when the *Callbacks series of object are instantiated.            
        self.leftToolbox  = None  # children - its buttons
        
        ## @var notebook 
        #
        #  A tkinter.tix widget which offers the possibility of tabbing several opened documents. Its children are 
        #  the canvas and the XMLEditor widgets
        self.notebook     = None  # children - canvas and XMLEditor
        
        ## @var canvas 
        #
        #  An enhanced canvas widget       
        self.canvas       = None
        
        ## @var XMLEditor
        #
        #  An enhanced text widget with syntax highlighting, search/replace, etc.          
        self.XMLEditor    = None

        ## @var statusBar 
        #
        #  A frame widget, grouping several label widgets which show various information
        # about the project and its current state        
        self.statusBar    = None  # several label type widgets holding information

        self.__createApp()

    def __createApp(self):
        """Creates the main application window populated with all the widgets."""
        
        self.menuBar = menu(self, self.settings("menu"))

        self.upperToolbox = uppertoolbox(self, self.settings("uppertoolbox"))

        self.middleFrame = None # TODO - start from here

        self.notebook=tkinter.tix.NoteBook(self)
        self.notebook.pack(side="top", fill="both", expand="yes")
        
        # create these, after the menu, and toolboxes where created (in order for the callbacks to be binded to the appropriate entries)
        self.projectCallbacks     = projectCallbacks(self, master)
        self.GeometryCallbacks    = geometryCallbacks(self, master)
        self.SettingsCallbacks    = settingsCallbacks(self, master)
        self.HelpCallbacks        = HelpCallbacks(self, master)
        
        # more like testing purpose
        self.statusBar=tkinter.Frame(self, borderwidth=0)
        self.lowerLabelFrame.pack(side="top", fill="x")
        self.lowerlabelstr.append(tkinter.StringVar())
        self.lowerLabel=tkinter.Label(self.lowerLabelFrame, textvariable=self.lowerlabelstr[0], relief="sunken")
        self.lowerLabel.pack(side="bottom", fill="x")

        # bindings

        self.geometry('%sx%s+0+0' % self.maxsize())

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

    def __cb_lowerlabel(self, event): # to be transformed in a full class widget
        self.lowerlabelstr[0].set("x_int = %d, y_int = %d" % (event.x, event.y))
