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

import tkinter, tkinter.tix # Tix is for the combobox

class csys(tkinter.tix.Toplevel):
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
        tkinter.tix.Toplevel.__init__(self, master)
        self.master=master
        self.csys=csys
        self.clabel=tkinter.StringVar()
        self.parent=tkinter.StringVar()
        self.originX=tkinter.StringVar()
        self.originY=tkinter.StringVar()
        self.rotation=tkinter.StringVar()
        self.typec=tkinter.StringVar()

        self.visible=tkinter.IntVar()

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
            self.rotation.set("0")
            self.typec.set("")
            self.title("Add Coordinate System")

        self.resizable(height="false", width="false")

        self.firstCoord=tkinter.StringVar()
        self.secondCoord=tkinter.StringVar()

        self.firstCoord.set("X origin")
        self.secondCoord.set("Y origin")

        # create widgets here (but don't display them)

        self.csysLabel=tkinter.Label(self, text="Coordinate System Label", anchor=tkinter.W)

        self.csysEntry=tkinter.Entry(self, textvariable=self.clabel)

        self.parentLabel=tkinter.Label(self, text="Coordinate System Parent")
        self.parentCombo=tkinter.tix.ComboBox(self, label=None, dropdown=1, editable=0, height=4, variable=self.parent)

        self.parentCombo.set_silent('global')

        for i in list(self.master.DrawingArea.csys.keys()):
            self.parentCombo.insert(tkinter.tix.END, i)

        self.origXLabel=tkinter.Label(self, textvariable=self.firstCoord, anchor=tkinter.W)
        self.origXEntry=tkinter.Entry(self, textvariable=self.originX)

        self.typeLabel=tkinter.Label(self, text="Coordinate System Type ", anchor=tkinter.W)
        self.typeCombo=tkinter.tix.ComboBox(self, label=None, dropdown=1, editable=0, command=self.__setPolar, height=3, variable=self.typec)

        self.typeCombo.set_silent('cartesian')

        self.typeCombo.insert(tkinter.tix.END, 'cartesian')
        self.typeCombo.insert(tkinter.tix.END, 'polar')

        self.origYLabel=tkinter.Label(self, textvariable=self.secondCoord, anchor=tkinter.W)
        self.origYEntry=tkinter.Entry(self, textvariable=self.originY)

        self.rotLabel=tkinter.Label(self, text="Rotation", anchor=tkinter.W)
        self.rotEntry=tkinter.Entry(self, textvariable=self.rotation)

        self.ckButton=tkinter.Checkbutton(self, anchor=tkinter.W, indicatoron=1, offvalue=0, onvalue=1, text="Visible", variable=self.visible)
        self.ckButton.select()

        self.okButton=tkinter.Button(self, text="Ok", command=self.__cbOk, width=6)
        self.cancelButton=tkinter.Button(self, text="Cancel", command=self.__cbCancel, width=6)

        self.showWidgets()

    def showWidgets(self):

        # upper row

        self.csysLabel.grid(row=0, column=0, padx=(10, 5), pady=(12, 0), sticky=tkinter.W+tkinter.E)
        self.csysEntry.grid(row=0, column=1, columnspan=2, pady=(12, 0), padx=(0, 5))

        self.parentLabel.grid(row=0, column=3, pady=(12, 0), sticky=tkinter.W)
        self.parentCombo.grid(row=0, column=4, padx=(0, 10), pady=(12, 0), columnspan=2)

        # next row

        self.origXLabel.grid(row=1, column=0, sticky=tkinter.W+tkinter.E, padx=(10, 0))
        self.origXEntry.grid(row=1, column=1, columnspan=2, padx=(0, 5))

        self.typeLabel.grid(row=1, column=3, sticky=tkinter.W)
        self.typeCombo.grid(row=1, column=4, columnspan=2, padx=(0, 10))

        # next row

        self.origYLabel.grid(row=2, column=0, sticky=tkinter.W+tkinter.E, padx=(10, 0))
        self.origYEntry.grid(row=2, column=1, columnspan=2, padx=(0, 5))

        self.rotLabel.grid(row=2, column=3, sticky=tkinter.W+tkinter.E)
        self.rotEntry.grid(row=2, column=4, padx=(5, 10), sticky=tkinter.W+tkinter.E, columnspan=2)

        # next row

        self.ckButton.grid(row=3, column=0, sticky=tkinter.W, padx=(10, 0))

        self.okButton.grid(row=3, column=4, sticky=tkinter.E, padx=(0, 5), pady=(10, 12))
        self.cancelButton.grid(row=3, column=5, sticky=tkinter.W, pady=(10, 12), padx=(5, 10))
        self.mainloop()

    def __call__(self):
        return [self.clabel.get(), self.originX.get(), self.originY.get(), self.rotation.get(), self.typec.get(), self.parent.get(), self.visible.get()]

    def __cbOk(self):
        if self.clabel.get() == "" or self.originX.get() == "" or self.originY.get() == "" or self.rotation.get() == "":
            if self.clabel.get() == "":
                self.csysEntry["bg"]="red"
            else:
                self.csysEntry["bg"]="white"
            if self.originX.get() == "":
                self.origXEntry["bg"]="red"
            else:
                self.origXEntry["bg"]="white"
            if self.originY.get() == "":
                self.origYEntry["bg"]="red"
            else:
                self.origYEntry["bg"]="white"
            if self.rotation.get() == "":
                self.rotEntry["bg"]="red"
            else:
                self.rotEntry["bg"]="white"
        else:
            tester=0 # dummy var - 0 means Ok, 1 means it is not ok
            try: # test x coordinate
                x=float(self.originX.get())
            except ValueError:
                self.origXEntry["bg"]="red"
                tester=1
            else:
                self.origXEntry["bg"]="white"

            try: # test y coordinate
                y=float(self.originY.get())
            except ValueError:
                tester=1
                self.origYEntry["bg"]="red"
            else:
                self.origYEntry["bg"]="white"

            try: # test rotation parameter
                r=float(self.rotation.get())
            except ValueError:
                self.rotEntry["bg"]="red"
                tester=1
            else:
                self.rotEntry["bg"]="white"

            if tester == 0:
                self.quit()
                self.destroy()

    def __cbCancel(self):
        self.originX.set("")
        self.originY.set("")
        self.clabel.set("")
        self.typec.set("")
        self.quit()
        self.destroy()

    def __setPolar(self, event=0):
        if self.typec.get()=="polar":
            self.firstCoord.set("Polar axis")
            self.secondCoord.set("Polar angle")
            self.typeCombo.set_silent('polar')

        if self.typec.get()=="cartesian":
            self.firstCoord.set("X origin")
            self.secondCoord.set("Y origin")
            self.typeCombo.set_silent('cartesian')

        self.update_idletasks()
