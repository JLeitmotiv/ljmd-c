/* 
 * simple lennard-jones potential MD code with velocity verlet.
 * units: Length=Angstrom, Mass=amu; Energy=kcal
 */

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <math.h>

#include "mdsys.h"
#include "evolution.h"
#include "force.h"
#include "list_cell.h"
#if defined(_OPENMP)
#include <omp.h>
#endif

/* generic file- or pathname buffer length */
#define BLEN 200

static int get_a_line(FILE *fp, char *buf);
static void output(mdsys_t *sys, FILE *erg, FILE *traj);
