# This module provides the CAD widget and the additional windows to collect information

from Tkinter import *
import gdefs

class CAD(Canvas):
    """A CAD Widget. Exports essential information like the graph matrix."""
    def __init__(self, master, **options):
        """options={"size":(1000, 100), "bgcolor":"black", "fgcolor":"white", "select":"orange"}"""
        Canvas.__init__(self, master)
        self.options=options
        self["width"]=self.options["size"][0] # this quantity is negotiated relative to the other widgets present
                                                           # on the root window. The code that does this is placed outside this widget
        self["height"]=self.options["size"][1] # canvas should have a minimum h/w imposed
        self["background"]=self.options["bgcolor"]

        self.globalSys={"name":"global", "size":2, "origin":[0.0, 0.0], "gcoords":[int(self.options["size"][0]/2.0), int(self.options["size"][1]/2.0)], "color":"blue", "parents":{}, "type":"cartesian", "visible":1, "children":{}} # canvas center 
        # data management:
        self.coordsys={} # format key:value -> "CsysTag":{"tags":["all", "zoomable", "TagOx", "TagOy"], "id":[id_Ox, id_Oy], "cSysObject":gCoordSys}
        self.points={}   # format key:value -> "pointTag":{"tags":["all", "zoomable"], "id":id, "pointObject":gPoint}
        self.segments={}    # format key:value -> "LineTag":{"type":"segment", "points_tags":[P1_Tag, P2_Tag], "tags":[], "id":id, "lineObject":gSegment}
        self.contours={}

        self.distance=IntVar()   # pixels/1 m
        self.distance.set(1000)  # modifiable by zoom methods family
        self.a=self.__pointSz() # compute once/stay the same for the whole session
        self.addCooSys()
        self.CurrentPos= IntVar(), IntVar()
        self.CurrentDir= IntVar(), IntVar()
        self.selectionFlag=0 # bytearray? and corelated with the type of selected entity
        self.scaleFactor=0

        # bindings
        self.bind("<Button-3>", self.__startRec)
        self.bind("<Motion>", self.__updateCurrentPos)
        self.bind("<Button-3><Motion><ButtonRelease-3>", self.__translation, add="+")
        #self.master.bind("<MouseWheel>", self.__zoom, add="+")
        self.master.bind("<Button-4>", self.__zoom, add="+")
        self.master.bind("<Button-5>", self.__zoom, add="+")        

    def __pointSz(self, size=1):
        """Computes the size as being size % of the canvas max(height, width)."""
        a = max(int(size/100.0*float(self["height"])), int(size/100.0*float(self["width"]))) # always rounding towards zero
        if not a%2: a=a/2
        else: a=(a+1)/2
        return a

    def __float2int(self, origin, xy):
        """Based on the self.distance, the (x,y) coordinates in pixels are determined with respect
           to the coordinate system. The coordinate system is also given in pixels (so the ypoint
           coordinate should be given with minus sign. It returns the points coordinates, in pixels,
           with respect to the upper left corner."""

        return [int(xy[0]*self.distance.get())+origin[0], origin[1]-int(xy[1]*self.distance.get())]

    def addSegm(self, p1_tag, p2_tag, segname, color, visible):
        """Adds segments to Canvas. A tag and an ID are created. The points defining the lines have the children field updated (with the new line).
        The line is at the bottom"""
        iSeg=gdefs.gSegment(self.points[p1_tag]["pointObject"], self.points[p2_tag]["pointObject"], segname, color, visible)
        idSeg=self.create_line(iSeg["p1"]["gcoords"], iSeg["p2"]["gcoords"], fill=iSeg["color"], state=iSeg["visible"])
        # add appropriate tags - TODO!!! + update the parents (the points)

    def addPoint(self, point):
        """Adds point to Canvas. A tag and an ID is created and the self.points is updated. Most
           importantly the gcoords data is computed."""

        if point["filled"]: fill=point["color"]
        else:               fill=self["background"]

        if point["gcoords"] == []: point["gcoords"]=self.__float2int(point["sys"]["gcoords"], point["rcoords"])
        if point["shape"] =="square":  # square
            id_point=self.create_rectangle(point["gcoords"][0]-self.a, point["gcoords"][1]-self.a, point["gcoords"][0]+self.a, point["gcoords"][1]+self.a, outline=point["color"], fill=fill, activefill=self.options["select"], activeoutline=self.options["select"], activewidth=4)
        else:                                                         # round
            id_point=self.create_oval(point["gcoords"][0]-self.a, point["gcoords"][1]-self.a, point["gcoords"][0]+self.a, point["gcoords"][1]+self.a, outline=point["color"], fill=fill, activefill=self.options["select"], activeoutline=self.options["select"], activewidth=4)

        # add relevant tags
        self.addtag_withtag("point", id_point)
        self.addtag_withtag(point["name"], id_point)
        #self.addtag_withtag("zoomable", id_point)
        self.addtag_withtag("all", id_point)
        # register the entity in self.points:
        self.points[point["name"]]={"tags":["point", point["name"], "zoomable", "all"], "id":id_point, "pointObject":point}

    def addCooSys(self, cSys=None, length=6):
        """Adds coordinate systems (two orthogonal lines with arows) on the canvas"""
        if cSys==None: 
            cSys=self.globalSys
        else:           # gcoords
            # for every other csys than global, the gcoords must be determined with respect to upper left
            if cSys["local"]==1:
                cSys["gcoords"]=self.__float2int(self.globalSys["gcoords"], cSys["origin"])
            else: # it is global, like self.globalSys
                t_gcoords=[cSys["origin"][0]-self.globalSys["origin"][0], cSys["origin"][1]-self.globalSys["origin"][1]]
                cSys["gcoords"]=self.__float2int(self.globalSys["gcoords"], t_gcoords)

        id_Oy=self.create_line(cSys["gcoords"][0], cSys["gcoords"][1], cSys["gcoords"][0], cSys["gcoords"][1]-2*length*self.a, arrow=LAST, fill=cSys["color"]) # Oy axis
        id_Ox=self.create_line(cSys["gcoords"][0], cSys["gcoords"][1], cSys["gcoords"][0]+2*length*self.a, cSys["gcoords"][1], arrow=LAST, fill=cSys["color"]) # Ox axis

        # adding relevant tags and registering into self.coordsys
        self.addtag_withtag(cSys["name"], id_Oy)
        self.addtag_withtag(cSys["name"], id_Ox)
        self.addtag_withtag("all", id_Oy)
        self.addtag_withtag("all", id_Ox)
        self.tag_lower(cSys["name"])

        self.coordsys[cSys["name"]]={"tags":["cSys", cSys["name"], "all"], "id":[id_Ox, id_Oy], "cSysObject":cSys}
        
    def delCooSys(self, CSys):
        pass

    def __updateCurrentPos(self, event):
        """updates the self.CurrentPos attribute with the current cursor position"""
        self.CurrentPos[0].set(event.x)
        self.CurrentPos[1].set(event.y)

    def __startRec(self, event):
        """records the event.x, event.y if the right click is pressed"""
        self.CurrentDir[0].set(event.x)
        self.CurrentDir[1].set(event.y)

    def __translation(self, event): 
        self.move("all", event.x-self.CurrentDir[0].get(), event.y-self.CurrentDir[1].get())
        # update the gcoords key of all the involved entities:

        for i in self.coordsys.keys():
            self.coordsys[i]['cSysObject']["gcoords"]=[self.coordsys[i]['cSysObject']["gcoords"][0]+event.x-self.CurrentDir[0].get(), self.coordsys[i]['cSysObject']["gcoords"][1]+event.y-self.CurrentDir[1].get()]
        for i in self.points.keys():
            self.points[i]["pointObject"]["gcoords"]=[self.points[i]["pointObject"]["gcoords"][0]+event.x-self.CurrentDir[0].get(), self.points[i]["pointObject"]["gcoords"][1]+event.y-self.CurrentDir[1].get()]
        # to add lines, contours :D
        for i in self.segments.keys():
            self.segments[i]			
        
    def __zoom(self, event):
        """My own implementation of the zoom function"""

        zoomFactor = 1        
        if event.num==4:   
            zoomFactor+=0.01
            self.scaleFactor+=1
        else:              
            zoomFactor-=0.01
            self.scaleFactor-=1

        for i in self.coordsys.keys():	     
            oldcoords = self.coordsys[i]['cSysObject']["gcoords"][0], self.coordsys[i]['cSysObject']["gcoords"][1]
            offset = oldcoords[0]-self.CurrentPos[0].get(), oldcoords[1]-self.CurrentPos[1].get()
            print self.coordsys[i]['cSysObject']["gcoords"] 
            self.coordsys[i]['cSysObject']["gcoords"][0], self.coordsys[i]['cSysObject']["gcoords"][1] = int(zoomFactor*self.coordsys[i]['cSysObject']["gcoords"][0]), int(zoomFactor*self.coordsys[i]['cSysObject']["gcoords"][1])
            print self.coordsys[i]['cSysObject']["gcoords"]
            self.move(self.coordsys[i]["id"][0], -(self.coordsys[i]['cSysObject']["gcoords"][0]-oldcoords[0]), -(self.coordsys[i]['cSysObject']["gcoords"][1]-oldcoords[1]))     
            self.move(self.coordsys[i]["id"][1], -(self.coordsys[i]['cSysObject']["gcoords"][0]-oldcoords[0]), -(self.coordsys[i]['cSysObject']["gcoords"][1]-oldcoords[1]))       
                        
        for i in self.points.keys():
            direction = self.CurrentPos[0].get()-self.points[i]["pointObject"]["gcoords"][0], 1+self.CurrentPos[1].get()-self.points[i]["pointObject"]["gcoords"][1]			
            
            oldcoords = self.points[i]["pointObject"]["gcoords"][0], self.points[i]["pointObject"]["gcoords"][1]
            
            self.points[i]["pointObject"]["gcoords"][0], self.points[i]["pointObject"]["gcoords"][1] = int(zoomFactor*self.points[i]["pointObject"]["gcoords"][0]), int(zoomFactor*self.points[i]["pointObject"]["gcoords"][1])
            
            self.move(self.points[i]["id"], -(self.points[i]["pointObject"]["gcoords"][0]-oldcoords[0]), -(self.points[i]["pointObject"]["gcoords"][1]-oldcoords[1]))
            
            
if __name__=="__main__":
    root=Tk()
    drwOpt={"size":(800, 600), "bgcolor":"black", "fgcolor":"green", "select":"orange"}
    drw=CAD(root, **drwOpt)                   #initiate the CAD widget
    drw.pack(fill=BOTH, expand=YES)

    a = gdefs.gPoint(drw.globalSys, "P1", [0.0, -0.02], "green", "round", 1, 1, {})
    b = gdefs.gPoint(drw.globalSys, "P2", [0.02, 0.1], "green", "round", 1, 1, {})
    c = gdefs.gPoint(drw.globalSys, "P3", [0.1, 0.0], "green", "round", 1, 1, {})
    drw.addPoint(a)
    drw.addPoint(b)
    drw.addPoint(c)

    # lines:
    #drw.addSegm("P1", "P2", "S1", "green", NORMAL)
    #drw.addSegm("P2", "P3", "S2", "green", NORMAL)
    #drw.addSegm("P1", "P3", "S3", "green", NORMAL)

    root.mainloop()
