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

from wx import Bitmap
import os
import xml.etree.ElementTree as ET

class upperToolbar():
    def __init__(self, master, resources): # resources (file, icons)       
        self.master = master

        self.__XMLfile   = resources[0]
        self.__iconspath = resources[1]

        self.buttonsList = []
        self.widgetsList = []

        self.toolbar = self.master.CreateToolBar()
        self.__createToolbar()

    def __createToolbar(self):
        tree = ET.parse(self.__XMLfile)
        root = tree.getroot()			    		
        
        for i in root:
            if i.attrib['name'] == 'Separator':
                self.buttonsList.append('Separator')
                self.toolbar.AddSeparator()
            else:    
                self.buttonsList.append([i.attrib['name'], i.attrib['icon']])
                self.widgetsList.append([i.attrib['name'], 
                                         self.toolbar.AddLabelTool(-1, '', Bitmap(os.path.join(self.__iconspath, i.attrib['icon'])))])

if __name__ == "__main__": # test - to be deleted after adding callbacks!
    import wx
    app = wx.App(False)
    x = wx.Frame(None)   
    m = upperToolbar(x, ("../../etc/gui/uppertoolbar.xml", "../../resources/icons22x22/uptoolbar"))
    x.SetSize((800, 600))
    x.SetTitle('Test icons and shortcuts')
    x.Centre()
    x.Show(True)    
    app.MainLoop()
