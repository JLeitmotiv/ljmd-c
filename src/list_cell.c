#include "list_cell.h"

/* ratio between cutoff radius and length of a cell */
const double cellrat=2.0;


/* release cell list storage */
void free_cell_list(mdsys_t *sys)
{
  int i;
    
  if (sys->clist == NULL) 
    return;
    
  for (i=0; i < sys->ncell; ++i) {
    free(sys->clist[i].idxlist);
  }
    
  free(sys->clist);
  sys->clist = NULL;
  sys->ncell = 0;
}

/* build and update cell list */
void updcells(mdsys_t *sys)
{
  int i, ngrid, ncell, npair, midx, natoms;
  double delta, boxby2, boxoffs;
  boxby2 = 0.5 * sys->box;
  natoms = sys->natoms;
        
  if (sys->clist == NULL) {
    int nidx;
        
    ngrid  = floor(cellrat * sys->box / sys->rcut);
    ncell  = ngrid*ngrid*ngrid;
    delta  = sys->box / ngrid;
    boxoffs= boxby2 - 0.5*delta;
        
    sys->delta = delta;
    sys->ngrid = ngrid;
    sys->ncell = ncell;

    /* allocate cell list storage */
    sys->clist = (cell_t *) malloc(ncell*sizeof(cell_t));
    sys->plist = (int *) malloc(2*ncell*ncell*sizeof(int));

    /* allocate index lists within cell. cell density < 2x avg. density */
    nidx = 2*natoms / ncell + 2;
    nidx = ((nidx/2) + 1) * 2;
    sys->nidx = nidx;
    for (i=0; i<ncell; ++i) {
      sys->clist[i].idxlist = (int *) malloc(nidx*sizeof(int));
    }

    /* build cell pair list, assuming newtons 3rd law. */
    npair = 0;
    for (i=0; i < ncell-1; ++i) {
      int j,k;
      double x1,y1,z1;
            
      k  = i/ngrid/ngrid;
      x1 = k*delta - boxoffs;
      y1 = ((i-(k*ngrid*ngrid))/ngrid)*delta - boxoffs;
      z1 = (i % ngrid)*delta - boxoffs;

      for (j=i+1; j<ncell; ++j) {
	double x2,y2,z2,rx,ry,rz;
                
	k  = j/ngrid/ngrid;
	x2 = k*delta - boxoffs;
	y2 = ((j-(k*ngrid*ngrid))/ngrid)*delta - boxoffs;
	z2 = (j % ngrid)*delta - boxoffs;

	rx=pbc(x1 - x2, boxby2, sys->box);
	ry=pbc(y1 - y2, boxby2, sys->box);
	rz=pbc(z1 - z2, boxby2, sys->box);

	/* check for cells on a line that are too far apart */
	if (fabs(rx) > sys->rcut+delta) continue;
	if (fabs(ry) > sys->rcut+delta) continue;
	if (fabs(rz) > sys->rcut+delta) continue;

	/* check for cells in a plane that are too far apart */
	if (sqrt(rx*rx+ry*ry) > (sys->rcut+sqrt(2.0)*delta)) continue;
	if (sqrt(rx*rx+rz*rz) > (sys->rcut+sqrt(2.0)*delta)) continue;
	if (sqrt(ry*ry+rz*rz) > (sys->rcut+sqrt(2.0)*delta)) continue;

	/* other cells that are too far apart */
	if (sqrt(rx*rx + ry*ry + rz*rz) > (sqrt(3.0)*delta+sys->rcut)) continue;
                
	/* cells are close enough. add to list */
	sys->plist[2*npair  ] = i;
	sys->plist[2*npair+1] = j;
	++npair;
      }
    }
    sys->npair = npair;
    printf("Cell list has %dx%dx%d=%d cells with %d/%d pairs and "
	   "%d atoms/celllist.\n", ngrid, ngrid, ngrid, sys->ncell, 
	   sys->npair, ncell*(ncell-1)/2, nidx);
  }

  /* reset cell list and sort atoms into cells */
  ncell=sys->ncell;
  delta=sys->delta;
  ngrid=sys->ngrid;
    
  for (i=0; i < sys->ncell; ++i) {
    sys->clist[i].natoms=0;
  }

  boxoffs= boxby2 - 0.5*delta;
  midx=0;
  for (i=0; i < natoms; ++i) {
    int idx,j,k,m,n;
        
    k=floor((pbc(sys->pos[i], boxby2, sys->box)+boxby2)/delta);
    m=floor((pbc(sys->pos[natoms + i], boxby2, sys->box)+boxby2)/delta);
    n=floor((pbc(sys->pos[2*natoms + i], boxby2, sys->box)+boxby2)/delta);
    j = ngrid*ngrid*k+ngrid*m+n;

    idx = sys->clist[j].natoms;
    sys->clist[j].idxlist[idx]=i;
    ++idx;
    sys->clist[j].natoms = idx;
    if (idx > midx) midx=idx;
  }
  if (midx > sys->nidx) {
    printf("overflow in cell list: %d/%d atoms/cells.\n", midx, sys->nidx);
    exit(1);
  }
  return;
}
