#!/usr/bin/python
#-*- coding: utf-8 -*-
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
from create_potential import *
import argparse
import time

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("-g", "--gui", help="gui interface",
                       action="store_true")
   parser.add_argument("-f", "--file", help="input file",
                       type = str)
   parser.add_argument("-p", "--parallel", help="parallel on",
                       action="store_true")
   args = parser.parse_args()
   if args.parallel: 
      md=CDLL("../libcoffeemd-parallel.so")
   else:   
      md=CDLL("../libcoffeemd-serial.so")


   cellfreq=4;
   mdsys=mdsys_t()
   md.start_threads(byref(mdsys))
 
   if args.gui:
      mdsys.gui_input()
   elif args.file != None:
      mdsys.file_input(args.file)
   else:
      mdsys.screen_input()

   if mdsys.type_potential == 1:
      Pot = LennardJones(mdsys.rcut, mdsys.npoints, mdsys.sigma, mdsys.epsilon)
   else:
      Pot = Morse(mdsys.rcut, mdsys.npoints, mdsys.De, mdsys.a, mdsys.re)
      
   mdsys.ptable.r = Pot.r.ctypes.data_as(POINTER(c_double))
   mdsys.ptable.V = Pot.V.ctypes.data_as(POINTER(c_double))
   mdsys.ptable.F = Pot.F.ctypes.data_as(POINTER(c_double))
   mdsys.ptable.rcut = mdsys.rcut
   mdsys.ptable.npoints = mdsys.npoints

   mdsys.allocate_arrays()
   mdsys.read_restart()

   time = []
   mdsys.temp_out = []
   mdsys.ekin_out = []
   mdsys.epot_out = []
   mdsys.etot_out = []

   mdsys.allocate_arrays()
   mdsys.read_restart()
 
   md.updcells(byref(mdsys))
   md.ekin(byref(mdsys))
   md.force(byref(mdsys))

   for i in range(mdsys.nsteps):
      if (i % mdsys.nprint == 0):
         mdsys.output(i)
         time.append(i)
      md.velverlet(byref(mdsys))
      md.ekin(byref(mdsys))
      if (i % cellfreq == 0):
         md.updcells(byref(mdsys))
      if mdsys.thermostat: md.andersen(byref(mdsys))


   ###--- the variables are loaded for plot
   result = Result(time,mdsys.temp_out,mdsys.ekin_out,mdsys.epot_out,mdsys.etot_out)
   result.graph()
