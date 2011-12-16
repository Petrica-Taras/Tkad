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

import Tkinter, math
from xml.dom import minidom
from ..cad import fkernel

# should be associeted with some options (callbacks) from Settings menu

class DrawingArea(Tkinter.Canvas):
    """Enhanced Canvas widget for CAD drawings. For now with limited options: no user predefined colors, colors schemes, etc."""
    def __init__(self, master, xmlfile):		
        """options={"bgcolor":"black", "def_fgcolor":"white", "slcolor":"orange", "pointshape":"square", "predef_colorsch":"User", "userdef_colors":"Values"}"""
        Tkinter.Canvas.__init__(self, master)
        
        self.master=master  
        self.focus_force()
        
        self.xmlfile=xmlfile
        self.options=self.__parseXml()    # must be passed to the Canvas somehow	
        self.psize=self.__pointSz()       # compute once/stay the same for the whole session

        self["background"]="black"
        
        self.scale_f2i=[0.001, 10]    # 1 mm at 10 pixels - should be moved to xml configuration file
        self.translatedFactor = [Tkinter.IntVar(), Tkinter.IntVar()]  # only for integer representation of pixels; [h, w] 
        self.zoomedFactor = Tkinter.IntVar()                          # only for integer representation of pixels
        
        self.translatedFactor[0].set(0)
        self.translatedFactor[1].set(0)
        self.zoomedFactor.set(1)
        self.currentPos=[Tkinter.IntVar(), Tkinter.IntVar()]
        self.currentDir=[Tkinter.IntVar(), Tkinter.IntVar()]

        self.csys={}        
        self.globalCsys={} 

        # add data like self.points["label"]={"floatinfo":fkernel.point(**options), "intPosition":[x, y], "graphRepr":{}}
        self.points={}
        self.segments={}
        self.arcs={} # begin with a single type of an arc.
        
        self.faces={}
        
        # bindings
        self.bind("<Button-3>", self.__startRec)        
        self.bind("<Motion>", self.__updateCurrentPos, add="+")   
        self.bind_all("<Motion><ButtonRelease-3>", self.translate, add="+")   
        self.master.bind("<MouseWheel>", self.zoom, add="+") # zoom MSWindows
        self.master.bind("<Button-4>", self.zoom, add="+")   # zoom Linux
        self.master.bind("<Button-5>", self.zoom, add="+")   # zoom Linux                  

    def __pointSz(self, size=1.0):
        """Computes the size as being size % of the root window max(width, height)."""
        a = max(int(size/100.0*float(self.master.winfo_screenwidth())), int(size/100.0*float(self.master.winfo_screenheight()))) # always rounding towards zero
        if not a%2: a=a/2
        else: a=(a+1)/2
        return a
    
    def __parseXml(self):
        """Parse the canvas settings and if it is necessary the settings associated with the model."""
        pass
       
    def translate(self, event): 
        self.move("translate", event.x-self.currentDir[0].get(), event.y-self.currentDir[1].get())
        # update the canvas integer coordinates of all the involved entities:
        
        # self.csys
        for i in self.csys.keys():
            self.csys[i]["intPosition"][0]+=event.x-self.currentDir[0].get()
            self.csys[i]["intPosition"][1]+=event.y-self.currentDir[1].get()
        # self.points ???
 
        print "Cannot update point representations on canvas" 
     
    def zoom(self, event): # scroll wheel zoom
        print "Not implemented yet" 		    		
    
    def dispCsys(self, intPos, length=6, rotation=0, visible=1):  # length option [%] should be moved to xml canvas settings file
        """Graphically creates and display a coordinate system"""   
        
        if visible == 1:
            state=Tkinter.NORMAL
        else:
            state=Tkinter.HIDDEN
            
        return [self.create_line(intPos[0], intPos[1], intPos[0]+int(length*self.psize*math.cos(rotation/180.0*3.14159)), intPos[1]-int(length*self.psize*math.sin(rotation/180.0*3.14159)), arrow=Tkinter.LAST, fill="white", state=state), 
                self.create_line(intPos[0], intPos[1], intPos[0]-int(length*self.psize*math.sin(rotation/180.0*3.14159)), intPos[1]-int(length*self.psize*math.cos(rotation/180.0*3.14159)), arrow=Tkinter.LAST, fill="white", state=state)] # 0x axis, Oy axis    

    def setGlobalCsys(self): # length option [%] should be moved to xml canvas settings file
        """Creates the global coordinate system."""
          
        self.globalCsys["intPosition"]=[self.winfo_width()/2+self.translatedFactor[0].get(), self.winfo_height()/2+self.translatedFactor[1].get()]  
        
        if self.zoomedFactor != 1: # modifications needed
            self.globalCsys["intPosition"][0]-=self.currentPos[0].get()*self.zoomedFactor.get() # ???
            self.globalCsys["intPosition"][1]-=self.currentPos[1].get()*self.zoomedFactor.get() # ???

        self.globalCsys["floatinfo"]=fkernel.csys([0.0, 0.0])
 
        # graphical stuff
        self.globalCsys["graphRepr"]={}
        self.globalCsys["graphRepr"]["visible"]=1 # to modify this setting in order to be loaded from canvas xml settings file
        self.globalCsys["graphRepr"]["entities"]=self.dispCsys([self.globalCsys["intPosition"][0], self.globalCsys["intPosition"][1]], rotation=0.0)
        
        self.globalCsys["graphRepr"]["tags"]=["global", "csys", "translate"] 
        
        for i in self.globalCsys["graphRepr"]["tags"]: 
            self.addtag_withtag(i, self.globalCsys["graphRepr"]["entities"][0])
            self.addtag_withtag(i, self.globalCsys["graphRepr"]["entities"][1])               
        
        self.csys["global"]=self.globalCsys # the rest of the coordinate systems will always have at least self.csys["global"] as a parent

    def float2int(self, csys_ints, reals, type_):
        """Transforms float coordinates into canvas coordinates."""
        # for now with no respect to the translation & zooming
        # but it can deal with polar coordinate systems
        
        if type_ == "polar": # determine the canvas local (with respect to csys_ints) coordinates in cartesian
            localv = reals[0]*math.cos(reals[1]/180.0*3.14159), reals[0]*math.sin(reals[1]/180.0*3.14159)
        else:
            localv = reals[0], reals[1]  
        return [csys_ints[0]+int(localv[0]*self.scale_f2i[1]/self.scale_f2i[0]), 
                csys_ints[1]-int(localv[1]*self.scale_f2i[1]/self.scale_f2i[0])]	

    def __updateCurrentPos(self, event):
        """updates the self.CurrentPos attribute with the current cursor position"""
        self.currentPos[0].set(event.x)
        self.currentPos[1].set(event.y)

    def __startRec(self, event):
        """records the event.x, event.y if the right click is pressed"""
        self.currentDir[0].set(event.x)
        self.currentDir[1].set(event.y)
