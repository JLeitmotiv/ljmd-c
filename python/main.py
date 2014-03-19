#!/usr/bin/python
import sys
import numpy as np
from ctypes import *
from result import Result
from md_classes import mdsys_t

#md=CDLL("../libljmd-serial.so")
md=CDLL("../libljmd-parallel.so")

if __name__ == "__main__":
   cellfreq=4;
   mdsys=mdsys_t()
   if len(sys.argv)==1:
      mdsys.screen_input()
   else:
      mdsys.file_input(sys.argv[1])

#   mdsys.nthreads=1 #Because we are running in serial mode
   mdsys.nthreads=8 #Because we are running in parallel mode

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
