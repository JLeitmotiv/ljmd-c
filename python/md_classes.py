#This file creates a structure that has the elements common to c object mdsys, the base one in which we
#have all the info. Here is the mdsys structure and how it is defined:
#There is a class mdsys_t that contains all the variables, defined as c_types, needed by the C library in order to perfom the MD simulation. It also contains more variables and function use by the main program in phython.
#The function contained are input for screen, file, GUI and output which are self explanatory
#
#Note: this might not be the best way to organize the program a future improvement could be separate variables in subclass accord to they use in the program in order to make a future improvement easier. 



from ctypes import *
from interface import Application
from Tkinter import *

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
               ("tempin", c_double),
               ("_pad1", c_double),
               ("tempout",c_double),
               ("nu",c_double),
               ("var_andersen",c_double),
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
      self.thermostat=False

   def allocate_arrays(self):
      self.pos=(c_double * (self.natoms * 3) )()
      self.vel=(c_double * (self.natoms * 3) )()
      self.frc=(c_double * (self.nthreads * self.natoms * 3) )()
      
   def read_restart(self):
      with open(self.inputfile, 'rb') as fp:
         for i in range(self.natoms):   
            line=fp.readline()
            try:
               aux=[float(j) for j in line.split()]
               self.pos[i]=aux[0]
               self.pos[i+self.natoms]=aux[1]
               self.pos[i+2*self.natoms]=aux[2]
            except ValueError:
               print "Error when trying to read_restart position in line %i" % (i+1)
               raise
         for i in range(self.natoms):
            line=fp.readline()
            try:
               aux=[float(j) for j in line.split()]
               self.vel[i]=aux[0] 
               self.vel[i+self.natoms]=aux[1]
               self.vel[i+2*self.natoms]=aux[2]
            except ValueError:
               print "Error when trying to read_restart velocity in line %i" % (i+1+self.natoms)
               raise
            
           
   def file_input(self,lineinp):
      with open(lineinp, 'rb') as fp:
         for line in fp:
            no_comment = line.split('#')[0]
            inp = [i.strip() for i in no_comment.split(' ')]
            key = inp[0]
            val = inp[1]
            if key=="natoms":
               self.natoms=int(inp[1])
            elif key=="mass":
               self.mass=float(inp[1])
            elif key=="epsilon":
               self.epsilon=float(inp[1])
            elif key=="sigma":   
               self.sigma=float(inp[1])
            elif key=="rcut":
               self.rcut=float(inp[1])
            elif key=="boxlength":
               self.box=float(inp[1])
            elif key=="nsteps":
               self.nsteps=int(inp[1])
            elif key=="timestep":
               self.dt =float(inp[1])
            elif key=="print":
               self.nprint=int(inp[1])
            elif key=="restart":
               self.inputfile=inp[1].strip()
            elif key=="thermo":
               self.file_therm = open(inp[1].strip(),'w')
            elif key=="coord":
               self.file_coord = open(inp[1].strip(),'w')
            elif key=="Andersen":
               self.tempin=float(inp[1])
               self.nu=float(inp[2])
               self.thermostat=True 
               mvsq2e=2390.05736153349
               kboltz=0.0019872067
               self.var_andersen=(kboltz*self.tempin/mvsq2e/self.mass)**0.5
            elif key=="nsteps":
                self.nsteps=int(inp[1])

   def gui_input(self):
      root = Tk()
      root.title("A simple gui interface for LJMD")
      root.geometry("750x400")
      app = Application(root)
      app.grid()
      root.mainloop()

      self.natoms = int(app.natoms)
      self.mass = float(app.mass)
      self.epsilon = float(app.epsilon)
      self.sigma = float(app.sigma)
      self.rcut = float(app.rcut)
      self.box = float(app.box)
      self.nsteps = int(app.nsteps)
      self.dt = float(app.dt)
      self.nprint = int(app.nprint)
      self.inputfile = app.restfile
      self.file_coord = open(app.trajfile,'w')
      self.file_therm = open(app.ergfile,'w')

   def screen_input(self):
      print "Number of atoms"
      self.natoms=int(raw_input())
      print "mass in AMU"
      self.mass=float(raw_input())
      print "epsilon in Kcal/mol"
      self.epsilon=float(raw_input())
      print "sigma in angstrom"
      self.sigma=float(raw_input())
      print "Radius cut in angstrom"
      self.rcut=float(raw_input())
      print "box length (in angstrom)"
      self.box=float(raw_input())
      print "MD Steps"
      self.nsteps=int(raw_input())
      print "time step (in femtoseconds)"
      self.dt =float(raw_input())
      print "print frecuency" 
      self.nprint=int(raw_input())
      print "input file"
      self.inputfile=raw_input()
      print "thermo_output file"
      self.file_therm = open(raw_input(), 'w')
      print "coord_output"
      self.file_coord  = open(raw_input(), 'w')

   def output(self, step):
      self.file_therm.write("%8d %20.8f %20.8f %20.8f %20.8f\n" %
                            (step,self.tempout,self.ekin,
                             self.epot,self.ekin+self.epot))

      self.temp_out.append(self.tempout)
      self.ekin_out.append(self.ekin)
      self.epot_out.append(self.epot)
      self.etot_out.append(self.ekin+self.epot)

      self.file_coord.write("%d\n nfi=%d etot=%20.8f\n"% 
                            (self.natoms,step,
                             self.ekin+self.epot))
      for i in range(self.natoms):
         self.file_coord.write("Ar  %20.8f %20.8f %20.8f\n"%
                               (self.pos[i],self.pos[self.natoms+i],
                                self.pos[2*self.natoms+i]))

