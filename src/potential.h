#ifndef POTENTIAL_H
#define POTENTIAL_H
/* structure for potential table data */
struct _pot {
  int npoints;
  double *r;
  double *V;
  double *F;
  double rcut;
};
typedef struct _pot pot_t;

#endif
