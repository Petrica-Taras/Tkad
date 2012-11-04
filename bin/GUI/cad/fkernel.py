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
        self.type_=type_
        self.label=label

        self.metadata={}
        # metadata: color, layer, visibility, integer coordinates on canvas, associated xml id/name/label?

    def isglobal(self):
        return self.label == "global"



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

        self.metadata={}

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

        self.metadata={}

    def __len__(self):
        return "not implemented yet!"

class arc():
    pass

class surface():
    pass	

class transformation():
    pass	
