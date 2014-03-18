"""
This file creates a structure that has the elements
common to c object mdsys, the base one in which we
have all the info. Here is the mdsys structure and
how it is defined:

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
"""
