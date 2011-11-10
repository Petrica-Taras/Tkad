# provides functions to deal with floating numbers on a drawing area 
#(transformations, scale, distances, length, symbolic representations, etc)

# geometric precision

class csys():
    """2D coordonate system data structure:

Parameters: 
    * label: it is the structure associated name
    * parent: the parent coordinate system (all systems have at least global as parent)
    * origin: a tuple containing the origin (with respect to the parent if it exists - if not to the global)
    * rotation: a float representing the angle of the Ox axis (with respect to the parent if it exists - if not to the global)
    """	
    def __init__(self, origin, parent=None, rotation=None, label="global", type_="cartesian"):
        self.origin=origin
        self.parent=parent			
        self.rotation=rotation
        self.symbolic=None     # always in the global coordinate system
        self.type_=type_
        self.label=label
        self.__getSymbolic()
        
    def __getSymbolic(self): 
        # avoid math operations up to the last second. The returned value is with respect to the global system
        # should consider polar csyses as well (for now only cartesian systems are suported)
        if self.parent==None: # this is with respect to the global
            self.symbolic="%s, %s" % (str(self.origin[0]), str(self.origin[1]))
        else:    
            self.symbolic="%s, %s" % (str(self.origin[0])+'+'+str(self.parent.origin[0]), str(self.origin[1])+'+'+str(self.parent.origin[1]))		
        
class point():
    """2D point data structure:

Parameters: 
    * label: it is the structure associated name
    * parent: the parent point (if the point is obtained through a geometrical transformation)
    * transformation: the geometrical transformation object (if the point was obtained through one - not implemented)
    * coords: the coordinates of the point with respect to the coordinate system
    * csys: the coordinate system in which xy values are defined (if csys == None then it is considerate to be global)
    """	
    def __init__(self, coords, parent=None, csys=None, transformation=None, label=None):
        self.coords=coords
        self.parent=parent		
        self.csys=csys
        self.transformation=transformation
        self.label=label	
        self.symbolic=None
        self.__getSymbolic()
        
    def __getSymbolic(self):
        if self.csys==None: # assume global coordinate system
            self.symbolic="%s, %s" % (str(self.coords[0]), str(self.coords[1]))
        else:    
            self.symbolic="%s, %s" % (str(self.coords[0])+'+'+str(self.csys.origin[0]), str(self.coords[1])+'+'+str(self.csys.origin[1]))		
    
class segment():
    """2D segment data structure:

Parameters: 
    * label: it is the structure associated name
    * parent: the parent line (if the line is obtained through a geometrical transformation)
    * transformation: the geometrical transformation object (if the segment was obtained through one - not implemented)
    * coords: the coordinates of the point with respect to the coordinate system
    * point1 & point2: the points defining the line in the 2D plane
    """	
    def __init__(self, coords, parent=None, transformation=None, label=None, point1=None, point2=None):
        self.coords=coords
        self.parent=parent		
        self.transformation=transformation
        self.label=label	
        self.symbolic=None
        self.__getSymbolic()
        
    def __getSymbolic(self):
        return "should be something based on the two points and the equation passing through 2 points - not implemented yet!" 

    def __len__(self):
        return "not implemented yet!"		

class arc():
    pass
    
class surface():
    pass		

class transformation():
    pass	
