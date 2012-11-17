import xml.etree.ElementTree as ET

import os

class settings(dict):  # hold and centralize the main settings in a dict like class (with additional methods to load the settings)
                       # what settings do I need? 
                       # also holds states
                       # the main idea is to hold stuff commonly required by several objects
    """Just a container for most settings shared between several objects."""
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

        # widgets settings
        self["menuIconsPath"] = os.path.join(self["basedir"], "resources/icons16x16/menu") # add possibilities for multiple resolutions        
        self["menuXMLPath"]   = os.path.join(self["basedir"], "etc/gui/menus.xml") 
        
        self["upperToolBoxIconsPath"] = os.path.join(self["basedir"], "resources/icons22x22/uptoolbox")
        self["upperToolBoxXMLPath"]   = os.path.join(self["basedir"], "etc/gui/uppertoolbox.xml")
                             
        # other usefull paths
        self["extraModulesPath"] = {} # add possibility in settings to add/remove values
        self["XMLPath"] = os.path.join(self["basedir"], "etc/paths.xml") # canvas.xml and others ???
        
        self.__parseXMLData()

    def __parseXMLData(self): # canvas.xml and others ???
        """Parses the default paths.xml file into the self["extraModulesPath"]"""

        tree = ET.parse(self["XMLPath"])
        root = tree.getroot()
        
        # modules:
        
        for i in root.getiterator('module'):
            self["extraModulesPath"][i[0].text] = i[1].text

    def __call__(self, xmlSettingsFilePath): # call the instance with various settings????
        # call the object with the new settings imposed by the project.xml file???
        pass

