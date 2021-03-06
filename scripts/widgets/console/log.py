# Copyright (C) 2012 Petrica Taras
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

from wx import TextCtrl, TE_MULTILINE, TextAttr

class consoleLog(TextCtrl):
    def __init__(self, master):
        TextCtrl.__init__(self, master, style = TE_MULTILINE)
        self.master = master
        self.SetBackgroundColour("Black")          # TODO: move into settings object
        self.SetDefaultStyle(TextAttr("GREEN"))    # TODO: move into settings object

        self.write("Tkad started!\n\n")
        
    def write(self, string):    
        self.AppendText(string)
        
