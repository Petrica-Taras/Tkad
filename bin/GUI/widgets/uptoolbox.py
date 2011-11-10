# Copyright (C) 2011 Petrica Taras
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

import Tkinter, collections, functools, os
from ..callbacks import project
from xml.dom import minidom
from PIL import Image, ImageTk

class UpperToolbox(Tkinter.Frame):
    def __init__(self, master, xmlfile):
        Tkinter.Frame.__init__(self, master=master)
        
        self.master=master
        
        self.xmlfile=xmlfile
        #self.iconsDir=os.path.join(self.master.basedir, "resources/icons22x22")
        self.iconsDir=os.path.join("/home/pts/cns/projects/me/python/urbanmod/experimental", "resources/icons22x22")
        self.img=[]
                
        self.ToolboxTree=[]    
        self.ToolboxWidgets=[]
        self.createToolboxTree()
        self.createToolbox()
    
    def createToolboxTree(self):
        xmltoolbox=minidom.parse(self.xmlfile)
        xmltoolboxRoot=xmltoolbox.firstChild
        for i in xmltoolboxRoot.childNodes:       
            if (i.nodeName != "#text") and (i.nodeName !='#comment'):  
                self.ToolboxTree.append((i.attributes["icon"].value, i.attributes["callback"].value))  
    
    def createToolbox(self):
        for i in self.ToolboxTree:
            self.img.append(ImageTk.PhotoImage(Image.open(os.path.join(self.iconsDir, i[0]))))		
            self.ToolboxWidgets.append(Tkinter.Button(self, command=functools.partial(eval(i[1]), self.master), image=self.img[-1]))	
            self.ToolboxWidgets[-1].pack(side="left")				    		