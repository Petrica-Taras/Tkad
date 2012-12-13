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

## @namespace project
#  Contains a class defining code for the Project menu entries callbacks.
#

import os
import re
import wx

## projectIO() class
#  
#  The instance of this class populates the Project menu entries with callbacks. It also modifies the state and settings objects
class projectIO():
    """Contains the callbacks associated with the entries from the Project menu:
        - new;
        - open;
        - save;
        - saveas;
        - close;
        - exit"""
    def __init__(self, app):
        self.app = app
        #self.app.state.projectStatus = 0 # set state to "new", "opened", "modified" ????    

        self.__setProjectMenu()

    def __setProjectMenu(self):
        """Populates the self.app.menuBar.projectsubmenu with callbacks"""
        self.app.Bind(wx.EVT_MENU, self.new, self.app.menuBar.menus[0][2][0][1])
        self.app.Bind(wx.EVT_MENU, self.open, self.app.menuBar.menus[0][2][1][1])
        self.app.Bind(wx.EVT_MENU, self.save, self.app.menuBar.menus[0][2][2][1])
        self.app.Bind(wx.EVT_MENU, self.saveAs, self.app.menuBar.menus[0][2][3][1])
        self.app.Bind(wx.EVT_MENU, self.close, self.app.menuBar.menus[0][2][5][1])
        self.app.Bind(wx.EVT_MENU, self.exit, self.app.menuBar.menus[0][2][6][1])

    def new(self, event):
        """Callback for the "New Project" menu entry"""	
     
        if "NewProject.project" not in os.listdir(self.app.settings["cwd"]):
            ProjFolder = "NewProject.project"
        else:
            dPattern=re.compile(r'^NewProject(\d*).project$')
            ldirs=[s for s in os.listdir(self.app.settings["cwd"]) if os.path.isdir(s)]      # separate folders from files
            l=[s for s in ldirs if dPattern.search(s) is not None]              # separate folders with pattern "NewProject*.project"
     
            gldirs=[int(dPattern.search(s).groups()[0]) for s in l if (dPattern.search(s).groups())[0] is not '']
            if gldirs==[]: ProjFolder = "NewProject1.project"          # found "NewProject.project" in the current directory
            else:
                DirNo=[i for i in range(1, max(gldirs)+1) if i not in gldirs]
                if DirNo == []:
                    ProjFolder = "NewProject"+str(max(gldirs)+1)+".project" # found a sequence of "NewProject*.project" named folders
                else:
                    ProjFolder = "NewProject"+str(min(DirNo))+".project"    # found a sequence of "NewProject*.project" named folders
                                                                            # with missing pieces
        
        self.app.settings.appTitle = ProjFolder #???
        self.app.consoleLog.write("New Project "+ProjFolder+" created\n")
        
    def open(self, event):
        self.app.consoleLog.write("Open Project functionality not implemented yet!\n")
    
    def save(self, event):
        self.app.consoleLog.write("Save Project functionality not implemented yet!\n")
    
    def saveAs(self, event):
        self.app.consoleLog.write("Save As Project functionality not implemented yet!\n")
    
    def close(self, event):
        self.app.consoleLog.write("Close Project functionality not implemented yet!\n")

    def exit(self, event):
        self.app.Close()
