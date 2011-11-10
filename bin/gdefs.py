# graphical entities definitions
# here are defined the graphical entities (in CAD module they are displayed only)
# also here should be defined the windows for collecting the informations.
# due to the definitions from this module, the CAD functions for display can be made much simpler and shorter

import math

class gCsys(dict):
    def __init__(self, name, origin, color, parents, type, visible, size=2):
        dict.__init__(self)
        self["name"]=name # a string i.e. "globalS". Also to be used as tag
        self["size"]=size
        self["origin"]=origin
        self["gcoords"]=[]
        self["color"]=color
        self["parents"]=parents
        if self["parents"] == {}:
            self["local"]=1
        else:
            self["local"]=0
        self["type"]=type # cartesian
        self["visible"]=visible
        self["children"]={"points":[], "lines":[], "csys":[]}
    def __repr__(self):
        if self["gcoords"]==[]:
            gc = "\n      Pixels  :"
        else:
            gc = "\n      Pixels  :"+str(self["gcoords"][0])+", "+str(self["gcoords"][1])
        return "Point "+self["name"]+"\n"+("-"*len("Point "+self["name"]))+"\n      CoordSys: "+self["sys"]["name"]+"\n      Coords  : "+str(self["rcoords"][0])+", "+str(self["rcoords"][1])+gc
        

class gPoint(dict):
    def __init__(self, coordsys, name, rcoords, color, shape, filled, visible, parents):
        dict.__init__(self)
        self["sys"]=coordsys     # coordinate system object
        self["name"]=name
        self["rcoords"]=rcoords  # with respect to the self["sys"] object
        self["gcoords"]=[]  # with respect to the upper left corner. they are computed by the CAD widget
        self["color"]=color
        self["shape"]=shape
        self["filled"]=filled
        self["visible"]=visible
        self["parents"]=parents # coordinate systems
        self["children"]={"points":[], "lines":[], "geomTrans":[]} # immediate children (like points, lines and geometrical transformations)
    def computeDistance(self, SecondPoint):
        distance=0.0
        for i in range(0, self["sys"].size): distance+=(self.rcoords[i]-SecondPoint.rcoords[i])**2
        return math.sqrt(distance)
    def __repr__(self):
        if self["gcoords"]==[]:
            gc = "\n      Pixels  :"
        else:
            gc = "\n      Pixels  :"+str(self["gcoords"][0])+", "+str(self["gcoords"][1])
        return "Point "+self["name"]+"\n"+("-"*len("Point "+self["name"]))+"\n      CoordSys: "+self["sys"]["name"]+"\n      Coords  : "+str(self["rcoords"][0])+", "+str(self["rcoords"][1])+gc


class gSegment(dict):
    def __init__(self, p1, p2, name, color, visible):
        dict.__init__(self)
        self["p1"]=p1
        self["p2"]=p2
        self["color"]=color
        self["visible"]=visible
        self["parents"]={"p1":p1, "p2":p2}
        self["children"]={"points":[], "lines":[], "geomTrans":[], "contours":[]}
    def __len__(self): self["p1"].computeDistance(self["p2"])
