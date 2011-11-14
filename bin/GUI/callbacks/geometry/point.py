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
from ...cad import fkernel, ikernel

def new(app):
    x=point.point(app)
    data=x() # a bunch of Tkinter.StringVars
    # register newly created point to DrawingArea
    # at least label, float and int information so far:
    floatRepr=fkernel.point(label=data[0].get(), csys=data[3].get(), coords=[float(data[1].get()), float(data[2].get())])
    intRepr=ikernel.float2ints(self.floatRepr.coords, app.DrawingArea)
    app.DrawingArea.points[floatRepr.label]={"floatRepr":floatRepr, "intRepr":intRepr}	# to add color/shape representation later

def edit(app):
    print "Edit Point: Not implemented yet!"

def delete(app):
    print "Delete Point: Not implemented yet!"

def lists(app):
    print "List Points: Not implemented yet!"
