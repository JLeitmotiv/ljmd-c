#include "velverlet.h"

void velverlet(mdsys_t *sys)
{
  /* first part: propagate velocities by half and positions by full step */
  first_step(sys);
  /* compute forces and potential energy */
  force(sys);
  /* second part: propagate velocities by another half step */
  final_step(sys);
}


