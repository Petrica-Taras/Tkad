import os

class common(dict): # hold and centralize the main settings in a dict like class (with additional methods to load the settings)
                       # what settings do I need? 
                       # also holds states
                       # the main idea is to hold stuff commonly required by several objects
    """Just a container for most settings shared between several objects.
    TODO:: Move the XML settings (including the parsing) and paths in this
    newly created object."""
    def __init__(self):
		dict.__init__(self)
		"""TODO:: define actions ..."""
		
		# settings to be loaded from files (or determined)
        self["basedir"] = os.getcwd()).replace("bin", ""
        self["lwd"] = None # last working directory - load from project (trunk) settings
                        # file and only if it is present. Otherwise use self.basedir

        self["menuIconsPath"] = "resources/icons16x16/menu" # add possibilities for multiple resolutions
        
        self["menuXMLPath"]   = "etc/gui/menus.xml" 
        
        self["upperToolBox"]  = "etc/gui/uppertoolbox.xml"
                  
        self.menusEnabled = {"Project": 0} # disabled (0) or enabled (1)?
                                           # must be able to do this in real time (Tkinter.StringVar()???)
                         

    def __parseXML(self):
		"""Reads the XML settings file into a nice data structure"""
        pass
        
    def register(self):
        pass # register to where?

    def __loadNewSettings(self):
        pass

    def __loadOpenSettings(self):
		pass

    def __call__(self, xmlSettingsFilePath):
        pass
