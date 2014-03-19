#!/usr/bin/python
import sys
import numpy as np
from ctypes import *
from result import Result
from md_classes import mdsys_t
from interface import Application
from Tkinter import *
'''
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gui", help="gui interface",
                    action="store_true")
parser.add_argument("-p", "--parallel", help="parallel computing",
                    action="store_true")
parser.add_argument("-f", "--file", help="input file",
                    action="store_true")
args = parser.parse_args()

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
      mdsys.file_coord = app.trajfile
      mdsys.file_therm = app.ergfile

'''

#md=CDLL("../libljmd-serial.so")
md=CDLL("../libljmd-parallel.so")

if __name__ == "__main__":
   cellfreq=4;
   mdsys=mdsys_t()
   if len(sys.argv)==1:
      mdsys.screen_input()
   else:
      mdsys.file_input(sys.argv[1])

   # choice the type of computing
#   if args.parallel:
   mdsys.nthreads=8 #Because we are running in parallel mode
#   else:
#      mdsys.nthreads=1 #Because we are running in serial mode
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

   # fetch the data from file 
#   (time, temp, Ekin, Epot, Etot) = np.loadtxt(mdsys.file_therm, unpack = True)
   ###--- the variables are loaded
   result = Result(time,mdsys.temp_out,mdsys.ekin_out,mdsys.epot_out,mdsys.etot_out)
   result.graph()
