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

if __name__ == "__main__":
     from bin.app import Application

     from bin.GUI.common.settings import settings
     from bin.GUI.common.model import model
     from bin.GUI.common.state import state     

     settingsObj = settings()
     modelObj    = model() 
     stateObj    = state()

     root   = Application(settings, model, state)
