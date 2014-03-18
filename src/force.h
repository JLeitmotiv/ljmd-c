#include "mdsys.h"

void force(mdsys_t *sys);
extern inline double pbc(double x, const double boxby2, const double box);
extern inline void azzero(double *d, const int n);

