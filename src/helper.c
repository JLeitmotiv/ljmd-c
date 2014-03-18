__attribute__((always_inline,pure))
static double pbc(double x, const double boxby2, const double box)
{
  while (x >  boxby2) x -= box;
  while (x < -boxby2) x += box;
  return x;
}

__attribute__((always_inline))
static void azzero(double *d, const int n)
{
  int i;
  for (i=0; i<n; ++i) {
    d[i]=0.0;
  }
}
