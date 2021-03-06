# Copyright (C) 2011 - 2012 Petrica Taras
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

from wx import TextCtrl, TE_MULTILINE

class XMLEditor(TextCtrl):
    """Widget for XML editor with suport for syntax highlighting, right click pop menu, find/replace, etc."""
    def __init__(self, master, resources): # resources - XML file
        TextCtrl.__init__(self, master, style = TE_MULTILINE)
        self.master = master
        
        self.__XMLfile = resources
        
