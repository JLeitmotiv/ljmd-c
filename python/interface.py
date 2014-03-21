#This is a simple Graphical User Interface that imports the info from an input text file,
#everything can be change except for the number of atoms and the restart file because 
#of incompatibilities 

from Tkinter import *
import tkMessageBox

class Application(Frame):
    """
    This is the GUI frontend. It sets some default values and 
    can be used to choose between Morse and Lennard Jones potential
    """
    def __init__(self, master):
        Frame.__init__(self, master)
	self.natoms = 108
        self.mass = 39.948
        self.epsilon = 0.2379
        self.sigma = 3.405
        self.rcut = 8.5
        self.box = 17.1580
        self.nsteps = 10000
        self.dt = 5.0
        self.nprint = 100
        self.restfile = 'argon_108.rest'
        self.trajfile = 'argon_108.xyz'
        self.ergfile = 'argon_108.dat'
        self.npoints = 10000

        self.de = 13.836
        self.a = 0.84
        self.re = 3.98

        self.tempin = 95.0
        self.nu = 0.1
        self.thermostat = False
        self.var_andersen = 0.0
	self.check_andersen = ''

	self.short_description = ''

	# for radiobutton of potential
	self.v = IntVar()
	self.v.set(3)  

	self.potential = [
	    (1, "Lennard Jones"),
	    (2, "Morse"),
	    (3, "Home Made")
	]
	self.ch_pot = ''

	# for radiobutton of integrator
	self.integrator = IntVar()
	self.integrator.set(1)  

	self.intg = [
	    (1, "Verlet"),
	    (2, "Integrator 2")
	]
	self.ch_intg = ''

	# for radiobutton of Thermostate
	self.thermostate = IntVar()
	self.thermostate.set(2)  

	self.th_state = [
	    (1, "Andersen"),
	    (2, "None")
	]
	self.ch_state = ''

        self.grid()
        self.widget()
	self.ShowChoiceThermo()
	self.ShowChoiceParam()

    def ShowChoiceParam(self):
    	if (self.v.get()==1):
           self.type_potential = 1

   	   # value of epsilon
           self.epsilon_label = Label(self, text = "Epsilon (in kj/mol): ")
           self.epsilon_label.grid(row=4, column=2, sticky=W, pady=4)
           self.epsilon_entry = Entry(self, bg = "#fff")
	   self.epsilon_entry.insert(END, self.epsilon)
           self.epsilon_entry.grid(row=4, column=3, sticky=W, pady=4)

	   # value of sigma
           self.sigma_label = Label(self, text = "Sigma (in angstrom): ")
           self.sigma_label.grid(row=5, column=2, sticky=W, pady=4)
           self.sigma_entry = Entry(self, bg = "#fff")
	   self.sigma_entry.insert(END, self.sigma)
           self.sigma_entry.grid(row=5, column=3, sticky=W, pady=4)

    	elif (self.v.get()==2):
           self.type_potential = 2

   	   # value of de
           self.de_label = Label(self, text = "Param 1 (De): ")
           self.de_label.grid(row=4, column=2, sticky=W, pady=4)
           self.de_entry = Entry(self, bg = "#fff")
	   self.de_entry.insert(END, self.de)
           self.de_entry.grid(row=4, column=3, sticky=W, pady=4)

	   # value of a
           self.a_label = Label(self, text = "Param 2 (a): ")
           self.a_label.grid(row=5, column=2, sticky=W, pady=4)
           self.a_entry = Entry(self, bg = "#fff")
	   self.a_entry.insert(END, self.a)
           self.a_entry.grid(row=5, column=3, sticky=W, pady=4)

   	   # value of re
           self.re_label = Label(self, text = "Param 3 (re): ")
           self.re_label.grid(row=6, column=2, sticky=W, pady=4)
           self.re_entry = Entry(self, bg = "#fff")
	   self.re_entry.insert(END, self.re)
           self.re_entry.grid(row=6, column=3, sticky=W, pady=4)

    def ShowChoiceThermo(self):
    	if (self.thermostate.get()==1):
	    # Trajectory file
            self.tempin_label = Label(self, text = "Temperature: ")
            self.tempin_label.grid(row=10, column=2, sticky=W, pady=4)
            self.tempin_entry = Entry(self, bg = "#fff")
	    self.tempin_entry.insert(END, self.tempin)
            self.tempin_entry.grid(row=10, column=3, sticky=W, pady=4)

	    # Output energies file
            self.nu_label = Label(self, text = "Frequency: ")
            self.nu_label.grid(row=11, column=2, sticky=W, pady=4)
            self.nu_entry = Entry(self, bg = "#fff")
	    self.nu_entry.insert(END, self.nu)
            self.nu_entry.grid(row=11, column=3, sticky=W, pady=4)

    	    Radiobutton(self, 
                text='None',
                variable=self.thermostate,
		command=self.ShowChoiceThermo, 
                value=2).grid(row=12, column=3, sticky=W, pady=4)

    def Andersen(self, master):
    	if (self.thermostate.get()==1):
            self.tempin=float(self.tempin_entry.get())
            self.nu=float(self.nu_entry.get())
            self.thermostat=True 
            mvsq2e=2390.05736153349
            kboltz=0.0019872067
            self.var_andersen=(kboltz*self.tempin/mvsq2e/float(self.mass))**0.5

    def widget(self):
        self.description_text = '''
Please give the input parameter
 to run in CoffeeMD
		'''
        self.description_label = Label(self, text = self.description_text)
        self.description_label.grid(row=0, column=0, sticky=W, pady=8)

	# number of atoms
        self.natoms_label = Label(self, text = "Number of Atoms: ")
        self.natoms_label.grid(row=1, column=0, sticky=W, pady=4)
        self.natoms_entry = Entry(self, bg = "#fff")
	self.natoms_entry.insert(END, self.natoms)
        self.natoms_entry.grid(row=1, column=1, sticky=W, pady=4)

	# mass of atoms
        self.mass_label = Label(self, text = "Mass of Atoms (in amu): ")
        self.mass_label.grid(row=2, column=0, sticky=W, pady=4)
        self.mass_entry = Entry(self, bg = "#fff")
	self.mass_entry.insert(END, self.mass)
        self.mass_entry.grid(row=2, column=1, sticky=W, pady=4)

	# rcut 
        self.rcut_label = Label(self, text = "rcut (in angstrom): ")
        self.rcut_label.grid(row=3, column=0, sticky=W, pady=4)
        self.rcut_entry = Entry(self, bg = "#fff")
	self.rcut_entry.insert(END, self.rcut)
        self.rcut_entry.grid(row=3, column=1, sticky=W, pady=4)

	# length of box
        self.box_label = Label(self, text = "box length (in angstrom): ")
        self.box_label.grid(row=4, column=0, sticky=W, pady=4)
        self.box_entry = Entry(self, bg = "#fff")
	self.box_entry.insert(END, self.box)
        self.box_entry.grid(row=4, column=1, sticky=W, pady=4)

	# Number of steps in MD
        self.nsteps_label = Label(self, text = "Number of steps in MD: ")
        self.nsteps_label.grid(row=5, column=0, sticky=W, pady=4)
        self.nsteps_entry = Entry(self, bg = "#fff")
	self.nsteps_entry.insert(END, self.nsteps)
        self.nsteps_entry.grid(row=5, column=1, sticky=W, pady=4)

	# MD time step (in fs)
        self.dt_label = Label(self, text = "MD time step (in fs): ")
        self.dt_label.grid(row=6, column=0, sticky=W, pady=4)
        self.dt_entry = Entry(self, bg = "#fff")
	self.dt_entry.insert(END, self.dt)
        self.dt_entry.grid(row=6, column=1, sticky=W, pady=4)

	# output print frequency
        self.nprint_label = Label(self, text = "output print frequency: ")
        self.nprint_label.grid(row=7, column=0, sticky=W, pady=4)
        self.nprint_entry = Entry(self, bg = "#fff")
	self.nprint_entry.insert(END, self.nprint)
        self.nprint_entry.grid(row=7, column=1, sticky=W, pady=4)

	# npoint 
        self.npoint_label = Label(self, text = "Point number for interpolation: ")
        self.npoint_label.grid(row=8, column=0, sticky=W, pady=4)
        self.npoint_entry = Entry(self, bg = "#fff")
	self.npoint_entry.insert(END, self.npoints)
        self.npoint_entry.grid(row=8, column=1, sticky=W, pady=4)

	# restart file
        self.restfile_label = Label(self, text = "Restfile (in *.rest): ")
        self.restfile_label.grid(row=9, column=0, sticky=W, pady=4)
        self.restfile_entry = Entry(self, bg = "#fff")
	self.restfile_entry.insert(END, self.restfile)
        self.restfile_entry.grid(row=9, column=1, sticky=W, pady=4)

	# Trajectory file
        self.trajfile_label = Label(self, text = "Trajectory ( in *.xyz): ")
        self.trajfile_label.grid(row=10, column=0, sticky=W, pady=4)
        self.trajfile_entry = Entry(self, bg = "#fff")
	self.trajfile_entry.insert(END, self.trajfile)
        self.trajfile_entry.grid(row=10, column=1, sticky=W, pady=4)

	# Output energies file
        self.ergfile_label = Label(self, text = "Output energies (in *.dat): ")
        self.ergfile_label.grid(row=11, column=0, sticky=W, pady=4)
        self.ergfile_entry = Entry(self, bg = "#fff")
	self.ergfile_entry.insert(END, self.ergfile)
        self.ergfile_entry.grid(row=11, column=1, sticky=W, pady=4)

	# radio potential
        self.potential_label = Label(self, text = "Potential: ")
        self.potential_label.grid(row=1, column=2, sticky=W, pady=4)
	for val, txt in self.potential:
    	    Radiobutton(self, 
                text=txt,
                variable=self.v, 
		command=self.ShowChoiceParam, 
                value=val).grid(row=val, column=3, sticky=W, pady=4)

	# radio integrator
        self.intg_label = Label(self, text = "Integrator: ")
        self.intg_label.grid(row=7, column=2, sticky=W, pady=4)
	for val, txt in self.intg:
    	    Radiobutton(self, 
                text=txt,
                variable=self.integrator, 
                value=val).grid(row=val+6, column=3, sticky=W, pady=4)

	# radio thermostate
        self.intg_label = Label(self, text = "Thermostat: ")
        self.intg_label.grid(row=9, column=2, sticky=W, pady=4)
	for val, txt in self.th_state:
    	    Radiobutton(self, 
                text=txt,
                variable=self.thermostate,
		command=self.ShowChoiceThermo, 
                value=val).grid(row=val+8, column=3, sticky=W, pady=4)

	# Information 
        self.info_label = Label(self, text = "CoffeeMD Graphical User Interface")
        self.info_label.grid(row=14, column=0, sticky=W, pady=4)

	# run button 
        self.button_run = Button(self, text = "run", command=self.on_run)
        self.button_run.grid(row=14, column=3, sticky=W, pady=4)

    def on_run(self):
	self.natoms = self.natoms_entry.get()
        self.mass = self.mass_entry.get()
        self.rcut = self.rcut_entry.get()
        self.box = self.box_entry.get()
        self.nsteps = self.nsteps_entry.get()
        self.dt = self.dt_entry.get()
        self.nprint = self.nprint_entry.get()
        self.restfile = self.restfile_entry.get()
        self.trajfile = self.trajfile_entry.get()
        self.ergfile = self.ergfile_entry.get()
	self.ch_pot = str(self.v.get())
	self.ch_intg = str(self.integrator.get())
	self.ch_state = str(self.thermostate.get())

	if self.v.get()==1:
           self.epsilon = self.epsilon_entry.get()
           self.sigma = self.sigma_entry.get()

     	   self.check_andersen = '\nepsilon: ' + self.epsilon + '\nsigma: ' + self.sigma
	elif self.v.get()==2:
           self.de = self.de_entry.get()
           self.a = self.a_entry.get()
           self.re = self.re_entry.get()

     	   self.check_andersen = '\nde: ' + self.de + '\na: ' + self.a +'\nre: ' + self.re

        a = self.potential[int(self.ch_pot)-1]
	b = self.intg[int(self.ch_intg)-1]
	c = self.th_state[int(self.ch_state)-1]

    	if (self.thermostate.get()==1):
	    self.Andersen(self)
	    self.check_andersen = '\nAndersen: ' + str(self.var_andersen)

	self.short_description = 'number of atoms: ' + self.natoms + '\nmass in amu: ' + self.mass + '\nrcut: ' + self.rcut + '\nbox length: ' + self.box + '\nnumber of steps: ' + self.nsteps + '\ntime interval: ' + self.dt + '\noutput frequency: ' + self.nprint + '\nrestart file: ' + self.restfile + '\ntrajectory file: ' + self.trajfile + '\nOutput file: ' + self.ergfile + '\nPotential: ' + a[1] + '\nIntegrator: ' + b[1] + '\nThermostate: ' + c[1] + self.check_andersen

	# Confirmation message
	if tkMessageBox.askyesno("Are you sure?", self.short_description):
	    self.quit()


