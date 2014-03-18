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


"""

from ctypes import *

class cell_t(Structure):
    _fields_ = [("natoms", c_int),
                ("owner", c_int),
                ("idxlist", POINTER(c_int))]

class mdsys(Structure):
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
