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

## @package settings
#  Holds the settings class required by the widgets

import xml.etree.ElementTree as ET
import os

class settings(dict): 
    """Just a container for most settings shared between several objects.
    Settings that are automatically defined:
    - basedir
    - last working directory (lwd) - initially usr/worked - but can be overriden
    by settings from the loaded model (project.xml)
    
    Settings that are loaded from XML files:
    - menu widget ??? - put the path to resources in the XML file menu.xml ???
    - upper toolbox widget ??? - same as for the menu widget ???
    - canvas widget
    - XML Editor
    - console
    - status bar???"""
    
    def __init__(self):
        """TODO:: define actions ..."""
        dict.__init__(self)
		
		# settings to be loaded from files (or determined)
        self["basedir"] = os.getcwd().replace("bin", "") # assumes that the main script starts from the
                                                         # bin directory
        self["lwd"] = os.getcwd().replace("bin", "")     # last working directory - priority:
                                                         # 1. load from project (trunk) settings file and only if it is present. 
                                                         # 2. use etc/paths.xml "LastWorkingDir" element
                                                         # 3. use self["basedir"] which assumes the same location as initall.py script

        # ----------------------------- widgets settings ----------------------------- 

        # Menu
        self["menuIconsPath"] = os.path.join(self["basedir"], "resources/icons16x16/menu") # add possibilities for multiple resolutions        
        self["menuXMLPath"]   = os.path.join(self["basedir"], "etc/gui/menus.xml") 
        self["menu"]          = {"icons":{}}
        
        # Upper toolbox
        self["upperToolBoxIconsPath"] = os.path.join(self["basedir"], "resources/icons22x22/uptoolbox")
        self["upperToolBoxXMLPath"]   = os.path.join(self["basedir"], "etc/gui/uppertoolbox.xml")
        self["upperToolBox"]          = {"icons":{}}
        
        # Canvas
        self["canvasXMLPath"] = os.path.join(self["basedir"], "etc/gui/canvas.xml")
        self["canvas"]        = {}
        # ----------------------------------------------------------------------------
        
        # other useful paths
        self["extraModulesPath"] = {} # relative/absolute paths???
        self["XMLPath"] = os.path.join(self["basedir"], "etc/paths.xml") # canvas.xml and others ???
        
        self.__parseXMLData()

    def __parseXMLData(self): # canvas.xml and others ???
        """Parses the default paths.xml file into the self["extraModulesPath"]"""

        tree = ET.parse(self["XMLPath"])
        root = tree.getroot()
        
        # modules:
        
        for i in root.getiterator('module'):
            self["extraModulesPath"][i[0].text] = i[1].text
            
        # lwd:
        
    def addXMLData(self, data, element):
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
            
            if data == "lwd":
                self['lwd'] = element
                lwd = root.find(data)
                lwd.text = element
         
            tree.write(self["XMLPath"], encoding = "UTF-8")
         
    def removeXMLData(self, data, element):
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
            
            if data == "lwd": # resets to default /usr/worked
                self['lwd'] = 'usr/worked'
                lwd = root.find(data)
                lwd.text = 'usr/worked'
                
            tree.write(self["XMLPath"], encoding = "UTF-8")
        
    def __call__(self, project.xml): # must define
        """Call the settings instance with the project.xml settings in order to 
        override some of its attributes with the information found in it."""
        pass

if __name__ == '__main__':
    obj = settings()
    #obj.addXMLData("lwd", 'xxxyyy/xxxyyy/zzyyxx')
    obj.removeXMLData('modules', 'bleah')
