/* 
 * simple lennard-jones potential MD code with velocity verlet.
 * units: Length=Angstrom, Mass=amu; Energy=kcal
 */

#include "ljmd.h"
/* a few physical constants */
/* number of MD steps between cell list updates */
const int cellfreq=4;

extern double mvsq2e;

/* helper function: read a line and then return
   the first string with whitespace stripped off */
static int get_a_line(FILE *fp, char *buf)
{
  char tmp[BLEN], *ptr;

  /* read a line and cut of comments and blanks */
  if (fgets(tmp,BLEN,fp)) {
    int i;

    ptr=strchr(tmp,'#');
    if (ptr) *ptr= '\0';
    i=strlen(tmp); --i;
    while(isspace(tmp[i])) {
      tmp[i]='\0';
      --i;
    }
    ptr=tmp;
    while(isspace(*ptr)) {++ptr;}
    i=strlen(ptr);
    strcpy(buf,tmp);
    return 0;
  } else {
    perror("problem reading input");
    return -1;
  }
  return 0;
}
 
/* append data to output. */
static void output(mdsys_t *sys, FILE *erg, FILE *traj)
{
  int i,natoms;
  natoms=sys->natoms;
    
  //printf("% 8d % 20.8f % 20.8f % 20.8f % 20.8f\n", sys->nfi, sys->temp, sys->ekin, sys->epot, sys->ekin+sys->epot);
  fprintf(erg,"% 8d % 20.8f % 20.8f % 20.8f % 20.8f\n", sys->nfi, sys->temp, sys->ekin, sys->epot, sys->ekin+sys->epot);
  fprintf(traj,"%d\n nfi=%d etot=%20.8f\n", sys->natoms, sys->nfi, sys->ekin+sys->epot);
  for (i=0; i<natoms; ++i) {
    fprintf(traj, "Ar  %20.8f %20.8f %20.8f\n", sys->pos[i], sys->pos[natoms+i], sys->pos[2*natoms+i]);
  }
}


/* main */
int main(int argc, char **argv) 
{
  int nprint, i;
  char restfile[BLEN], trajfile[BLEN], ergfile[BLEN], line[BLEN];
  FILE *fp,*traj,*erg;
  mdsys_t sys;

#if defined(_OPENMP)
#pragma omp parallel
  {
    if(0 == omp_get_thread_num()) {
      sys.nthreads=omp_get_num_threads();
      printf("Running OpenMP version using %d threads\n", sys.nthreads);
    }
  }
#else
  sys.nthreads=1;
#endif

  /* read input file */
  if(get_a_line(stdin,line)) return 1;
  sys.natoms=atoi(line);
  if(get_a_line(stdin,line)) return 1;
  sys.mass=atof(line);
  if(get_a_line(stdin,line)) return 1;
  sys.epsilon=atof(line);
  if(get_a_line(stdin,line)) return 1;
  sys.sigma=atof(line);
  if(get_a_line(stdin,line)) return 1;
  sys.rcut=atof(line);
  if(get_a_line(stdin,line)) return 1;
  sys.box=atof(line);
  if(get_a_line(stdin,restfile)) return 1;
  if(get_a_line(stdin,trajfile)) return 1;
  if(get_a_line(stdin,ergfile)) return 1;
  if(get_a_line(stdin,line)) return 1;
  sys.nsteps=atoi(line);
  if(get_a_line(stdin,line)) return 1;
  sys.dt=atof(line);
  if(get_a_line(stdin,line)) return 1;
  nprint=atoi(line);

  /* allocate memory */
  sys.pos=(double *)malloc(3*sys.natoms*sizeof(double));
  sys.vel=(double *)malloc(3*sys.natoms*sizeof(double));
  sys.frc=(double *)malloc(sys.nthreads*3*sys.natoms*sizeof(double));

  /* read restart */
  fp=fopen(restfile,"r");
  if(fp) {
    int natoms;
    natoms=sys.natoms;
        
    for (i=0; i<natoms; ++i) {
      fscanf(fp,"%lf%lf%lf",sys.pos+i, sys.pos+natoms+i, sys.pos+2*natoms+i);
    }
    for (i=0; i<natoms; ++i) {
      fscanf(fp,"%lf%lf%lf",sys.vel+i, sys.vel+natoms+i, sys.vel+2*natoms+i);
    }
    fclose(fp);
    azzero(sys.frc, 3*sys.nthreads*sys.natoms);
  } else {
    perror("cannot read restart file");
    return 3;
  }

  /* initialize forces and energies.*/
  sys.nfi=0;
  sys.clist=NULL;
  sys.plist=NULL;
  updcells(&sys);
  force(&sys);
  ekin(&sys);
    
  erg=fopen(ergfile,"w");
  traj=fopen(trajfile,"w");

  printf("Starting simulation with %d atoms for %d steps.\n",sys.natoms, sys.nsteps);
  printf("     NFI            TEMP            EKIN                 EPOT              ETOT\n");
  output(&sys, erg, traj);

  /**************************************************/
  /* main MD loop */
  for(sys.nfi=1; sys.nfi <= sys.nsteps; ++sys.nfi) {

    /* write output, if requested */
    if ((sys.nfi % nprint) == 0) 
      output(&sys, erg, traj);

    /* propagate system and recompute energies */
    velverlet(&sys);
    ekin(&sys);

    /* update cell list */
    if ((sys.nfi % cellfreq) == 0) 
      updcells(&sys);
  }
  /**************************************************/

  /* clean up: close files, free memory */
  printf("Simulation Done.\n");
  fclose(erg);
  fclose(traj);
  free(sys.pos);
  free(sys.vel);
  free(sys.frc);
  free_cell_list(&sys);

  return 0;
}
