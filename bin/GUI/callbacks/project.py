from xml.dom import minidom
import os, re, tkFileDialog

def newProject(app): 
    """Generates a fully xml tree and file of the project trunk. It updates the global variables so that other \
       methods can work on the xml project tree, project trunk, etc."""	
    # change to the last known location of the working directory
  
    os.chdir(app.lwd)

    try:
        ProjFolder = "NewProject.project"	
        os.mkdir(os.path.join(app.lwd, ProjFolder)) 	  
    except:
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
        os.mkdir(os.path.join(os.getcwd(), ProjFolder))     
    
    app.title(ProjFolder)
      
    # create the project trunk:
   
    app.xmlprojfiles["trunk"] = [minidom.Document(), open("%s.xml" % ProjFolder, "a+")] 
    app.xmlprojfiles["trunk"][0].encoding="UTF-8"

    os.chdir(ProjFolder) 

    projelement=app.xmlprojfiles["trunk"][0].createElement("Project")
    projelement.setAttribute('name', ProjFolder.replace(".project", ""))
    app.xmlprojfiles["trunk"][0].appendChild(projelement)
    ########################## Geometry #########################################
    geomelement=app.xmlprojfiles["trunk"][0].createElement("Geometry")
    geomelement.setAttribute('dim', '2D')
    geomelement.setAttribute('type', 'plane')
    geomelement.appendChild(app.xmlprojfiles["trunk"][0].createTextNode("%s.geometry.xml"%ProjFolder.replace(".project", "")))
    projelement.appendChild(geomelement)
    ############################## Mesh #########################################
    meshelement=app.xmlprojfiles["trunk"][0].createElement("Mesh")
    meshelement.setAttribute('status', 'nomesh')
    meshelement.appendChild(app.xmlprojfiles["trunk"][0].createTextNode("%s.mesh.xml"%ProjFolder.replace(".project", "")))
    projelement.appendChild(meshelement)
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

    app.xmlprojfiles["trunk"][1].write(app.xmlprojfiles["trunk"][0].toprettyxml(indent = '   ', encoding=app.xmlprojfiles["trunk"][0].encoding))
    
    app.xmlprojfiles["trunk"][1].close()
    # geometry
    app.xmlprojfiles["geometry"] = [minidom.Document(), open("%s.geometry.xml" % ProjFolder.replace(".project", ""), "a+")]   
    app.xmlprojfiles["geometry"][1].close()
    # mesh
    app.xmlprojfiles["mesh"] = [minidom.Document(), open("%s.mesh.xml" % ProjFolder.replace(".project", ""), "a+")]        
    app.xmlprojfiles["mesh"][1].close()

    app.initDrawingArea()
                                                         
    os.chdir(app.lwd) 
     
    
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
    app.xmlprojfiles["geometry"]=[minidom.parse(geomlocation), open(geomlocation, "a+")]

def saveProject():
    print "Save Project: Not implemented yet!"
    	
def saveAsProject():
    print "Save As Project: Not implemented yet!"

def closeProject(obj):
    try:
        app.xmlprojfiles["trunk"][1].close()
        app.xmlprojfiles["geometry"][1].close()        
    except:
        pass		    
    obj.destroy()
    obj.quit()
