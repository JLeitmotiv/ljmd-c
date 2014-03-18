#include "mdsys.h"

const double mvsq2e=2390.05736153349; /* m*v^2 in kcal/mol */

static void first_step(mdsys_t *sys);
static void final_step(mdsys_t *sys);
