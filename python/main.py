#!/usr/bin/python
import sys
import numpy as np
from class_and_funtion import * 
from ctypes import *
from result import Result

#md=CDLL("../libljmd-serial.so")
md=CDLL("../libljmd-parallel.so")

if __name__ == "__main__":
   cellfreq=4;
   mdsys=mdsys_t()
   if len(sys.argv)==1:
      screen_input(mdsys)
   else:
      file_input(sys.argv[1],mdsys)

#   mdsys.nthreads=1 #Because we are running in serial mode
   mdsys.nthreads=8 #Because we are running in parallel mode

   allocate_arrays(mdsys)
   read_restart(mdsys)
   printt=prints(mdsys)
   
   md.updcells(byref(mdsys));
   md.ekin(byref(mdsys));
   md.force(byref(mdsys));
   for i in range(mdsys.nsteps):
      ## This is the main loop, integrator and force calculator
      if (i % mdsys.nprint == 0):
         printt.print_output(i+1, mdsys)
      md.first_step(byref(mdsys))
      md.force(byref(mdsys))
      md.final_step(byref(mdsys))
      md.ekin(byref(mdsys))
      if (i % cellfreq == 0):
         md.updcells(byref(mdsys))

# fetch the data from file 
(time, temp, Ekin, Epot, Etot) = np.loadtxt(mdsys.thermo_output, unpack = True)
###--- the variables are loaded
result = Result(time,temp,Ekin,Epot,Etot)
result.graph()
