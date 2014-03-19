#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mdsys.h"

extern inline double pbc(double x, const double boxby2, const double box);
void free_cell_list(mdsys_t *sys);
void updcells(mdsys_t *sys);
