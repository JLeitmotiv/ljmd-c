# -*- Makefile -*-
SHELL=/bin/sh
############################################

default: serial parallel 

serial parallel:
	$(MAKE) $(MFLAGS) -C Obj-$@

clean:
	$(MAKE) $(MFLAGS) -C Obj-serial clean
	$(MAKE) $(MFLAGS) -C Obj-parallel clean
