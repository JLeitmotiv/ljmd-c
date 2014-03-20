#!/usr/bin/python
import sys
import numpy as np
from ctypes import *
from result import Result
from md_classes import mdsys_t
from interface import Application
from Tkinter import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gui", help="gui interface",
                    action="store_true")
args = parser.parse_args()


import time
#md=CDLL("../libljmd-serial.so")
md=CDLL("../libljmd-parallel.so")

if __name__ == "__main__":
   LJPot = LennardJones(2.5, 1000, 1.0, 1.0)
   cellfreq=4;
   mdsys=mdsys_t(LJPot)
   md.start_threads(byref(mdsys))
   if len(sys.argv)==1:
      mdsys.screen_input()
   elif args.gui:
      root = Tk()
      root.title("A simple gui interface for LJMD")
      root.geometry("750x400")
      app = Application(root)
      app.grid()
      root.mainloop()

      mdsys.natoms = int(app.natoms)
      mdsys.mass = float(app.mass)
      mdsys.epsilon = float(app.epsilon)
      mdsys.sigma = float(app.sigma)
      mdsys.rcut = float(app.rcut)
      mdsys.box = float(app.box)
      mdsys.nsteps = int(app.nsteps)
      mdsys.dt = float(app.dt)
      mdsys.nprint = int(app.nprint)
      mdsys.inputfile = app.restfile
      mdsys.file_coord = open(app.trajfile,'w')
      mdsys.file_therm = open(app.ergfile,'w')
   else:
      mdsys.file_input(sys.argv[1])

   mdsys.allocate_arrays()
   mdsys.read_restart()
   md.updcells(byref(mdsys));
   md.ekin(byref(mdsys));
   md.force(byref(mdsys));

   time = []
   mdsys.temp_out = []
   mdsys.ekin_out = []
   mdsys.epot_out = []
   mdsys.etot_out = []

   for i in range(mdsys.nsteps):
      ## This is the main loop, integrator and force calculator
      if (i % mdsys.nprint == 0):
         mdsys.output(i)
         time.append(i)
      md.first_step(byref(mdsys))
      md.force(byref(mdsys))
      md.final_step(byref(mdsys))
      md.ekin(byref(mdsys))
      if (i % cellfreq == 0):
         md.updcells(byref(mdsys))

   ###--- the variables are loaded for plot
   result = Result(time,mdsys.temp_out,mdsys.ekin_out,mdsys.epot_out,mdsys.etot_out)
   result.graph()
