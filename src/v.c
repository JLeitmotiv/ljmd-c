# 1 "velverlet.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "velverlet.c"
# 1 "velverlet.h" 1
# 1 "evolution.h" 1
# 1 "mdsys.h" 1



# 1 "cell.h" 1



struct _cell {
  int natoms;
  int owner;
  int *idxlist;
};
typedef struct _cell cell_t;
# 5 "mdsys.h" 2



struct _mdsys {
  double dt, mass, epsilon, sigma, box, rcut;
  double ekin, epot, temp, _pad1;
  double *pos, *vel, *frc;
  cell_t *clist;
  int *plist, _pad2;
  int natoms, nfi, nsteps, nthreads;
  int ngrid, ncell, npair, nidx;
  double delta;
};
typedef struct _mdsys mdsys_t;
# 2 "evolution.h" 2

const double mvsq2e=2390.05736153349;

static void first_step(mdsys_t *sys);
static void final_step(mdsys_t *sys,);
# 2 "velverlet.h" 2


static void velverlet(mdsys_t *sys);
# 2 "velverlet.c" 2

static void velverlet(mdsys_t *sys)
{

  first_step(sys);

  force(sys);

  final_step(sys);
}
