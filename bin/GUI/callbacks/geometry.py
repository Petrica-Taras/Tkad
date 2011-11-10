from ..widgets import csys, point
from ..cad import fkernel, ikernel

def newCSys(app):
    x=csys.csys(app)
    data=x()

def newPoint(app):
    x=point.point(app)
    data=x() # a bunch of Tkinter.StringVars
    # register newly created point to DrawingArea
    # at least label, float and int information so far:
    floatRepr=fkernel.point(label=data[0].get(), csys=data[3].get(), coords=[float(data[1].get()), float(data[2].get())])
    intRepr=ikernel.float2ints(self.floatRepr.coords, app.DrawingArea)
    app.DrawingArea.points[floatRepr.label]={"floatRepr":floatRepr, "intRepr":intRepr}	# to add color/shape representation later

def newSegment():
    print "New Segment: Not implemented yet!"
    
def newArc():
    print "New Arc: Not implemented yet!"    
    
def detectFaces():
    print "Detect Faces: Not implemented yet!"		
