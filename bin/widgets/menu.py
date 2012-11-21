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

from tkinter import Menu, PhotoImage
import os
import xml.etree.ElementTree as ET

## menu() class
#
#  Custom menu which loads an application menu from a XML file
class menu(Menu):
    """A custom Menu object which will generate the application menu based on a configuration XML file. \
    
     Parameters:
     * parent application
     * XML configuration file
     * icons directory path"""	
    def __init__(self, master, xmlfile, iconspath):
        tkinter.Menu.__init__(self, master=master)
        self.master=master
        self.master.config(menu=self)       
         
        self.xmlfile=xmlfile
        self.iconspath=iconspath

        self.img=[]
        		
        self.MenuTree = None
        
        self.menus    = None # in order to have access to the widgets later  
        
        self.__createMenuDataStructure() 
        
        self.__createMenuDisplay()
        
        self.master.update_idletasks()
        
    def __createMenuDataStructure(self):
        """Extracts the layout information from the XML configuration file."""		
        xmlmenu=minidom.parse(self.xmlfile)
        MenuXMLRoot=[i for i in xmlmenu.childNodes if (i.nodeName != "#text" and i.nodeName != "#comment")]  # correct approach     

        try:
            if MenuXMLRoot == [] or MenuXMLRoot[0].nodeName != "MenuBar": raise RuntimeError
        except RuntimeError:
            tkinter.messagebox.showerror("Damaged Menu Configuration File", "The menu configuration file have been tampered with it. Will abort operation ...")
            self.master.quit()
            self.master.destroy()
            exit(1)

        self.MenuTree=[[i.attributes["name"].value, i] for i in MenuXMLRoot[0].childNodes if i.nodeName == "Menu"]
        self.menus=[[i.attributes["name"].value, i] for i in MenuXMLRoot[0].childNodes if i.nodeName == "Menu"]
        
        def recursMenuTree(node):
            """recursive function to populate the MenuTree"""
            menulist=[i for i in node.childNodes if (i.nodeName != "#text" and i.nodeName != "#comment")]
            node=[[] for i in menulist] # no longer needed
           
            for j in menulist:
                if j.nodeName == "MenuItem": 
                    node[menulist.index(j)]=[j.attributes["name"].value, list(j.attributes.items())]
                else: # must by a MenuSubDir
                    node[menulist.index(j)]=[j.attributes["name"].value, list(j.attributes.items()), j]
                    node[menulist.index(j)][2]=recursMenuTree(node[menulist.index(j)][2])
            return node        
         
        for i in self.MenuTree: 
            i[1]=recursMenuTree(i[1])

        for i in self.menus: # weird solution but self.menus=copy.copy(self.MenuTree) doesn't work as I expect
            i[1]=recursMenuTree(i[1])
                
    def createMenuDisplay(self):
        """It actually creates the Menu widgets"""
        # first create the menu:
        for i in self.MenuTree: 
            self.menus[self.MenuTree.index(i)][0]=tkinter.Menu(self)   
            self.add_cascade(label=i[0], menu=self.menus[self.MenuTree.index(i)][0])
        
        # recursively add the rest of the menu widget in a similar structure with self.MenuTree

        def recursMenus(menuname):
            """recursive function to add the rest of the menu widget."""
            # menuname is a two items like [Tkinter.Menu_Instance, [cascade_members]]
           
            for j in menuname[1]:
                if len(j) == 2: # simple item j[0] is the label of the menu item; j[1] - various options
                    
                    # consider the possibility of separators:
                    if j[0] == "Separator" and j[1][0][1] == "Separator":
                        menuname[0].add_separator()
                    else: 
                        # unpack the options and names (j[1]) into a dictionary like this: 
                        # {"name": strvalue, "callback": strvalue, "accelerator": strvalue, "icon":strvalue}   
                        attr={}
                        for i in j[1]: attr[i[0]]=i[1]
                        try:
                            self.img.append(ImageTk.PhotoImage(Image.open(os.path.join(self.iconspath, attr["icon"]))))
                            menuname[0].add_command(label=attr["name"], compound=tkinter.LEFT, image=self.img[-1], accelerator=attr["accelerator"])
                        except:
                            menuname[0].add_command(label=attr["name"], compound=tkinter.LEFT, image="", self.master, accelerator=attr["accelerator"])
                        del attr
                else: # must be a MenuSubDir (j[2] contains the items in the MenuSubDir)
                    j[0]=tkinter.Menu(menuname[0])
                    # unpack the options and names (j[1]) into a dictionary like this: 
                    # {"name": strvalue, "callback": strvalue, "accelerator": strvalue, "icon":strvalue}   
                    attr={}
                    for i in j[1]: attr[i[0]]=i[1]    
                    try:        
                        self.img.append(ImageTk.PhotoImage(Image.open(os.path.join(self.iconspath, attr["icon"]))))  
                        menuname[0].add_cascade(label=attr["name"], menu=j[0], compound=tkinter.LEFT, image=self.img[-1], accelerator=attr["accelerator"])
                    except:
                        menuname[0].add_cascade(label=attr["name"], menu=j[0], compound=tkinter.LEFT, image="", accelerator=attr["accelerator"]) 
                    del attr  
                    recursMenus([j[0], j[2]])
 
        for i in self.menus: 
            recursMenus(i)   
            
if __name__ == "__main__":
    from tkinter import tk
