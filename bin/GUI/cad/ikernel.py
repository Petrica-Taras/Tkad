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

# same as fkernel but for integer numbers
# should fkernel and ikernel be associated with canvas like so:
# GUI.widgets.canvas.fkernel.pointDict
# GUI.widgets.canvas.ikernel.pointDict
# or canvas can inherit the fkernel and ikernel classes
# right now is:
# GUI.cad.fkernel.someop

# there is only one csys (placed at x=0, y=0) while the global sys is placed in the middle of the canvas (for a new canvas)

origin=[]

def setOrigin(DrawingArea):
    """Calculates the location on canvas of the global coordinate system. Returns the location"""
    location = [0, 0]
    pass


def float2ints(floats, DrawingArea):
    """Transforms float coordinates into canvas coordinates.

Parameters:
    * floats - a fkernel point class
    * DrawingArea.zoomedFactor - keeps tracks of the zoom actions for the DrawingArea so that the new points can be positioned correctly
    * DrawingArea.translatedFactor - keeps tracks of the translating actions for the DrawingArea so that the new points can be positioned correctly    
    * DrawingArea.scale_f2i - a tuple of type (unit, pixels)"""
    # not finished since it does not consider translation and zoom (will be added after the coordinate system is implemented)
    return [int(floats[0]*DrawingArea.scale_f2i[1]/DrawingArea.scale_f2i[0]), int(floats[1]*DrawingArea.scale_f2i[1]/DrawingArea.scale_f2i[0])]	
