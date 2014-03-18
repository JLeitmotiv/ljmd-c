#ifndef CELL_H
#define CELL_H
/* structure for cell-list data */
struct _cell {
  int natoms;                 /* number of atoms in this cell */
  int owner;                  /* task/thread id that owns this cell */
  int *idxlist;               /* list of atom indices */
};
typedef struct _cell cell_t;

#endif
