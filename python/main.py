from result import Result
from class_and_funtion import *

###--- variables will be comes from program
### this import is valid for only data file
import sys
import numpy as np

if __name__ == "__main__":
   mdsys=mdsys_t()
   if len(sys.argv)==1:
      screen_input(mdsys)
   else:
      file_input(mdsys)
   grow_array(mdsys)
   read_restart(mdsys)
   printt=prints(mdsys)

    ######super looop ######
    if (mdsys.nfi%mdsys.nprint==0):
        printt.print_output(mdsys)

# fetch the data from file 
(time, temp, Ekin, Epot, Etot) = np.loadtxt(mdsys.thermo_output, unpack = True)
###--- the variables are loaded
     result = Result(time,temp,Ekin,Epot,Etot)

result.graph()
