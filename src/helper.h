#include "mdsys.h"
#if defined(_OPENMP)
#include <omp.h>
#endif

/* helper function: apply minimum image convention */
//__attribute__((always_inline,pure))
double pbc(double x, const double boxby2, const double box);

/* helper function: zero out an array */

//__attribute__((always_inline))
void azzero(double *d, const int n);

void start_threads(mdsys_t *sys);
