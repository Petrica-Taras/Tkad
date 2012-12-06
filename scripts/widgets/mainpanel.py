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

from wx import Panel, GridBagSizer, Notebook, EXPAND, ALL

class mainPanel(Panel):
    """A custom container, grouping all the widgets."""
    def __init__(self, master, size = (4, 4)):
        Panel.__init__(self, master)

        self.master = master
        self.sizer = GridBagSizer(*size)
        self.widgets = {} # holds the widgets as values. The keys are tuples with
                          # three members (row, col, colspan)
        self.sizer.AddGrowableCol(1)
        self.sizer.AddGrowableRow(1)
        
        self.SetSizerAndFit(self.sizer)
        
    def addtoPanel(self, widget, position):
        if (position == (1, 1, 1) or position == (2, 0, 2)) and position in self.widgets.keys():
            self.__addNotebook(position, widget)
        else:
            self.sizer.Add(widget, pos = (position[0], position[1]), span = (1, position[2]), flag = EXPAND|ALL)
            self.widgets[position] = widget 

    def __addNotebook(self, position, widget):
        """This function creates a notebook widget and replaces the self.widgets[position] with
        the notebook. If the notebook already exists then it is not replaced."""
        if isinstance(self.widgets[position], Notebook):
            self.widgets[position].AddPage(widget, widget.title)
        else:
            ntbk = Notebook(self, -1)
            ntbk.AddPage(self.widgets[position], self.widgets[position].title)
            ntbk.AddPage(widget, widget.title)
            self.widgets[position] = ntbk

if __name__ == "__main__": # test - to be deleted after adding callbacks!
    import wx
    class cw(wx.Button):
        def __init__(self, parent):
            wx.Button.__init__(self, parent, size=(400, 100), label="Ok")
            self.title = 'Button Title'
            
    app = wx.App(False)
    x = wx.Frame(None)
    m = mainPanel(x)
    b1 = cw(x)
    b2 = cw(x)
    b3 = cw(x)
    b4 = cw(x)
    b5 = cw(x)
    
    m.addtoPanel(b1, (0, 0, 1))
    m.addtoPanel(b2, (0, 1, 1))
    m.addtoPanel(b3, (1, 0, 1))
    m.addtoPanel(b4, (1, 1, 1))
    m.addtoPanel(b5, (2, 0, 2))
    
    x.SetSize((800, 600))
    x.SetTitle('Test icons and shortcuts')
    x.Centre()
    x.Show(True)    
    app.MainLoop()                
