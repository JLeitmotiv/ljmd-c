#input reading and preparing file#
import sys
import numpy as np

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
 print mdsys.vel, mdsys.pos

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
 print "output file"
 mdinfo.output=raw_input()

class mdsys_t(object):
  dt=0; mass=0; epsilon=0; sigma=0; box=0; rcut=0; ekin=0
  epot=0; temp=0; _pad1=0; pos=[]; vel=[]; frc=[]; cell_t=0 
  clist=[]; plist=[]; _pad2=0; natoms=0; nfi=0; nsteps=0
  nthreads=0; ngrid=0; ncell=0; npair=0; nidx=0; delta=0;nprint=0
  output='';inputfile=''

if __name__ == "__main__":
    mdsys=mdsys_t()
    if len(sys.argv)==1:
       screen_input(mdsys)
    else:
       file_input(mdsys)
    grow_array(mdsys)    
    read_restart(mdsys)
