#include "mdsys.h"
#include "stdlib.h"
#if defined(_OPENMP)
#include <omp.h>
#endif

double pbc(double x, const double boxby2, const double box);
double gauss(double sigmaa);
void azzero(double *d, const int n);
void start_threads(mdsys_t *sys);
