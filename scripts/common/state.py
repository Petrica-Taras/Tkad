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

import tkinter

## state() class
#  
#  Instances of this class generates the application window
class state(dict):
    """Holds the status of various menu, toolbar entries (i.e. enabled/disabled)"""
    def __init__(self):
        dict.__init__(self)
        
        # instead of plain 1's should be IntVar()
        self["newProject"] = 1 # should be disabled when an project is opened
        self["openProject"] = 1 # should be disabled
        
        self.defaultState()
    
    def defaultState(self):
        """Disables the unneeded entries when the program starts"""
        pass
    
    def newProject():
        """Needed when a new project command is given.
           TODO: enumerate the widgets to be connected to this method.""" 
        pass
    
    def openProject():
        pass
