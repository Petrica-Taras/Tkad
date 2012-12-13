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

## @namespace settings
#  Contains a class which holds the settings required by the root frame and several other widgets.
#
#  Centralizes the settings for all the widgets.  

import xml.etree.ElementTree as ET
import os

## settings() class
#  
#  The instance of this class generates the settings object required by several
#  other objects. It inherits from dict primitive
class settings(dict): 
    """Just a container for most settings shared between several objects.
       Settings that are automatically defined:
       - basedir
       - current working directory (cwd) - initially usr/worked - but can be overriden
       by settings from the loaded model (project.xml)
    
       Settings that are loaded from XML files:
       - menu widget ??? - put the path to resources in the XML file menu.xml ???
       - upper toolbox widget ??? - same as for the menu widget ???
       - canvas widget
       - XML Editor
       - console
       - status bar???"""
    ## The constructor
    # 
    #  Takes the 
    #  @param master
    #  argument which is the instance of the Application() class
    def __init__(self, master):
        """TODO:: define actions ..."""
        dict.__init__(self)

        ## @var self.master
        #  Holds a reference to the Application() type object
        self.master = master
        
		## @var self["basedir"]
		#  Determines the base directory (tkad.py directory)
		#
		#  Its value assumes that the main script starts from the Tkad.py directory
        self["basedir"] = os.getcwd() 
        
		## @var self["cwd"]
		#  Determines the current working directory
		#
		#  Reads etc/paths.xml LastWorkingDir element. If a project is opened, this 
		#  setting is overwritten by the project setting
        self["cwd"] = ""

        # ----------------------------- widgets settings ----------------------------- 

        # Menu
        self["menuIconsPath"] = os.path.join(self["basedir"], "resources/icons16x16/menu") # add possibilities for multiple resolutions        
        self["menuXMLPath"]   = os.path.join(self["basedir"], "etc/gui/menus.xml") 
        
        # Upper toolbar
        self["upperToolBarIconsPath"] = "resources/icons22x22/uptoolbar"
        self["upperToolBarXMLPath"]   = "etc/gui/uppertoolbar.xml"
        
        # Left toolbar
        self["leftToolBarIconsPath"] = "resources/icons22x22/lefttoolbar"
        self["leftToolBarXMLPath"]   = "etc/gui/lefttoolbar.xml"
        
        # Canvas
        self["canvasXMLPath"] = os.path.join(self["basedir"], "etc/gui/canvas.xml")
        self["canvas"]        = {}
        
        # XMLEditor
        self["XMLEditorXMLPath"] = os.path.join(self["basedir"], "etc/gui/XMLeditor.xml")
        self["XMLEditor"]        = {}
        
        # root Frame
        self.appTitle="Tkad - version 0.0.0a"        
        self.master.SetTitle(self.appTitle)
        self.master.SetSize((800, 600))
        self.master.Centre()
        self.master.Maximize()
        
        # ----------------------------------------------------------------------------
        
        # other useful paths
        self["extraModulesPath"] = {}     # relative/absolute paths???
        self["XMLPath"] = "etc/paths.xml" # canvas.xml and others ???


        self.__parseXMLData()

    def __parseXMLData(self): # canvas.xml and others ???
        """Parses the default paths.xml file into the self["extraModulesPath"]"""

        tree = ET.parse(self["XMLPath"])
        root = tree.getroot()
        
        # modules:
        
        for i in root.getiterator('module'):
            self["extraModulesPath"][i[0].text] = i[1].text
            
        # cwd:
        # quick and dirty solution - TODO - to be improved
        self["cwd"] = os.getcwd()
        
    def addXMLData(self, data, element):   # ????
        """Adds data to XML file paths.xml"""
        
        tree = ET.parse(self["XMLPath"])
        root = tree.getroot() 

        if (root.find(data).tag == data):

            if data == 'modules':
                self["extraModulesPath"][element['name']] = element['path']
                module = tree.SubElement(root.find(data), 'module')
                name   = tree.SubElement(module, 'name')
                name.text = element['name']
                path   = tree.SubElement(module, 'path')
                path.text = element['path']
            
            if data == "cwd":
                self['cwd'] = element
                lwd = root.find(data)
                lwd.text = element
         
            tree.write(self["XMLPath"], encoding = "UTF-8")
         
    def removeXMLData(self, data, element): # ???
        """Removes data to XML file paths.xml"""
        
        tree = ET.parse(self["XMLPath"])
        root = tree.getroot() 

        if (root.find(data).tag == data) and (element in self["extraModulesPath"]):
            if data == 'modules':
                del self["extraModulesPath"][element]
                module = root.find('modules')
                for i in module.findall('module'):   
                    if i[0].text == element:
                        module.remove(i)
            
            if data == "cwd": # resets to default /usr/worked
                self['cwd'] = 'usr/worked'
                lwd = root.find(data)
                lwd.text = 'usr/worked'
                
            tree.write(self["XMLPath"], encoding = "UTF-8")
        
    def __call__(self, data): # must define
        """Call the settings instance with the project.xml settings in order to 
        override some of its attributes with the information found in it."""
        if data == "menu":
            return (self["menuXMLPath"], self["menuIconsPath"])
        if data == "uppertoolbar":
            return (self["upperToolBarXMLPath"], self["upperToolBarIconsPath"])
        if data == "lefttoolbar":
            return (self["leftToolBarXMLPath"], self["leftToolBarIconsPath"])
        if data == "XMLEditor":
            return self["XMLEditorXMLPath"]  # ????
