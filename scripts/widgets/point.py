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

import tkinter, tkinter.tix

class point(tkinter.tix.Toplevel):
    def __init__(self, master, point=None):	
        tkinter.tix.Toplevel.__init__(self, master)
        self.master=master
        self.point=point	
        
        self.plabel = tkinter.StringVar()        
        self.csys   = tkinter.StringVar()
        self.xcoord = tkinter.StringVar()
        self.ycoord = tkinter.StringVar()
        self.color  = tkinter.StringVar() #??? [r, g, b] or "r g b"
        self.representation = tkinter.StringVar()  
        
        self.visible=tkinter.IntVar()
        self.filled=tkinter.IntVar()
 
        if self.point != None:  # so this is edit point command
            self.xcoord.set(str(self.point.xcoord[0]))
            self.ycoord.set(str(self.point.ycoord[1]))
            self.csys.set(self.point.csys)
            self.plabel.set(self.point.plabel)
            self.color.set(self.point.color)
            self.representation.set(self.point.representation)
            self.title("Edit Point")
        else:
            self.xcoord.set("")
            self.ycoord.set("")
            self.csys.set("")
            self.plabel.set("")			
            self.color.set("white") # to be read from the XML settings file (associated with the model)
            self.representation.set("square") # to be read from the XML settings file (associated with the model)
            self.title("Add Point")			

        self.resizable(height="false", width="false")

        self.firstCoord=tkinter.StringVar()
        self.secondCoord=tkinter.StringVar()
        
        self.firstCoord.set("X coordinate")
        self.secondCoord.set("Y coordinate")

        # create widgets here (but don't display them)
        self.pointLabel=tkinter.Label(self, text="Point Label", anchor=tkinter.W)
        self.pointEntry=tkinter.Entry(self, textvariable=self.plabel)

        self.csysLabel=tkinter.Label(self, text="Coordinate System")            
        self.csysCombo=tkinter.tix.ComboBox(self, label=None, dropdown=1, editable=0, height=4, variable=self.csys)
        self.csysCombo.set_silent('global') #??? if edit???

        for i in list(self.master.DrawingArea.csys.keys()):
            self.csysCombo.insert(tkinter.tix.END, i)  

        self.coord1Label=tkinter.Label(self, textvariable=self.firstCoord, anchor=tkinter.W)    
        self.coord1Entry=tkinter.Entry(self, textvariable=self.xcoord)

        self.colorLabel=tkinter.Label(self, text="Color", anchor=tkinter.W)
        self.colorCombo=tkinter.tix.ComboBox(self, label=None, dropdown=1, editable=0, command=None, height=3, variable=self.color)  
        self.colorCombo.set_silent('default')
 
        self.colorCombo.insert(tkinter.tix.END, 'yellow')
        self.colorCombo.insert(tkinter.tix.END, 'red')        

        self.coord2Label=tkinter.Label(self, textvariable=self.secondCoord, anchor=tkinter.W)    
        self.coord2Entry=tkinter.Entry(self, textvariable=self.ycoord)        
        
        self.represLabel=tkinter.Label(self, text="Representation", anchor=tkinter.W)
        self.represCombo=tkinter.tix.ComboBox(self, label=None, dropdown=1, editable=0, command=None, height=3, variable=self.representation) 
        self.represCombo.set_silent('square')
        
        self.represCombo.insert(tkinter.tix.END, 'circle')
        self.represCombo.insert(tkinter.tix.END, 'triangle') # diamond, stars, other shapes?

        self.ckButton=tkinter.Checkbutton(self, anchor=tkinter.W, indicatoron=1, offvalue=0, onvalue=1, text="Visible", variable=self.visible)
        self.ckButton.select()

        self.fillButton=tkinter.Checkbutton(self, anchor=tkinter.W, indicatoron=1, offvalue=0, onvalue=1, text="Filled", variable=self.filled)
        self.fillButton.select()
        
        self.okButton=tkinter.Button(self, text="Ok", command=self.__cbOk, width=6)
        self.cancelButton=tkinter.Button(self, text="Cancel", command=self.__cbCancel, width=6)  
        
        self.showWidgets()
   
    def showWidgets(self):
        # upper row		

        self.pointLabel.grid(row=0, column=0, padx=(10, 5), pady=(12, 0), sticky=tkinter.W+tkinter.E)
        self.pointEntry.grid(row=0, column=1, columnspan=2, pady=(12, 0), padx=(0, 5))
        
        self.csysLabel.grid(row=0, column=3, pady=(12, 0), sticky=tkinter.W)
        self.csysCombo.grid(row=0, column=4, padx=(0, 10), pady=(12, 0), columnspan=2)
        
        # next row
        self.coord1Label.grid(row=1, column=0, sticky=tkinter.W+tkinter.E, padx=(10, 0))
        self.coord1Entry.grid(row=1, column=1, columnspan=2, padx=(0, 5))
        
        self.colorLabel.grid(row=1, column=3, sticky=tkinter.W)
        self.colorCombo.grid(row=1, column=4, columnspan=2, padx=(0, 10))
        
        # next row

        self.coord2Label.grid(row=2, column=0, sticky=tkinter.W+tkinter.E, padx=(10, 0))  
        self.coord2Entry.grid(row=2, column=1, columnspan=2, padx=(0, 5))
        
        self.represLabel.grid(row=2, column=3, sticky=tkinter.W+tkinter.E)
        self.represCombo.grid(row=2, column=4, padx=(0, 10), sticky=tkinter.W+tkinter.E, columnspan=2)
          
        # next row
        
        self.ckButton.grid(row=3, column=0, sticky=tkinter.W, padx=(10, 0))
        self.fillButton.grid(row=3, column=1, sticky=tkinter.W, padx=(0, 0))
  
        self.okButton.grid(row=3, column=4, sticky=tkinter.E, padx=(0, 5), pady=(10, 12))
        self.cancelButton.grid(row=3, column=5, sticky=tkinter.W, pady=(10, 12), padx=(5, 10))     
        self.mainloop()   
        
    def __call__(self):  # label, x, y, csys, color [r, g, b], representation, visible
        return [self.plabel.get(), self.xcoord.get(), self.ycoord.get(), self.csys.get(), self.color.get(), self.representation.get(), self.visible.get(), self.filled.get()] 
        
    def __cbOk(self):
        if self.plabel.get() == "" or self.xcoord.get() == "" or self.ycoord.get() == "": 
            if self.plabel.get() == "":
                self.pointEntry["bg"]="red"
            else:
                self.pointEntry["bg"]="white"    
            if self.xcoord.get() == "":
                self.coord1Entry["bg"]="red"
            else:
                self.coord1Entry["bg"]="white"    
            if self.ycoord.get() == "":
                self.coord2Entry["bg"]="red" 
            else:
                self.coord2Entry["bg"]="white"     
        else:
            tester=0 # dummy var - 0 means Ok, 1 means it is not ok
            try: # test x coordinate
                x=float(self.xcoord.get())
            except ValueError: 
                self.coord1Entry["bg"]="red"
                tester=1
            else:    
                self.coord1Entry["bg"]="white"  
                                 
            try: # test y coordinate
                y=float(self.ycoord.get())
            except ValueError: 
                tester=1
                self.coord2Entry["bg"]="red"  
            else:    
                self.coord2Entry["bg"]="white" 
                
            if tester == 0:    
                self.quit()
                self.destroy()
        
    def __cbCancel(self):
        self.xcoord.set("")
        self.ycoord.set("")
        self.csys.set("")
        self.plabel.set("")		    		    
        self.quit()
        self.destroy()

    def __setPolar(self, event=0):
        if self.master.DrawingArea.csys[self.csys.get()]["floatinfo"].type_=="polar":
            self.firstCoord.set("Polar axis")    
            self.secondCoord.set("Polar angle")             
        
        if self.master.DrawingArea.csys[self.csys.get()]["floatinfo"].type_=="cartesian":
            self.firstCoord.set("X coordinate")    
            self.secondCoord.set("Y coordinate")
            
        self.update_idletasks() 
