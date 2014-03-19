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
parser.add_argument("-p", "--parallel", help="parallel computing",
                    action="store_true")
args = parser.parse_args()

#md=CDLL("../libljmd-serial.so")
md=CDLL("../libljmd-parallel.so")

if __name__ == "__main__":
   cellfreq=4;
   mdsys=mdsys_t()
   if len(sys.argv)==1:
      mdsys.screen_input()
   elif args.gui:
      root = Tk()
      root.title("A simple gui interface for LJMD")
      root.geometry("750x400")
      app = Application(root)
      app.grid()
      root.mainloop()

      mdsys.natoms = app.natoms
      mdsys.mass = app.mass
      mdsys.epsilon = app.epsilon
      mdsys.sigma = app.sigma
      mdsys.rcut = app.rcut
      mdsys.box = app.box
      mdsys.nsteps = app.nsteps
      mdsys.dt = app.dt
      mdsys.nprint = app.nprint
      mdsys.inputfile = app.restfile
      mdsys.file_coord = app.trajfile
      mdsys.file_therm = app.ergfile
   else:
      mdsys.file_input(sys.argv[1])

   # choice the type of computing
   if args.parallel:
      mdsys.nthreads=8 #Because we are running in parallel mode
   else:
      mdsys.nthreads=1 #Because we are running in serial mode


   mdsys.allocate_arrays()
   mdsys.read_restart()
   
   md.updcells(byref(mdsys));
   md.ekin(byref(mdsys));
   md.force(byref(mdsys));
   for i in range(mdsys.nsteps):
      ## This is the main loop, integrator and force calculator
      if (i % mdsys.nprint == 0):
         mdsys.output(i)
      md.first_step(byref(mdsys))
      md.force(byref(mdsys))
      md.final_step(byref(mdsys))
      md.ekin(byref(mdsys))
      if (i % cellfreq == 0):
         md.updcells(byref(mdsys))

# fetch the data from file 
(time, temp, Ekin, Epot, Etot) = np.loadtxt(mdsys.file_therm.name, unpack = True)
###--- the variables are loaded
result = Result(time,temp,Ekin,Epot,Etot)
result.graph()
