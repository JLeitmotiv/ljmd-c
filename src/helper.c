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

__attribute__((always_inline))
double gauss(double var)
{
   double r=2.0;
   double v1,v2,l;
   while(r>1){
    v1=(float)rand()/(RAND_MAX);
    v2=(float)rand()/(RAND_MAX);
    v1=2*v1-1;
    v2=2*v2-1;
    r=v1*v1+v2*v2;
   }
   l=v1*pow(-2*log(r)/r,0.5);
   l=var*l;
   return l;
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
