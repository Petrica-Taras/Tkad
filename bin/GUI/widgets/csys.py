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

import Tkinter

class csys(Tkinter.Toplevel):
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
        Tkinter.Toplevel.__init__(self, master)
        self.master=master
        self.csys=csys	
        self.clabel=Tkinter.StringVar()
        self.parent=Tkinter.StringVar()
        self.originX=Tkinter.StringVar()
        self.originY=Tkinter.StringVar()
        self.rotation=Tkinter.StringVar()
        self.typec=Tkinter.StringVar()
        
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
        self.csysLabel.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky=Tkinter.W,)
        self.csysEntry.grid(row=0, column=1, columnspan=2, padx=(0, 10), pady=(10, 0))
        # next rox
        self.origXLabel=Tkinter.Label(self, text="X origin")            
        self.origXEntry=Tkinter.Entry(self, textvariable=self.originX)  
        self.origXLabel.grid(row=1, column=0, sticky=Tkinter.W, padx=(10, 0))  
        self.origXEntry.grid(row=1, column=1, columnspan=2, padx=(0, 10))
        # next row
        self.origYLabel=Tkinter.Label(self, text="Y origin")            
        self.origYEntry=Tkinter.Entry(self, textvariable=self.originY)  
        self.origYLabel.grid(row=2, column=0, sticky=Tkinter.W, padx=(10, 0))  
        self.origYEntry.grid(row=2, column=1, columnspan=2, padx=(0, 10)) 
        # next row
        self.typeLabel=Tkinter.Label(self, text="Coordinate System Type ")    
        self.typeEntry=Tkinter.Entry(self, textvariable=self.typec)
        self.typeLabel.grid(row=3, column=0, sticky=Tkinter.W, padx=(10, 0))
        self.typeEntry.grid(row=3, column=1, columnspan=2, padx=(0, 10))  
        # next row
        self.okButton=Tkinter.Button(self, text="Ok", command=self.__cbOk, width=6)
        self.cancelButton=Tkinter.Button(self, text="Cancel", command=self.__cbCancel, width=6)   
        self.okButton.grid(row=4, column=1, sticky=Tkinter.W+Tkinter.E, pady=(6, 12))
        self.cancelButton.grid(row=4, column=2, sticky=Tkinter.W+Tkinter.E, pady=(6, 12), padx=(0, 10))     
        self.mainloop() 
        
    def __call__(self):
        return [self.clabel, self.originX, self.originY, self.typec]    

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
