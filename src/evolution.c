#include "evolution.h"

double mvsq2e=2390.05736153349; /* m*v^2 in kcal/mol */
const double kboltz=0.0019872067;

void first_step(mdsys_t *sys)
{
  int i;
  double dtmf;
  dtmf = 0.5*sys->dt / mvsq2e / sys->mass;

  for (i=0; i<3*sys->natoms; ++i) {
    sys->vel[i] += dtmf * sys->frc[i];
    sys->pos[i] += sys->dt*sys->vel[i];
  }
}  

void final_step(mdsys_t *sys)
{
  int i;
  double dtmf;
  dtmf = 0.5*sys->dt / mvsq2e / sys->mass;
  for (i=0; i<3*sys->natoms; ++i) {
    sys->vel[i] += dtmf * sys->frc[i];
  }
}

/* compute kinetic energy */
void ekin(mdsys_t *sys)
{   
  int i;

  sys->ekin=0.0;
  for (i=0; i< 3*sys->natoms; ++i) {
    sys->ekin += sys->vel[i]*sys->vel[i];
  }
  sys->ekin *= 0.5*mvsq2e*sys->mass;
  sys->tempout  = 2.0*sys->ekin/(3.0*sys->natoms-3.0)/kboltz;
}
void andersen(mdsys_t *sys)
{
  int i;
  double r;
  for(i =0;i<3*sys->natoms; ++i){
      r = (float) rand()/(RAND_MAX);
      if(r<sys->nu*sys->dt){
        sys->vel[i]=gauss(sys->var_andersen);
      }
  }
}
void velverlet(mdsys_t *sys)
{
  /* first part: propagate velocities by half and positions by full step */
  first_step(sys);
  /* compute forces and potential energy */
  force(sys);
  /* second part: propagate velocities by another half step */
  final_step(sys);
}
