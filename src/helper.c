#include "helper.h"
__attribute__((always_inline,pure))
double pbc(double x, const double boxby2, const double box)
{
  while (x >  boxby2) x -= box;
  while (x < -boxby2) x += box;
  return x;
}

__attribute__((always_inline))
void azzero(double *d, const int n)
{
  int i;
  for (i=0; i<n; ++i) {
    d[i]=0.0;
  }
}

void start_threads(mdsys_t *sys)
{
#if defined(_OPENMP)
#pragma omp parallel
  {
    if(0 == omp_get_thread_num()) {
      sys->nthreads=omp_get_num_threads();
    }
  }
#else
  sys->nthreads=1;
#endif
}
