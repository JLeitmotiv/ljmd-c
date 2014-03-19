"""
This file creates a structure that has the elements
common to c object mdsys, the base one in which we
have all the info. Here is the mdsys structure and
how it is defined:

/* structure for md system */
struct _mdsys {
  double dt, mass, epsilon, sigma, box, rcut;
  double ekin, epot, temp, _pad1;
  double *pos, *vel, *frc;
  cell_t *clist;
  int *plist, _pad2;
  int natoms, nfi, nsteps, nthreads;
  int ngrid, ncell, npair, nidx;
  double delta;
};
typedef struct _mdsys mdsys_t;

/* structure for cell-list data */
struct _cell {
  int natoms;                 /* number of atoms in this cell */
  int owner;                  /* task/thread id that owns this cell */
  int *idxlist;               /* list of atom indices */
};
typedef struct _cell cell_t;
#input reading and preparing file#
"""

import sys
import numpy as np
from ctypes import *

class cell_t(Structure):
   _fields_ = [("natoms", c_int),
               ("owner", c_int),
               ("idxlist", POINTER(c_int))]
   
class mdsys_t(Structure):
   _fields_ = [("dt", c_double),
               ("mass", c_double),
               ("epsilon", c_double),
               ("sigma", c_double),
               ("box", c_double),
               ("rcut", c_double),
               ("ekin", c_double),
               ("epot", c_double),
               ("temp", c_double),
               ("_pad1", c_double),
               ("pos", POINTER(c_double)),
               ("vel", POINTER(c_double)),
               ("frc", POINTER(c_double)),
               ("clist", POINTER(cell_t)),
               ("plist", POINTER(c_int)),
               ("_pad2", c_int),
               ("natoms", c_int),
               ("nfi", c_int),
               ("nsteps", c_int),
               ("nthreads", c_int),
               ("ngrid", c_int),
               ("ncell", c_int),
               ("npair", c_int),
               ("nidx", c_int),
               ("delta", c_double)]
   def __init__(self):
      self.nfi=0
      self.clist=None
      self.plist=None
      
class prints(object):
   def __init__(self,mdinfo):
      self.gp = open(mdinfo.coord_output,'w')
      self.fp = open(mdinfo.thermo_output,'w')

   def print_output(self,nfi,mdinfo):
      self.fp.write("%8d %20.8f %20.8f %20.8f %20.8f\n" %
                    (nfi,mdinfo.temp,mdinfo.ekin,
                     mdinfo.epot,mdinfo.ekin+mdinfo.epot))
      self.gp.write("%d\n nfi=%d etot=%20.8f\n"% 
                    (mdinfo.natoms,mdinfo.nfi,
                     mdinfo.ekin+mdinfo.epot))
      for i in range(mdinfo.natoms):
         self.gp.write("Ar  %20.8f %20.8f %20.8f\n"%
                       (mdinfo.pos[i],mdinfo.pos[mdinfo.natoms+i],
                        mdinfo.pos[2*mdinfo.natoms+i]))

def allocate_arrays(mdinfo):
   mdinfo.pos=(c_double * (mdinfo.natoms * 3) )()
   mdinfo.vel=(c_double * (mdinfo.natoms * 3) )()
   mdinfo.frc=(c_double * (mdinfo.nthreads * mdinfo.natoms * 3) )()
   
def read_restart(mdinfo):
   fp = open(mdinfo.inputfile,'rb')
   for i in range(mdinfo.natoms):   
      line=fp.readline()
      try:
         aux=[float(j) for j in line.split()]
         mdinfo.pos[i]=aux[0]
         mdinfo.pos[i+mdinfo.natoms]=aux[1]
         mdinfo.pos[i+2*mdinfo.natoms]=aux[2]
      except ValueError:
         print "Error when trying to read_restart position in line %i" % (i+1)
         raise
   for i in range(mdinfo.natoms):
      line=fp.readline()
      try:
         aux=[float(j) for j in line.split()]
         mdinfo.vel[i]=aux[0] 
         mdinfo.vel[i+mdinfo.natoms]=aux[1]
         mdinfo.vel[i+2*mdinfo.natoms]=aux[2]
      except ValueError:
         print "Error when trying to read_restart velocity in line %i" % (i+1+mdinfo.natoms)
         raise
   fp.close()


def file_input(lineinp,mdinfo):
   fp=open(lineinp,'rb')
   for line in fp:
      #discard comments and parse instructions
      no_comment = line.split('#')[0]
      print no_comment
      #parse input
      inp = [i.strip() for i in no_comment.split(' ')]
      key = inp[0]
      val = inp[1]
      if key=="natoms":
         mdinfo.natoms=int(val)
      elif key=="mass":
         mdinfo.mass=float(val)
      elif key=="epsilon":
         mdinfo.epsilon=float(val)
      elif key=="sigma":   
         mdinfo.sigma=float(val)
      elif key=="rcut":
         mdinfo.rcut=float(val)
      elif key=="boxlength":
         mdinfo.box=float(val)
      elif key=="nsteps":
         mdinfo.nsteps=int(val)
      elif key=="timestep":
         mdinfo.dt =float(val)
      elif key=="print":
         mdinfo.nprint=int(val)
      elif key=="restart":
         mdinfo.inputfile=val.strip()
      elif key=="thermo":
         mdinfo.thermo_output=val.strip()
      elif key=="coord":
         mdinfo.coord_output=val.strip()
      else:
         raise ValueError('Could not find option %s' % key)
   fp.close()

def screen_input(mdinfo):
   print "Number of atoms"
   mdinfo.natoms=int(raw_input())
   print "mass in AMU"
   mdinfo.mass=float(raw_input())
   print "epsilon in Kcal/mol"
   mdinfo.epsilon=float(raw_input())
   print "sigma in angstrom"
   mdinfo.sigma=float(raw_input())
   print "Radius cut in angstrom"
   mdinfo.rcut=float(raw_input())
   print "box length (in angstrom)"
   mdinfo.box=float(raw_input())
   print "MD Steps"
   mdinfo.nsteps=int(raw_input())
   print "time step (in femtoseconds)"
   mdinfo.dt =float(raw_input())
   print "print frecuency" 
   mdinfo.nprint=int(raw_input())
   print "input file"
   mdinfo.inputfile=raw_input()
   print "thermo_output file"
   mdinfo.thermo_output=raw_input()
   print "coord_output"
   mdinfo.coord_output=raw_input()
