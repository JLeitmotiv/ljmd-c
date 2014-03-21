#!/usr/bin/python


#This is a python Interface that couples whit a Molecular Dynamics program write in C.
#The features supported are:
#       Lennard-Jones potential 
#       Verlet integrator for constant energy or constant temperature simulation
#       Easy input from a GUI or text file
#       Automatic plotting of Energy and Temperature graphs
#       Output of Coordinates in xyz format
#       Output of thermodynamic data  
#       Step Temp Ekin Epot Etot	 

#Authoring of the C code corresponds to Axel Kohlmeyer
#Authoring of Python interface corresponds to Alcain Pablo, Hoque Md. Enamul, Factorovich Matias.


import sys
import numpy as np
from ctypes import *
from result import Result
from md_classes import mdsys_t

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gui", help="gui interface",
                    action="store_true")
parser.add_argument("-f", "--file", help="input file",
                    type = str)
args = parser.parse_args()


import time
md=CDLL("../libljmd-serial.so")
#md=CDLL("../libljmd-parallel.so")

if __name__ == "__main__":
   cellfreq=4;
   mdsys=mdsys_t()
   md.start_threads(byref(mdsys))
 
   if len(sys.argv)==1:
      mdsys.screen_input()
   elif args.gui:
      mdsys.gui_input()
   else:
      mdsys.file_input(args.file)

   # choice the type of computing
#   mdsys.nthreads=8 #Because we are running in parallel mode
   mdsys.nthreads=1 #Because we are running in serial mode

   mdsys.allocate_arrays()
   mdsys.read_restart()

   time = []
   mdsys.temp_out = []
   mdsys.ekin_out = []
   mdsys.epot_out = []
   mdsys.etot_out = []

   mdsys.allocate_arrays()
   mdsys.read_restart()
 
   md.updcells(byref(mdsys));
   md.ekin(byref(mdsys));
   md.force(byref(mdsys));

   if mdsys.thermostat==False:  
    for i in range(mdsys.nsteps):
      ## This is the main loop, integrator and force calculator
      if (i % mdsys.nprint == 0):
         mdsys.output(i)
         time.append(i)
      md.velverlet(byref(mdsys))
      md.ekin(byref(mdsys))
      if (i % cellfreq == 0):
         md.updcells(byref(mdsys))
   if mdsys.thermostat==True:
    for i in range(mdsys.nsteps):
      ## This is the main loop, integrator and force calculator
      if (i % mdsys.nprint == 0):
         mdsys.output(i)
         time.append(i)
      md.velverlet(byref(mdsys))
      md.ekin(byref(mdsys))
      md.andersen(byref(mdsys))
      if (i % cellfreq == 0):
         md.updcells(byref(mdsys))


   ###--- the variables are loaded for plot
   result = Result(time,mdsys.temp_out,mdsys.ekin_out,mdsys.epot_out,mdsys.etot_out)
   result.graph()
