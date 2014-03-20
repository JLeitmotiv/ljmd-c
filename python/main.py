#!/usr/bin/python
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


#md=CDLL("../libljmd-serial.so")
md=CDLL("../libljmd-parallel.so")

if __name__ == "__main__":
   cellfreq=4;
   mdsys=mdsys_t()
   if len(sys.argv)==1:
      mdsys.screen_input()
   elif args.gui:
      mdsys.gui_input()
   else:
      mdsys.file_input(args.file)

   # choice the type of computing
   mdsys.nthreads=8 #Because we are running in parallel mode
   # mdsys.nthreads=1 #Because we are running in serial mode

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
