# Copyright (C) 2011-2012 Petrica Taras
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
import wx

from scripts.common.settings import settings
#from scripts.common import model
#from scripts.common import state  
     
from scripts.widgets.menu import menuBar
from scripts.widgets.toolbar import toolbar
from scripts.widgets.mainpanel import mainPanel

#from scripts.widgets.canvas import canvas
from scripts.widgets.XMLeditor import XMLEditor

from scripts.widgets.console.log import consoleLog

## Application() class
#  
#  Instances of this class generates the application window
class Application(wx.Frame):
    """Main app window. Everything starts here.
       Keeps the main widgets (menu, upper and left toolbar, console, canvas, XML editor, etc.
       Initialises or uses the (common) settings object, the state object and the model object."""
    ## The constructor. 
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        # load registered settings and default empty state (menu & co)

        ## @var settings 
        #  A dictionary which holds the settings/options for various widgets
        self.settings = settings(self)

        ## @var model 
        #  A dictionary which holds the model tree structure and the associated files
        #self.model    = model()
        
        ## @var state 
        #  A dictionary which accounts for disabled         
        #self.state    = state()

        ## @var menuBar 
        #
        #  A menu widget with resources specified in a XML file. The callbacks to 
        #  various menu entries are added when the *Callbacks series of object are 
        #  instantiated. 
        self.menuBar      = None  # children - submenus
        
        ## @var upperToolbar 
        #
        #  A ToolBar widget, grouping several buttons/widgets with resources specified in a XML file. The callbacks 
        #  associated to various buttons are binded when the *Callbacks series of object are instantiated.         
        self.upperToolbar = None  # children - its buttons

        ## @var leftToolbar 
        #
        #  A ToolBar widget, grouping several buttons/widgets with resources specified in a XML file. The callbacks 
        #  associated to various buttons are binded when the *Callbacks series of object are instantiated.         
        self.leftToolbar = None  # children - its buttons
               
        ## @var canvas 
        #
        #  An enhanced canvas widget       
        #self.canvas       = None
        
        ## @var XMLEditor
        #
        #  An enhanced text widget with syntax highlighting, search/replace, etc.          
        self.XMLEditor    = None
        
        ## @var panel 
        #
        #  A panel widget which groups all the widgets previously created     
        self.mainPanel  = None  # children - all the widgets besides the menu and status bar

        ## @var consoleLog 
        #
        #  A TextCtrl widget which records log entries     
        self.consoleLog  = None  # children - none

        ## @var statusBar 
        #
        #  The statusBar        
        self.statusBar    = None # to be expanded to an external class

        self.__createApp()

    def __createApp(self):
        """Creates the main application window populated with all the widgets."""
        self.menuBar = menuBar(self, self.settings("menu"))

        self.mainPanel = mainPanel(self)
        
        self.upperToolbar = toolbar(self.mainPanel, self.settings("uppertoolbar"), wx.TB_HORIZONTAL)
        
        self.leftToolbar = toolbar(self.mainPanel, self.settings("lefttoolbar"), wx.TB_VERTICAL)
        
        self.XMLEditor = XMLEditor(self.mainPanel) # add settings later
        
        self.consoleLog = consoleLog(self.mainPanel) # add settings and functionality later

        self.mainPanel.addtoPanel(self.upperToolbar, (0, 0, 2))
        self.mainPanel.addtoPanel(self.leftToolbar, (1, 0, 1))
        self.mainPanel.addtoPanel(self.XMLEditor, (1, 1, 1))
        self.mainPanel.addtoPanel(self.consoleLog, (2, 0, 2))
        
        self.statusBar = self.CreateStatusBar()
        
        # create these, after the menu, and toolboxes where created (in order for the callbacks to be binded to the appropriate entries)
        #self.projectCallbacks     = projectCallbacks(self, master)
        #self.GeometryCallbacks    = geometryCallbacks(self, master)
        #self.SettingsCallbacks    = settingsCallbacks(self, master)
        #self.HelpCallbacks        = HelpCallbacks(self, master)

        self.Show()
        

    def initDrawingArea(self): # should be called after the other widgets are initialiazed.
        pass
