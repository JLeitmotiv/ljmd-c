#ifndef MDSYS_H
#define MDSYS_H

#include "cell.h"
#include "potential.h"

/* structure to hold the complete information 
 * about the MD system */
struct _mdsys {
  cell_t *clist;
  pot_t ptable;
  double dt, mass, box;
  double ekin, epot, temp, _pad1;
  double *pos, *vel, *frc;
  int *plist, _pad2;
  int natoms, nfi, nsteps, nthreads;
  int ngrid, ncell, npair, nidx;
  double delta;
};
typedef struct _mdsys mdsys_t;

#endif
