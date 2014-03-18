#include "evolution.h"

static void first_step(mdsys_t *sys)
{
  int i;
  double dtmf;
  dtmf = 0.5*sys->dt / mvsq2e / sys->mass;

  for (i=0; i<3*sys->natoms; ++i) {
    sys->vel[i] += dtmf * sys->frc[i];
    sys->pos[i] += sys->dt*sys->vel[i];
  }
}  

static void final_step(mdsys_t *sys)
{
  int i;
  double dtmf;
  dtmf = 0.5*sys->dt / mvsq2e / sys->mass;

  for (i=0; i<3*sys->natoms; ++i) {
    sys->vel[i] += dtmf * sys->frc[i];
  }
}
