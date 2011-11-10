import Tkinter, collections, functools
from ..callbacks import *
from xml.dom import minidom

class MenuToolbar(Tkinter.Menu):
    """A Menu Class holding all the Menu related stuff (except for the callbacks). It is based on a XML file."""	
    def __init__(self, master, xmlfile):
        Tkinter.Menu.__init__(self, master=master)
        self.master=master
        self.master.config(menu=self)       
         
        self.xmlfile=xmlfile
        		
        self.MenuTree=collections.OrderedDict()
        
        self.createMenuTree() 
        
        self.menus=[]           # in order to have access to the widgets later  
        
        self.createMenu()
        
        self.master.update_idletasks()
        
    def createMenuTree(self):
        """Extracts the information from the xml file and creates a tree containing the menu name entry and the associated callbacks name."""		
        xmlmenu=minidom.parse(self.xmlfile)
        MenuXMLRoot=xmlmenu.firstChild		
        for i in MenuXMLRoot.childNodes: 
            if i.nodeName != "#text":
                self.MenuTree[i.attributes["name"].value]=collections.OrderedDict()
                for j in i.childNodes:
                    if j.nodeName != "#text":
                        self.MenuTree[i.attributes["name"].value][j.attributes["name"].value]={"callback":j.attributes["callback"].value}	

    def createMenu(self):
        """It actually creates the menu widgets"""
        indexer=0
        for i in self.MenuTree.keys(): 
            self.menus.append(Tkinter.Menu(self))
            self.add_cascade(label=i, menu=self.menus[indexer])
            indexer+=1

        indexer=0
        for i in self.MenuTree.keys():
            for j in self.MenuTree[i]:			
                self.menus[indexer].add_command(label=j, command=functools.partial(eval(i.lower()+"."+self.MenuTree[i][j]["callback"]), self.master))	
            indexer+=1	
