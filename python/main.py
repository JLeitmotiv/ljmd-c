from result import Result

###--- variables will be comes from program
### this import is valid for only data file
import numpy as np

filename = 'argon_108.dat'


# fetch the data from file 
(time, temp, Ekin, Epot, Etot) = np.loadtxt(filename, unpack = True)
###--- the variables are loaded

result = Result(time, temp, Ekin, Epot, Etot)

result.graph()
