#!/usr/bin/env python

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

def help():
    return "This is *fem a complete fem suite.\n\nOptions: \
                \n\t-h or --help: show this message; \
                \n\t--version: displays the software version; \
                \n\t--authors: shows the list of the software developers; \
                \n\t--openmodel project_name: open a model; \
                \n\t--solve project_name: if the project is ready the solving process begin; \
                \n\t--check project_name: check if a project is complete and ready to solve; \
                \n\t--batch project_name1 project_name2 ... : batch process solving of multiple models; \
                \n\t--debug [along with any other option]: prints extra warning messages including software internals; \
                \n\t--dependencies: outputs the libraries required for *fem to work;"

def authors():
    return "Petrica TARAS"

def version():
    return "0.0.0a"

def libraries():
    return "List of required Python libraries: \n \
            \n\tTkinter - GUI toolkit; \
            \n\tnetworkx - graph library; \
            \n\tsympy - symbolic computation library;"            

if __name__ == "__main__":
    import sys
    if len(sys.argv)==1:
        execfile("./initall.py")
    else: # ufff - better check if these strings are in the sys.argv string list then print them properly. Move the message errors to xml files.
        if len(sys.argv)==2:
            if sys.argv[1]=="-h" or sys.argv[1]=="--help":
                print help()
            elif sys.argv[1]=="--version":
                print version()
            elif sys.argv[1]=="--authors":
                print authors()
            elif sys.argv[1]=="--dependencies":
                print libraries()
            else:
                print "Unrecognized parameter: Please refer to the available help:\n\n"+help()
else:
    pass
