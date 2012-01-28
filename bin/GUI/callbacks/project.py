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

from xml.dom import minidom
import os, re, tkFileDialog
from ..cad import fkernel

def newProject(app): 
    """Generates a fully xml tree and file of the project trunk. It updates the global variables so that other \
       methods can work on the xml project tree, project trunk, etc."""	
    # change to the last known location of the working directory
  
    os.chdir(app.lwd)

    if "NewProject.project" not in os.listdir(os.getcwd()):
        ProjFolder = "NewProject.project"		  
    else:
        dPattern=re.compile(r'^NewProject(\d*).project$')
        ldirs=[s for s in os.listdir(os.getcwd()) if os.path.isdir(s)]      # separate folders from files
        l=[s for s in ldirs if dPattern.search(s) is not None]              # separate folders with pattern "NewProject*.project"

        gldirs=[int(dPattern.search(s).groups()[0]) for s in l if (dPattern.search(s).groups())[0] is not '']             
        if gldirs==[]: ProjFolder = "NewProject1.project"          # found "NewProject.project" in the current directory
        else:
            DirNo=[i for i in range(1, max(gldirs)+1) if i not in gldirs]
            if DirNo == []:
                ProjFolder = "NewProject"+str(max(gldirs)+1)+".project" # found a sequence of "NewProject*.project" named folders
            else:
                ProjFolder = "NewProject"+str(min(DirNo))+".project"    # found a sequence of "NewProject*.project" named folders
                                                                        # with missing pieces    
    
    app.title(ProjFolder)
      
    # create the project trunk:
   
    app.xmlprojfiles["trunk"] = [minidom.Document(), None] 
    app.xmlprojfiles["trunk"][0].encoding="UTF-8"     # to load from a global configuration file !!!

    projelement=app.xmlprojfiles["trunk"][0].createElement("Project")
    projelement.setAttribute('name', ProjFolder.replace(".project", ""))
    app.xmlprojfiles["trunk"][0].appendChild(projelement)
    ########################## Geometry #########################################
    # register the geometry file entry in the project file
    geomelement=app.xmlprojfiles["trunk"][0].createElement("Geometry")
    geomelement.setAttribute('dim', '2D')
    geomelement.setAttribute('type', 'plane')
    geomelement.appendChild(app.xmlprojfiles["trunk"][0].createTextNode("%s.geometry.xml"%ProjFolder.replace(".project", "")))
    projelement.appendChild(geomelement)
    
    # initiate the geometry 
    app.xmlprojfiles["geometry"] = [minidom.Document(), None, []]   
    app.xmlprojfiles["geometry"][0].encoding="UTF-8"
    
    compdomelement=app.xmlprojfiles["geometry"][0].createElement("ComputationDomain")
    compdomelement.setAttribute('dimension', '2D')
    app.xmlprojfiles["geometry"][0].appendChild(compdomelement)
    
    csyselement=app.xmlprojfiles["geometry"][0].createElement("CoorSys")
    pointelement=app.xmlprojfiles["geometry"][0].createElement("Points")
    linelement=app.xmlprojfiles["geometry"][0].createElement("Lines")
    surfacelement=app.xmlprojfiles["geometry"][0].createElement("Surfaces")
    
    pointelement.appendChild(app.xmlprojfiles["geometry"][0].createTextNode(""))
    linelement.appendChild(app.xmlprojfiles["geometry"][0].createTextNode(""))
    surfacelement.appendChild(app.xmlprojfiles["geometry"][0].createTextNode(""))
    
    compdomelement.appendChild(csyselement)
    compdomelement.appendChild(pointelement)
    compdomelement.appendChild(linelement)
    compdomelement.appendChild(surfacelement)
    
    app.xmlprojfiles["geometry"][2]=[csyselement, pointelement, linelement, surfacelement]
    
    ############################## Mesh #########################################
    # register the mesh file entry in the project file
    meshelement=app.xmlprojfiles["trunk"][0].createElement("Mesh")
    meshelement.setAttribute('status', 'nomesh')
    meshelement.appendChild(app.xmlprojfiles["trunk"][0].createTextNode("%s.mesh.xml"%ProjFolder.replace(".project", "")))
    projelement.appendChild(meshelement)
    
    # initiate the mesh 
    app.xmlprojfiles["mesh"] = [minidom.Document(), None]     
        
    ############################ Physics ########################################
    physelement=app.xmlprojfiles["trunk"][0].createElement("Physics")
    physelement.setAttribute('status', 'nophysics')
    physelement.appendChild(app.xmlprojfiles["trunk"][0].createTextNode("%s.physics.xml"%ProjFolder.replace(".project", "")))
    projelement.appendChild(physelement)
    ########################### Assembler #######################################
    assemelement=app.xmlprojfiles["trunk"][0].createElement("Assembler")
    assemelement.setAttribute('custom', 'no')
    assemelement.appendChild(app.xmlprojfiles["trunk"][0].createTextNode("%s.assembler.xml"%ProjFolder.replace(".project", "")))
    projelement.appendChild(assemelement)
    ########################### Postprocess #####################################
    reselement=app.xmlprojfiles["trunk"][0].createElement("Postprocess")
    reselement.setAttribute('status', 'noresults')
    reselement.appendChild(app.xmlprojfiles["trunk"][0].createTextNode("%s.results.xml"%ProjFolder.replace(".project", "")))
    projelement.appendChild(reselement)
    #############################################################################

    app.initDrawingArea()    
    
def openProject(app):
    os.chdir(app.lwd)	
    filetypes=[("Project files", "*project.xml")]	
    openedProject=tkFileDialog.askopenfilename(filetypes=filetypes, title="Open an existing project")
    localdir, localfile = os.path.split(openedProject)
    os.chdir(localdir)
    app.lwd=localdir # to change in the appropriate xml settings file !!!!!!
    app.xmlprojfiles["trunk"]=[minidom.parse(openedProject), openedProject] # app title ??
    app.title(localfile.replace(".xml", ""))
    geomlocation=os.path.join(localdir, os.path.join(localfile.replace(".xml", ""), localfile.replace("project", "geometry")))
    
    # parse the geometry file 
    app.xmlprojfiles["geometry"]=[minidom.parse(geomlocation), None, []]
    
    # draw the geometry file content on canvas
    
    # draw csys
    # parse the info into the appropriate data structure
    
    app.xmlprojfiles["geometry"][2].append(app.xmlprojfiles["geometry"][0].getElementsByTagName("CoorSys")[0])
    csyslist=app.xmlprojfiles["geometry"][0].getElementsByTagName("Csys")

    app.initDrawingArea()
        
    for i in csyslist:
        # retrieve attributes
        if i.getAttribute("id") == "global": # global is already drawn by app.initDrawingArea()
            pass
        else:
            parent=app.DrawingArea.csys[i.getAttribute("parent")]["floatinfo"]

            # retrieve data
            data=i.firstChild.data.strip().split()
            x, y, rotation = float(data[0]), float(data[1]), float(data[2])  
            
            app.DrawingArea.csys[i.getAttribute("id")]={"floatinfo":fkernel.csys(parent=parent, origin=[x, y], rotation=rotation, label=i.getAttribute("id"), type_=i.getAttribute("type")),
                                                    "intPosition":app.DrawingArea.float2int(app.DrawingArea.csys[i.getAttribute("parent")]["intPosition"], 
                                                                            [x, y], i.getAttribute("type")),
                                                    "graphRepr":{"visible":1}}
            # for now the csys are allways visible     
            app.DrawingArea.csys[i.getAttribute("id")]["graphRepr"]["entities"]=app.DrawingArea.dispCsys(app.DrawingArea.float2int(app.DrawingArea.csys[i.getAttribute("parent")]["intPosition"], [x, y], type_=i.getAttribute("type")), rotation=rotation, visible=1)
        
            # associate proper tags 
            app.DrawingArea.csys[i.getAttribute("id")]["graphRepr"]["tags"]=[i.getAttribute("id"), "csys", "translate"]  # add zoom later !!!
        
    for k in app.DrawingArea.csys[i.getAttribute("id")]["graphRepr"]["tags"]: 
        app.DrawingArea.addtag_withtag(k, app.DrawingArea.csys[i.getAttribute("id")]["graphRepr"]["entities"][0])
        app.DrawingArea.addtag_withtag(k, app.DrawingArea.csys[i.getAttribute("id")]["graphRepr"]["entities"][1])                                                     
    
    # draw points
    
    # draw lines
    
    # draw surfaces
    


def saveProject(app):    
    os.chdir(app.lwd)    
    ProjFolder=app.title()
    os.mkdir(os.path.join(os.getcwd(), ProjFolder))
    
    # save main project file first:
    app.xmlprojfiles["trunk"][1] = open("%s.xml" % ProjFolder, "w+")    
    app.xmlprojfiles["trunk"][1].write(app.xmlprojfiles["trunk"][0].toprettyxml(indent = '   ', encoding=app.xmlprojfiles["trunk"][0].encoding)) 
    app.xmlprojfiles["trunk"][1].close()
   
    # save geometry
    os.chdir(ProjFolder)   
    app.xmlprojfiles["geometry"][1] = open("%s.geometry.xml" % ProjFolder.replace(".project", ""), "w+")      
    app.xmlprojfiles["geometry"][1].write(app.xmlprojfiles["geometry"][0].toprettyxml(indent = '   ', encoding=app.xmlprojfiles["geometry"][0].encoding))
    app.xmlprojfiles["geometry"][1].close()
       
    # save mesh
    app.xmlprojfiles["mesh"][1] = open("%s.mesh.xml" % ProjFolder.replace(".project", ""), "w+")   
    app.xmlprojfiles["mesh"][1].close()
    
    os.chdir(app.lwd)     
        	
def saveAsProject(app):
    ProjFolder=os.path.split(tkFileDialog.asksaveasfilename(initialdir=app.lwd, parent=app)) # full path
    
    if ProjFolder is not "":          
        app.title(ProjFolder[1]+".project")
        os.chdir(ProjFolder[0])
    
        app.xmlprojfiles["trunk"][1] = open("%s.project.xml" % ProjFolder[1], "w+")    
        app.xmlprojfiles["trunk"][1].write(app.xmlprojfiles["trunk"][0].toprettyxml(indent = '   ', encoding=app.xmlprojfiles["trunk"][0].encoding)) 
        app.xmlprojfiles["trunk"][1].close()
   
        # save geometry
        os.mkdir(ProjFolder[1]+".project")
        os.chdir(ProjFolder[1]+".project")   
        app.xmlprojfiles["geometry"][1] = open("%s.geometry.xml" % ProjFolder[1], "w+")      
        app.xmlprojfiles["geometry"][1].write(app.xmlprojfiles["geometry"][0].toprettyxml(indent = '   ', encoding=app.xmlprojfiles["geometry"][0].encoding))
        app.xmlprojfiles["geometry"][1].close()
       
        # save mesh
        app.xmlprojfiles["mesh"][1] = open("%s.mesh.xml" % ProjFolder[1], "w+")   
        app.xmlprojfiles["mesh"][1].close()

        os.chdir(ProjFolder[0])
        app.lwd=ProjFolder[0] 

def closeProject(app):
    try:
        app.xmlprojfiles["trunk"][1].close()
        app.xmlprojfiles["geometry"][1].close()      
        app.xmlprojfiles["mesh"][1].close()   
    except:
        pass		    
    app.destroy()
    app.quit()
