/* helper function: apply minimum image convention */
//__attribute__((always_inline,pure))
static double pbc(double x, const double boxby2, const double box);

/* helper function: zero out an array */

//__attribute__((always_inline))
static void azzero(double *d, const int n);
