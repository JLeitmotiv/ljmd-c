#ifndef EVOLUTION_H
#define EVOLUTION_H
#include "mdsys.h"
extern inline double gauss(double sigmaa);
void first_step(mdsys_t *sys);
void final_step(mdsys_t *sys);
void ekin(mdsys_t *sys);
void andersen(mdsys_t *sys);
#endif
