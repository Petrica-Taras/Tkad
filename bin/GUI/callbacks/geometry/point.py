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
    x=point.point(app)
    data=x() # label, x, y, csys, color [r, g, b], representation, visible, filled
    
    # register point and associated data to DrawingArea
    app.DrawingArea.points[data[0]]={"floatinfo":fkernel.point(parent=None, transformation=None, coords=[float(data[1]), float(data[2])], csys=app.DrawingArea.csys[data[3]]["floatinfo"], label=data[0]),
                                     "intPosition":app.DrawingArea.float2int(app.DrawingArea.csys[data[3]]["intPosition"], 
                                                                             [float(data[1]), float(data[2])], type_=app.DrawingArea.csys[data[3]]["floatinfo"].type_),
                                     "graphRepr":{"visible":int(data[6])}} # data[6] is already an int?
                                
    app.DrawingArea.points[data[0]]["graphRepr"]["entities"]=app.DrawingArea.dispPoint(app.DrawingArea.float2int(app.DrawingArea.csys[data[3]]["intPosition"], [float(data[1]), float(data[2])], type_=app.DrawingArea.csys[data[3]]["floatinfo"].type_), data[5], data[4], visible=data[6], filled=int(data[7]))

    # associate proper tags 
    app.DrawingArea.points[data[0]]["graphRepr"]["tags"]=[data[0], "point", "translate"]

    # add code somewhere to check if the point name (label) is already taken
    # add code to work in milimeters 
    
    # register the point in the XML tree
    l_point=app.xmlprojfiles["geometry"][0].createElement("Point")
    l_point.setAttribute('id', data[0])
    l_point.setAttribute('csys', data[3])
    l_point.setAttribute('color', data[4])
    l_point.setAttribute('representation', data[5])
    l_point.setAttribute('visible', data[6])
    l_point.setAttribute('filled', data[7])
    l_point.appendChild(app.xmlprojfiles["geometry"][0].createTextNode("%s %s" % (data[1], data[2])))    

def edit(app):
    print "Edit Point: Not implemented yet!"

def delete(app):
    print "Delete Point: Not implemented yet!"

def lists(app):
    print "List Points: Not implemented yet!"
