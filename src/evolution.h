#ifndef EVOLUTION_H
#define EVOLUTION_H

#include "mdsys.h"
#include "stdlib.h"
#include "force.h"

void first_step(mdsys_t *sys);
void final_step(mdsys_t *sys);
void ekin(mdsys_t *sys);
void velverlet(mdsys_t *sys);
void andersen(mdsys_t *sys);

#endif
