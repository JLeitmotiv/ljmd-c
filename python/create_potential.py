import numpy as np
from math import exp

class Potential(object):
    def __init__(self, rcut, npoints):
        """
        Constructor: sets the value of the cutoff rcut and the number
        of points in the interpolation
        """
        self.rcut = rcut
        self.npoints = npoints
        self.create_table()

    def create_table(self):
        """
        This method creates a table, given the functions self.V_r and self.F_r
        If the potential for r = 0 is well designed, it is inserted.
        """
        self.r = np.linspace(self.rcut/self.npoints,self.rcut,self.npoints)
        self.V = np.zeros(self.npoints)
        self.F = np.zeros(self.npoints)
        for i in range(len(self.r)):
            p = self.r[i]
            self.V[i] = self.V_r(p)
            self.F[i] = self.F_r(p)
        try:
            np.insert(self.V, 0, self.V_r(0))
            np.insert(self.F, 0, self.F_r(0))
        except ZeroDivisionError:
            print "Warning: Couldn't evaluate the potential for r = 0"


class LennardJones(Potential):
    """
    This class defines a Lennard-Jones potential
    """
    def __init__(self, rcut, npoints, sigma, epsilon):
        """
        Constructor: makes F_r and V_r and builds the table with
        typical LJ parameters
        """
        [self.V_r, self.F_r] = self.interaction(epsilon, sigma)
        Potential.__init__(self, rcut, npoints)
 
    def interaction(self, e, s):
	"""
        Makes F_r and V_r
        """ 
        v = lambda r: 4 * e * ( (s/r)**12 - (s/r)**6 )
	f = lambda r: 4 * e * ( 12 * (s/r)**12 - 6 *(s/r)**6 ) / r
        return v, f
                                      

class Morse(Potential):
    """
    This class defines a Morsev potential
    """
    def __init__(self, rcut, npoints, d, a, re):
        """
        Constructor: makes F_r and V_r and builds the table with
        typical Morse parameters
        """
        [self.V_r, self.F_r] = self.interaction(d, a, re)
        Potential.__init__(self, rcut, npoints)
 
    def interaction(self, d, a, re):
	"""
        Makes F_r and V_r
        """ 
	v = lambda r: d * ( ( 1-exp(- a * (r - re) ) ) ** 2 - 1 )
	f = lambda r: 2 * a * d * exp(a * (re - r)) * (-1 + exp(a * (re - r)))
        return v, f

class HomeMade(Potential):
    """
    This class is for any potential created on the fly
    """ 
    def __init__(self, rcut, npoints, V_r, F_r):
        """
        Constructor: the potential and force function need to be passed
        """
        self.V_r = V_r
        self.F_r = F_r
        Potential.__init__(self, rcut, npoints)

if __name__ == "__main__":
    """
    Just run some examples and check if everything makes sense
    """
    import pylab as pl

    LJPot = LennardJones(8.5, 10000, 3.405, 0.2379)
    pl.plot(LJPot.r, LJPot.V)
    pl.ylim(-0.5, 1)
    pl.ylabel("Potential")
    pl.xlabel("Distance")
    pl.show()

    MPot = Morse(5.5, 1000, 1.0, 1.0, 1.0)
    pl.plot(MPot.r, MPot.V)
    pl.ylim(-2, 2)
    pl.ylabel("Potential")
    pl.xlabel("Distance")
    pl.show()

    #We must define our own functions if we want to use HomeMade
    V_Spring = lambda r: 0.5 * r**2
    F_Spring = lambda r: -r

    SPot = HomeMade(5.5, 1000, V_Spring, F_Spring)
    pl.plot(SPot.r, SPot.V)
    pl.ylim(0, 0.5*6*6)
    pl.ylabel("Potential")
    pl.xlabel("Distance")
    pl.show()
