# first thing called by the main executable (sfem.py)
# does some initialisations based on the xml files
# starts the GUI

from xml.dom import minidom
import os, Tkinter
import GUI.widgets.menu, GUI.widgets.uptoolbox, GUI.widgets.canvas

# generate application window

class Application(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)	
        self.basedir=(os.getcwd()).replace("bin", "")
        self.lwd=None # last working directory
        self.xmlPaths=None
        self.modulePaths=[] # other directories to import modules from
        
        self.xmlprojfiles={"trunk":None, "geometry":None, "mesh":None, }
        
        self.menuBar=None

        self.upperFrame=None # general buttons like zoom, new, save, entity hierarchy, open editor (xml, python),                         
        
        self.middleFrame=None # left toolbox + cad widget
        self.canvasFrame=[] # with tabs possibility - must be 
        self.leftFrame=None
        self.DrawingArea=None
        
        self.lowerConsole=None # with tabs possibility
        self.lowerLabelFrame=None # has priority when determining the windows size
        self.lowerLabel=None
        self.lowerlabelstr=[]
        
        self.AppTitle=Tkinter.StringVar()
        self.AppTitle.set("")

        self.readXML()
        self.createApp()       
        
    def createApp(self):
        self.menuBar=GUI.widgets.menu.MenuToolbar(self, os.path.join(self.basedir, "etc/gui/menus.xml"))   
        
        self.upperFrame=GUI.widgets.uptoolbox.UpperToolbox(self, os.path.join(self.basedir, "etc/gui/uppertoolbox.xml")) 
        self.upperFrame.pack(side="top", anchor="nw")        
        
        self.middleFrame=Tkinter.Frame(self)
        self.middleFrame.pack(side="top", fill="both", expand="yes")
        self.canvasFrame.append(Tkinter.Frame(self.middleFrame))
        self.canvasFrame[0].pack(side="right", fill="both", expand="yes")
        
        # more like testing purpose
        self.lowerLabelFrame=Tkinter.Frame(self)
        self.lowerLabelFrame.pack(side="top", fill="x")
        self.lowerlabelstr.append(Tkinter.StringVar())
        self.lowerLabel=Tkinter.Label(self.lowerLabelFrame, textvariable=self.lowerlabelstr[0], relief="sunken")
        self.lowerLabel.pack(side="bottom", fill="x")
        
        # bindings
    
        self.geometry('%sx%s+0+0' % self.maxsize())
        
        self.title(self.AppTitle.get())
        self.update_idletasks()
        self.mainloop()

    def initDrawingArea(self): # a parameter fo openProject (like the project xml trunk of the project to be opened)
        self.DrawingArea=GUI.widgets.canvas.DrawingArea(self, os.path.join(self.basedir, "etc/gui/canvas.xml")) 
        self.DrawingArea.pack(fill="both", expand="yes", in_=self.canvasFrame[0],)		

        self.DrawingArea.bind("<Motion>", self.__cb_lowerlabel) 
               
    def readXML(self):
        self.xmlPaths=minidom.parse(os.path.join(self.basedir, "etc/paths.xml"))		    

        for i in self.xmlPaths.getElementsByTagName('ModPath'):
            self.modulePaths.append(i.firstChild.data)   
      
        self.lwd=self.xmlPaths.getElementsByTagName("LastWorkingDir")[0].firstChild.data
    
    def __cb_lowerlabel(self, event):
        self.lowerlabelstr[0].set("x_int = %d, y_int = %d" % (event.x, event.y))		    
                 		
root=Application()

# end generation windows
