#!/usr/bin/python
from ctypes import *

###--- variables will be comes from program
### this import is valid for only data file

import sys
import numpy as np
from class_and_funtion import * 

md=CDLL("../libljmd-serial.so")

if __name__ == "__main__":
   cellfreq=4;
   mdsys=mdsys_t()
   if len(sys.argv)==1:
      screen_input(mdsys)
   else:
      file_input(sys.argv[1],mdsys)

  # mdsys.natoms=2916
  # mdsys.mass=39.948
  # mdsys.epsilon=0.2379
  # mdsys.sigma=3.405
  # mdsys.rcut=12.0
  # mdsys.box=51.4740
  # mdsys.nsteps=20000
  # mdsys.dt =5.0
  # mdsys.nprint=10
  # mdsys.inputfile="argon_2916.rest"
  # mdsys.thermo_output="argon_2916.dat"
  # mdsys.coord_output="argon_2916.xyz"
  # mdsys.nfi=0
  # mdsys.clist=None
  # mdsys.plist=None
   mdsys.nthreads=1 #Because we are running in serial mode

   allocate_arrays(mdsys)
   read_restart(mdsys)
   printt=prints(mdsys)
   
   md.updcells(byref(mdsys));
   md.ekin(byref(mdsys));
   md.force(byref(mdsys));
   for i in range(mdsys.nsteps):
      ## This is the main loop, integrator and force calculator
      if (i%mdsys.nprint==0):
         printt.print_output(i+1, mdsys)
      md.first_step(byref(mdsys))
      md.force(byref(mdsys))
      md.final_step(byref(mdsys))
      md.ekin(byref(mdsys))
      if (i%cellfreq==0):
         md.updcells(byref(mdsys))

# fetch the data from file 
from result import Result
(time, temp, Ekin, Epot, Etot) = np.loadtxt(mdsys.thermo_output, unpack = True)
###--- the variables are loaded
result = Result(time,temp,Ekin,Epot,Etot)
result.graph()
