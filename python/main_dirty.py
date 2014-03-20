#!/usr/bin/python
import sys
import numpy as np
from ctypes import *
from result import Result
from md_classes import mdsys_t
from create_potential import *
from interface import Application
from Tkinter import *


import time
md=CDLL("../libljmd-serial.so")
#md=CDLL("../libljmd-parallel.so")

if __name__ == "__main__":
   LJPot = LennardJones(8.5, 10000, 3.405, 0.2379)
   cellfreq=4;
   mdsys=mdsys_t()
   md.start_threads(byref(mdsys))
   mdsys.natoms = 108
   mdsys.dt = 1.0
   mdsys.mass = 39.948
   mdsys.box = 17.1580
   mdsys.nsteps = 10000
   mdsys.nprint = 100
   mdsys.inputfile = "argon_108.rest"
   mdsys.file_coord = open("argon_108.xyz",'w')
   mdsys.file_therm = open("argon_108.dat",'w')
   mdsys.ptable.npoints = 10000
   mdsys.ptable.rcut = 8.5
   mdsys.ptable.r = LJPot.r.ctypes.data_as(POINTER(c_double))
   mdsys.ptable.V = LJPot.V.ctypes.data_as(POINTER(c_double))
   mdsys.ptable.F = LJPot.F.ctypes.data_as(POINTER(c_double))

   mdsys.allocate_arrays()
   mdsys.read_restart()
   print mdsys.natoms
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
      print i, mdsys.ekin, mdsys.epot, mdsys.ekin+mdsys.epot
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
