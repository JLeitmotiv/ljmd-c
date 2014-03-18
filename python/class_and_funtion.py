#input reading and preparing file#
import sys
import numpy as np


class prints(object):
   def __init__(self,mdinfo):
       gp.open(mdinfo.coord_output,'w')
       fp.open(mdinfo.thermo_output,'w')

   def print_output(self,mdinfo):
     gp.write("%s %s\n"%(aux[0],aux[int(col_num)-1]))
     fp.write("% 8d % 20.8f % 20.8f % 20.8f % 20.8f\n"%(mdinfo.nfi,mdinfo.temp,mdinfo.ekin,mdinfo.epot,mdinfo.ekin+mdinfo.epot))
     gp.write("%d\n nfi=%d etot=%20.8f\n"%mdinfo.natoms,mdinfo.nfi,mdinfo.ekin+mdinfo.epot))
     for i in range(mdinfo.natoms)
     gp.write("Ar  %20.8f %20.8f %20.8f\n"%(mdinfo.pos[i]%mdinfo.pos[natoms+i]%mdinfo.pos[2*natoms+i]))

def grow_array(mdinfo):
 mdinfo.pos=np.zeros(mdinfo.natoms*3)
 mdinfo.vel=np.zeros(mdinfo.natoms*3)
    
def read_restart(mdinfo):
 fp = open(mdinfo.inputfile,'rb')
 print len(mdinfo.pos)
 for i in range(mdinfo.natoms):   
  line=fp.readline()
  aux=line.split()
  mdinfo.pos[i]=aux[0]
  mdinfo.pos[i+mdinfo.natoms]=aux[1]
  mdinfo.pos[i+2*mdinfo.natoms]=aux[2]
 for i in range(mdinfo.natoms):
  line=fp.readline()
  aux=line.split() 
  mdinfo.vel[i]=aux[0] 
  mdinfo.vel[i+mdinfo.natoms]=aux[1]
  mdinfo.vel[i+2*mdinfo.natoms]=aux[2]
 fp.close()


def file_input(mdinfo):
 0

def screen_input(mdinfo):
 print "Number of atoms"
 mdinfo.natoms=int(raw_input())
 print "mass in AMU"
 mdinfo.mass=raw_input()
 print "epsilon in Kcal/mol"
 mdinfo.epsilon=raw_input()
 print "sigma in angstrom"
 mdinfo.sigma=raw_input()
 print "Radius cut in angstrom"
 mdinfo.rcut=raw_input()
 print "box length (in angstrom)"
 mdinfo.box=raw_input()
 print "MD Steps"
 mdinfo.nsteps=raw_input()
 print "time step (in femtoseconds)"
 mdinfo.dt =raw_input()
 print "print frecuency" 
 mdinfo.nprint=raw_input()
 print "input file"
 mdinfo.inputfile=raw_input()
 print "thermo_output file"
 mdinfo.thermo_output=raw_input()
 print "coord_output"
 mdinfo.coord_output=raw_input()

class mdsys_t(object):
  dt=0; mass=0; epsilon=0; sigma=0; box=0; rcut=0; ekin=0
  epot=0; temp=0; _pad1=0; pos=[]; vel=[]; frc=[]; cell_t=0 
  clist=[]; plist=[]; _pad2=0; natoms=0; nfi=0; nsteps=0
  nthreads=0; ngrid=0; ncell=0; npair=0; nidx=0; delta=0;nprint=0
  thermo_output=''; coord_output='';inputfile=''

