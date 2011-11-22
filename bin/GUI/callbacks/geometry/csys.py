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

from ...widgets import csys, point
from ...cad import fkernel

def new(app):
    x=csys.csys(app)
    data=x() # label, x, y, rotation, type, parent, visible
    # now register data within the canvas
    app.DrawingArea.csys[data[0]]={"floatinfo":fkernel.csys(parent=app.DrawingArea.csys[data[5]]["floatinfo"], origin=[float(data[1]), float(data[2])], rotation=float(data[3]), label=data[0], type_=data[4]), "intPosition":app.DrawingArea.float2int([float(data[1]), float(data[2])]), "graphRepr":{}}
    # add exceptions to deal with empty or non number fields.
    # add code to register if the csys should be visible or not

def edit(app):
    print "Edit Coordinate System: Not implemented yet!"
   
def delete(app):
    print "Delete Coordinate System: Not implemented yet!"

def lists(app):        
    print "Lists Coordinate Systems: Not implemented yet!"
