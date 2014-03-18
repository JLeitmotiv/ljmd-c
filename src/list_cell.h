#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mdsys.h"

/* ratio between cutoff radius and length of a cell */
const double cellrat=2.0;

static void free_cell_list(mdsys_t *sys);
static void updcells(mdsys_t *sys);

