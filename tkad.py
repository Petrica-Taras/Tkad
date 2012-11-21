#!/usr/bin/env python

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

def main():
    import os
    import sys
    # Find out the location of exaile's working directory, and insert it to sys.path
    basedir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(os.path.join(basedir, "tkad.py")):
        cwd = os.getcwd()
        if os.path.exists(os.path.join(cwd, "tkad.py")):
            basedir = cwd
    sys.path.insert(0, basedir)
    
    from bin.app import Application 
    root = Application()


if __name__ == "__main__":
    main()


