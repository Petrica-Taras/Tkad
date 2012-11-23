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

from wx import MenuBar, Menu, MenuItem, Bitmap
import os
import xml.etree.ElementTree as ET

## menu() class
#
#  Custom menu which loads an application menu from a XML file
class menubar(MenuBar):
    """A custom Menu object which will generate the application menu based on a configuration XML file."""	
    def __init__(self, master, resources): # resources - (file, icons)
        MenuBar.__init__(self)
        self.master = master     
         
        self.__XMLfile   = resources[0]
        self.__iconspath = resources[1]
        
        ## @var MenuTree
        #
        #  holds the options for each widget		
        self.MenuTree = []

        ## @var menus
        #
        #  holds the widgets in a treelike fashion
        self.menus    = [] 
        
        self.__createMenu() 
        self.master.SetMenuBar(self)
             
    def __createMenu(self, node = None, dataTree = None, widgetsTree = None):
        """Extracts the layout information from the XML configuration file and creates
        the menubar in a recursive manner."""	

        if node == None:                       # base case
            tree = ET.parse(self.__XMLfile)
            root = tree.getroot()
            for i in root:
                self.MenuTree.append([i.attrib['name'], []])
                
                self.menus.append([i.attrib['name'], Menu(), []])
                self.Append(self.menus[-1][1], self.MenuTree[-1][0])
                
                self.__createMenu(i, self.MenuTree[-1][-1], self.menus[-1])
        else:
            for i in node:
                if len(i) > 0: 
                    dataTree.append([i.attrib['name'], 
                                     [i.attrib['accelerator'], i.attrib['icon']],
                                     []])
                    
                    widgetsTree[2].append([i.attrib['name'],
                                           Menu(),
                                           []]) 
                    
                    widgetsTree[1].AppendMenu(-1, i.attrib['name']+'\t'+i.attrib['accelerator'], widgetsTree[2][-1][1])
                    
                    self.__createMenu(i, dataTree[-1][-1], widgetsTree[2][-1])
                else:                      # simple menu item or separator encountered 
                    if i.attrib['name'] == 'Separator':
                        dataTree.append('Separator')
                        
                        widgetsTree[2].append('Separator') # may not be necessary!
                        widgetsTree[1].AppendSeparator()
                    else:
                        dataTree.append([i.attrib['name'], 
                                         [i.attrib['accelerator'], i.attrib['icon']]])   
                        
                        widgetsTree[2].append([i.attrib['name'],
                                               MenuItem(widgetsTree[1], 
                                                         -1, 
                                                         i.attrib['name']+'\t'+i.attrib['accelerator'])
                                              ])
                        # if the icons don't show up in the menu open gconf-editor - desktop>gnome>interface> menus_have_icons
                        widgetsTree[2][-1][1].SetBitmap(Bitmap(os.path.join(self.__iconspath, i.attrib['icon']), wx.BITMAP_TYPE_PNG))
                        widgetsTree[1].AppendItem(widgetsTree[2][-1][1])
             
if __name__ == "__main__": # test - to be deleted after adding callbacks!
    import wx
    app = wx.App(False)
    x = wx.Frame(None)
    m = menubar(x, ("../../etc/gui/menus.xml", "../../resources/icons16x16/menu"))
    x.SetSize((800, 600))
    x.SetTitle('Test icons and shortcuts')
    x.Centre()
    x.Show(True)    
    app.MainLoop()
