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

import tkinter, math
from xml.dom import minidom # functionality that should be moved to other objects
from ..cad import fkernel   # functionality that should be moved to other objects

# should be associated with some options (callbacks) from Settings menu

class DrawingArea(tkinter.Canvas):
    """Enhanced Canvas widget for CAD drawings."""
    def __init__(self, master, xmlfile):
        tkinter.Canvas.__init__(self, master)

        self.master=master
        self.focus_force()

        self.xmlfile=xmlfile
        self.options=self.__parseXml()    # must be passed to the Canvas somehow - must be moved from here ;)
        self.psize=self.__pointSz()       # compute once/stay the same for the whole session

        self["background"] = "black"
        self.defaultFg = "white"

        self.scale_f2i=[0.1, 10]                                      # 100 mm at 10 pixels - should be moved to xml configuration file
        self.translatedFactor = [tkinter.IntVar(), tkinter.IntVar()]  # only for integer representation of pixels; [h, w]
        self.zoomedFactor = 1.1                                       # zoom 10 %

        self.translatedFactor[0].set(0)
        self.translatedFactor[1].set(0)

        self.currentPos=[tkinter.IntVar(), tkinter.IntVar()]
        self.currentDir=[tkinter.IntVar(), tkinter.IntVar()]

        self.csys={}

        # add data like self.points["label"]={"floatinfo":fkernel.point(**options),
        #                                     "intPosition":[x, y],
        #                                     "graphRepr":{}}
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

    def __pointSz(self, size=0.5):
        """Computes the size as being size % of the root window max(width, height)."""
        a = max(int(size/100.0*float(self.master.winfo_screenwidth())),
                int(size/100.0*float(self.master.winfo_screenheight()))) # always rounding towards zero
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
        for i in list(self.csys.keys()):
            self.csys[i]["intPosition"][0]+=event.x-self.currentDir[0].get()
            self.csys[i]["intPosition"][1]+=event.y-self.currentDir[1].get()
        # self.points
        for i in list(self.points.keys()):
            self.points[i]["intPosition"][0]+=event.x-self.currentDir[0].get()
            self.points[i]["intPosition"][1]+=event.y-self.currentDir[1].get()

    def zoom(self, event): # scroll wheel zoom
        if event.num == 4: # scrolled up
            lfactor = self.zoomedFactor
        if event.num == 5: # scrolled down
            lfactor = 1.0/self.zoomedFactor

        # MSWindows
        if event.delta == 120: # scrolled up
            lfactor = self.zoomedFactor
        if event.delta == -120: # scrolled down
            lfactor = 1.0/self.zoomedFactor

        self.scale_f2i[1] *= lfactor

        # zoom csys

        for i in list(self.csys.keys()):
            # new

            xNew = lfactor*self.csys[i]["intPosition"][0]+self.currentPos[0].get()*(1-lfactor)
            yNew = lfactor*self.csys[i]["intPosition"][1]+self.currentPos[1].get()*(1-lfactor)

            self.move(i, xNew-self.csys[i]["intPosition"][0], yNew-self.csys[i]["intPosition"][1])

            self.csys[i]["intPosition"][0]=xNew
            self.csys[i]["intPosition"][1]=yNew

        # zoom points
        for i in list(self.points.keys()):
            # new

            xNew = lfactor*self.points[i]["intPosition"][0]+self.currentPos[0].get()*(1-lfactor)
            yNew = lfactor*self.points[i]["intPosition"][1]+self.currentPos[1].get()*(1-lfactor)

            self.move(i, xNew-self.points[i]["intPosition"][0], yNew-self.points[i]["intPosition"][1])

            self.points[i]["intPosition"][0]=xNew
            self.points[i]["intPosition"][1]=yNew

        # zoom lines

    def dispCsys(self, intPos, length=12, rotation=0, visible=1):  # length option [%] should be moved to xml canvas settings file
        """Graphically creates and display a coordinate system"""

        if visible == 1:
            state=tkinter.NORMAL
        else:
            state=tkinter.HIDDEN

        return [self.create_line(intPos[0], intPos[1], intPos[0]+int(length*self.psize*math.cos(rotation/180.0*3.14159)), intPos[1]-int(length*self.psize*math.sin(rotation/180.0*3.14159)), arrow=tkinter.LAST, fill=self.defaultFg, state=state),
                self.create_line(intPos[0], intPos[1], intPos[0]-int(length*self.psize*math.sin(rotation/180.0*3.14159)), intPos[1]-int(length*self.psize*math.cos(rotation/180.0*3.14159)), arrow=tkinter.LAST, fill=self.defaultFg, state=state)] # 0x axis, Oy axis

    def dispPoint(self, intPos, representation, color, visible=1, filled=0):
        """Graphically creates and display on canvas a point entity"""

        if visible == 1:
            state=tkinter.NORMAL
        else:
            state=tkinter.HIDDEN

        if color == "default":
            color=self.defaultFg

        if filled ==1:
            fill=color
        else:
            fill=self["background"]

        if representation == "square": # to add possibility for active fill
            idPoint=self.create_rectangle(intPos[0]-self.psize, intPos[1]-self.psize,
                                          intPos[0]+self.psize, intPos[1]+self.psize,
                                          outline=color, fill=fill, state=state)
        if representation == "circle":
            idPoint=self.create_oval(intPos[0]-self.psize, intPos[1]-self.psize,
                                     intPos[0]+self.psize, intPos[1]+self.psize,
                                     outline=color, fill=fill, state=state)
        if representation == "triangle":
            idPoint=self.create_polygon(intPos[0], intPos[1]-int(2*self.psize*1.73/3.0),
                                        intPos[0]-self.psize, intPos[1]+int(2*self.psize*1.73/6.0),
                                        intPos[0]+self.psize, intPos[1]+int(2*self.psize*1.73/6.0),
                                        outline=color, fill=fill, state=state)

        return idPoint

    def setGlobalCsys(self): # length option [%] should be moved to xml canvas settings file
        """Creates the global coordinate system. """

        if "global" not in list(self.csys.keys()):
            self.csys["global"]={}
            self.csys["global"]["intPosition"]=[self.winfo_width()/2+self.translatedFactor[0].get(),
                                                self.winfo_height()/2+self.translatedFactor[1].get()]

            self.csys["global"]["floatinfo"]=fkernel.csys([0.0, 0.0])

            # graphical stuff
            self.csys["global"]["graphRepr"]={}
            self.csys["global"]["graphRepr"]["visible"]=1 # to modify this setting in order to be loaded from canvas xml settings file
            self.csys["global"]["graphRepr"]["entities"]=self.dispCsys([self.csys["global"]["intPosition"][0], self.csys["global"]["intPosition"][1]], rotation=0.0)

            self.csys["global"]["graphRepr"]["tags"]=["global", "csys", "translate"]

            for i in self.csys["global"]["graphRepr"]["tags"]:
                self.addtag_withtag(i, self.csys["global"]["graphRepr"]["entities"][0])
                self.addtag_withtag(i, self.csys["global"]["graphRepr"]["entities"][1])

            # register the global coordinate system into the XML tree
            # like so <CSys id="global" parent="none" type="cartesian">0.0 0.0 0.0</CSys>
            g_csys=self.master.xmlprojfiles["geometry"][0].createElement("Csys")
            g_csys.setAttribute('id', 'global')
            g_csys.setAttribute('parent', 'none')
            g_csys.setAttribute('type', 'cartesian')
            g_csys.appendChild(self.master.xmlprojfiles["geometry"][0].createTextNode("0.0 0.0 0.0"))
            self.master.xmlprojfiles["geometry"][2][0].appendChild(g_csys)

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
