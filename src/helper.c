#include "stdlib.h" 
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
double gauss(double sigmaa)
{
   int r=2;
   double v1,v2,l;
   while(r>1){
    v1=2*(rand()/(RAND_MAX))-1;
    v2=2*(rand()/(RAND_MAX))-1;
    r=v1*v1+v2*v2;
   }
   l=v1*pow(-2*log(r)/r,0.5);
   l=sigmaa*l;
   return l;
}


