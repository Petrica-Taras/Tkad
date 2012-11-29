# Copyright (C) 2011 - 2012 Petrica Taras
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

from wx import ToolBar, Bitmap
import os
import xml.etree.ElementTree as ET

class leftToolbar(ToolBar):
    def __init__(self, master, resources, orientation): # resources (file, icons)
        ToolBar.__init__(self, master, style=orientation)
        self.master = master

        self.__XMLfile   = resources[0]
        self.__iconspath = resources[1]

        self.buttonsList = []
        self.widgetsList = []

        self.__createToolbar()
        self.Realize()

    def __createToolbar(self):
        tree = ET.parse(self.__XMLfile)
        root = tree.getroot()			    		
        
        for i in root:
            if i.attrib['name'] == 'Separator':
                self.buttonsList.append('Separator')
                self.AddSeparator()
            else:    
                self.buttonsList.append([i.attrib['name'], i.attrib['icon']])
                self.widgetsList.append([i.attrib['name'], 
                                         self.AddLabelTool(-1, '', Bitmap(os.path.join(self.__iconspath, i.attrib['icon'])))])

if __name__ == "__main__": # test - to be deleted after adding callbacks!
    import wx
    app = wx.App(False)
    x = wx.Frame(None)   
    vbox = wx.BoxSizer(wx.HORIZONTAL)
    
    m = leftToolbar(x, ("../../etc/gui/lefttoolbar.xml", "../../resources/icons22x22/lefttoolbar"), wx.TB_VERTICAL)
    
    vbox.Add(m, 0, wx.EXPAND)
    x.SetSizer(vbox)
    
    x.SetSize((800, 600))
    x.SetTitle('Test icons and shortcuts')
    x.Centre()
    x.Show(True)    
    app.MainLoop()
