import Tkinter
from xml.dom import minidom
#from ..cad import fkernel, ikernel ???

# should be associeted with some options (callbacks) from Settings menu

class DrawingArea(Tkinter.Canvas):
    """Enhanced Canvas widget for CAD drawings. For now with limited options: no user predefined colors, colors schemes, etc."""
    def __init__(self, master, xmlfile):		
        """options={"bgcolor":"black", "def_fgcolor":"white", "slcolor":"orange", "pointshape":"square", "predef_colorsch":"User", "userdef_colors":"Values"}"""
        Tkinter.Canvas.__init__(self, master)
        self.xmlfile=xmlfile
        self.options=self.__parseXml()    # must be passed to the Canvas somehow	
        self.psize=self.__pointSz() # compute once/stay the same for the whole session

        self["background"]="black"
        
        self.scale_f2i=[0.001, 10]    # 1 mm at 10 pixels
        self.translatedFactor=[0, 0]  # only for integer representation of pixels 
        self.zoomedFactor=0           # only for integer representation of pixels

        self.csys={}
        # add data like self.points.append({"label":"label", "floatinfo":fkernel.point(**options), "intinfo":ikernel.something, "representation":{}})
        self.points={}
        self.segments={}
        self.arcs={} # begin with a single type of an arc.
        
        self.faces={}

    def __pointSz(self, size=1):
        """Computes the size as being size % of the canvas max(height, width)."""
        a = max(int(size/100.0*float(self["height"])), int(size/100.0*float(self["width"]))) # always rounding towards zero
        if not a%2: a=a/2
        else: a=(a+1)/2
        return a
    
    def __parseXml(self):
        pass
       
    def translate(self):
        pass
     
    def zoom(self): # scroll wheel zoom
        pass

    def addCsys(self): # a default global csys must be added
        pass
        
    def addPoint(self, **options): # here or in geometry menu callbacks? maybe there since it would simplify some things
        pass    		
    
    def addSegment(self, **options):
        pass
     
    def addArc(self, **options):
        pass
        
    def detectFaces(self, **options):
        pass		    		    		    
