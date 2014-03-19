#ifndef MDSYS_H
#define MDSYS_H

#include "cell.h"

/* structure to hold the complete information 
 * about the MD system */
struct _mdsys {
  double dt, mass, epsilon, sigma, box, rcut;
  double ekin, epot, tempin, _pad1,tempout,nu,var_andersen;
  double *pos, *vel, *frc;
  cell_t *clist;
  int *plist, _pad2;
  int natoms, nfi, nsteps, nthreads;
  int ngrid, ncell, npair, nidx;
  double delta;
};
typedef struct _mdsys mdsys_t;

#endif
