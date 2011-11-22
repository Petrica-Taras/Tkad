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

import Tkinter, Tix # Tix is for the combobox

class csys(Tix.Toplevel):
    """GUI.widgets.csys.csys class(rootApp, csys=None)\n\n \

Tkinter.Toplevel like widget to collect information for either constructing a \
new coordinate system or editing an existing one (case csys !=None).\n\n \
\
Parameters:\n\n \
\
Input: \n\n \
csys - the coordinate system to be edited.\n\n \
\
Output: \n\n \
..."""
    def __init__(self, master, csys=None):	
        Tix.Toplevel.__init__(self, master)
        self.master=master
        self.csys=csys	
        self.clabel=Tkinter.StringVar()
        self.parent=Tkinter.StringVar()
        self.originX=Tkinter.StringVar()
        self.originY=Tkinter.StringVar()
        self.rotation=Tkinter.StringVar()
        self.typec=Tkinter.StringVar()
        
        self.visible=Tkinter.IntVar()
        
        if self.csys != None: # editing a csys entity
            self.originX.set(str(self.csys.origin[0]))
            self.originY.set(str(self.csys.origin[1]))
            self.parent.set(self.csys.parent.label)
            self.clabel.set(self.csys.label)
            self.rotation.set(str(self.csys.rotation))
            self.typec.set(self.csys.type)
            self.title("Edit Coordinate System")
        else:
            self.originX.set("")
            self.originY.set("")
            self.parent.set("")
            self.clabel.set("")
            self.rotation.set("")
            self.typec.set("")
            self.title("Add Coordinate System")

        self.resizable(height="false", width="false")
        self.addWidgets()

    def addWidgets(self):
        # upper row		
        self.csysLabel=Tkinter.Label(self, text="Coordinate System Label")
        self.csysEntry=Tkinter.Entry(self, textvariable=self.clabel)
        self.csysLabel.grid(row=0, column=0, padx=(10, 0), pady=(12, 0), sticky=Tkinter.W)
        self.csysEntry.grid(row=0, column=1, columnspan=2, pady=(12, 0), padx=(0, 5))
        
        self.parentLabel=Tkinter.Label(self, text="Coordinate System Parent")
        self.parentCombo=Tix.ComboBox(self, label=None, dropdown=1, editable=0, height=4, variable=self.parent)
        self.parentLabel.grid(row=0, column=3, pady=(12, 0), sticky=Tkinter.W)
        self.parentCombo.grid(row=0, column=4, padx=(0, 10), pady=(12, 0), columnspan=2)
        
        self.parentCombo.set_silent('global')
        
        for i in self.master.DrawingArea.csys.keys():
            self.parentCombo.insert(Tix.END, i)
        
        # next row
        self.origXLabel=Tkinter.Label(self, text="X origin")            
        self.origXEntry=Tkinter.Entry(self, textvariable=self.originX)  
        self.origXLabel.grid(row=1, column=0, sticky=Tkinter.W, padx=(10, 0))  
        self.origXEntry.grid(row=1, column=1, columnspan=2, padx=(0, 5))
        
        self.typeLabel=Tkinter.Label(self, text="Coordinate System Type ")    
        self.typeCombo=Tix.ComboBox(self, label=None, dropdown=1, editable=0, height=3, variable=self.typec)
        self.typeLabel.grid(row=1, column=3, sticky=Tkinter.W)
        self.typeCombo.grid(row=1, column=4, columnspan=2, padx=(0, 10))  

        self.typeCombo.set_silent('cartesian')
        
        self.typeCombo.insert(Tix.END, 'cartesian')
        self.typeCombo.insert(Tix.END, 'polar')

        # next row
        self.origYLabel=Tkinter.Label(self, text="Y origin")            
        self.origYEntry=Tkinter.Entry(self, textvariable=self.originY)  
        self.origYLabel.grid(row=2, column=0, sticky=Tkinter.W, padx=(10, 0))  
        self.origYEntry.grid(row=2, column=1, columnspan=2, padx=(0, 5)) 
        
        self.rotLabel=Tkinter.Label(self, text="Rotation") 
        self.rotEntry=Tkinter.Entry(self, textvariable=self.rotation) 
        self.rotLabel.grid(row=2, column=3, sticky=Tkinter.W)
        self.rotEntry.grid(row=2, column=4, padx=(5, 10), sticky=Tkinter.W+Tkinter.E, columnspan=2)
        
        # next row

        self.ckButton=Tkinter.Checkbutton(self, anchor=Tkinter.W, indicatoron=1, offvalue=0, onvalue=1, text="Visible", variable=self.visible)
        self.ckButton.grid(row=3, column=0, sticky=Tkinter.W, padx=(10, 0))
        self.ckButton.select()

        self.okButton=Tkinter.Button(self, text="Ok", command=self.__cbOk, width=6)
        self.cancelButton=Tkinter.Button(self, text="Cancel", command=self.__cbCancel, width=6)   
        self.okButton.grid(row=3, column=4, sticky=Tkinter.E, padx=(0, 5), pady=(10, 12))
        self.cancelButton.grid(row=3, column=5, sticky=Tkinter.W, pady=(10, 12), padx=(5, 10))     
        self.mainloop() 
        
    def __call__(self):
        return [self.clabel.get(), self.originX.get(), self.originY.get(), self.rotation.get(), self.typec.get(), self.parent.get(), self.visible.get()]    

    def __cbOk(self):
        self.update_idletasks()		
        self.quit()
        self.destroy()
        
    def __cbCancel(self):
        self.originX.set("")
        self.originY.set("")
        self.clabel.set("")
        self.typec.set("")		    		    
        self.quit()
        self.destroy()        
