import Tkinter

class point(Tkinter.Toplevel):
    # to add exceptions so that no non-values can be passed by entries	
    def __init__(self, master, point=None):	
        Tkinter.Toplevel.__init__(self, master)
        self.master=master
        self.point=point	
        self.csys, self.xcoord, self.ycoord=Tkinter.StringVar(), Tkinter.StringVar(), Tkinter.StringVar()
        self.plabel=Tkinter.StringVar()
 
        if self.point != None:  # so this is edit point command
            self.xcoord.set(str(self.point.coords[0]))
            self.ycoord.set(str(self.point.coords[1]))
            self.csys.set(self.point.csys.label)
            self.plabel.set(self.point.label)
            self.title("Edit Point")
        else:
            self.xcoord.set("")
            self.ycoord.set("")
            self.csys.set("")
            self.plabel.set("")			
            self.title("Add Point")			

        self.resizable(height="false", width="false")

        self.addWidgets()
   
    def addWidgets(self):
        # upper row		
        self.pointLabel=Tkinter.Label(self, text="Point Label")
        self.pointEntry=Tkinter.Entry(self, textvariable=self.plabel)
        self.pointLabel.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky=Tkinter.W,)
        self.pointEntry.grid(row=0, column=1, columnspan=2, padx=(0, 10), pady=(10, 0))
        # next rox
        self.csysLabel=Tkinter.Label(self, text="Coordinate System")            
        self.csysEntry=Tkinter.Entry(self, textvariable=self.csys)  
        self.csysLabel.grid(row=1, column=0, padx=(10, 0))  
        self.csysEntry.grid(row=1, column=1, columnspan=2, padx=(0, 10))
        # next row
        self.coord1Label=Tkinter.Label(self, text="x = ")    
        self.coord1Entry=Tkinter.Entry(self, textvariable=self.xcoord)
        self.coord1Label.grid(row=2, column=0, sticky=Tkinter.W, padx=(10, 0))
        self.coord1Entry.grid(row=2, column=1, columnspan=2, padx=(0, 10))    
        # next row
        self.coord2Label=Tkinter.Label(self, text="y = ")    
        self.coord2Entry=Tkinter.Entry(self, textvariable=self.ycoord)
        self.coord2Label.grid(row=3, column=0, sticky=Tkinter.W, padx=(10, 0))
        self.coord2Entry.grid(row=3, column=1, columnspan=2, padx=(0, 10))  
        # next row
        self.okButton=Tkinter.Button(self, text="Ok", command=self.__cbOk, width=6)
        self.cancelButton=Tkinter.Button(self, text="Cancel", command=self.__cbCancel, width=6)   
        self.okButton.grid(row=4, column=1, sticky=Tkinter.W+Tkinter.E, pady=(6, 12))
        self.cancelButton.grid(row=4, column=2, sticky=Tkinter.W+Tkinter.E, pady=(6, 12), padx=(0, 10))     
        self.mainloop()    
        
    def __call__(self):  
        return [self.plabel, self.xcoord, self.ycoord, self.csys] 
        
    def __cbOk(self):
        self.update_idletasks()		
        self.quit()
        self.destroy()
        
    def __cbCancel(self):
        self.xcoord.set("")
        self.ycoord.set("")
        self.csys.set("")
        self.plabel.set("")		    		    
        self.quit()
        self.destroy()
