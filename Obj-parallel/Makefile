# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS=-fopenmp -Wall -g -O3 -ffast-math -fomit-frame-pointer
LDLIBS=-lm

# list of source files
SRC=ljmd.c
VPATH=../src
OBJ=$(SRC:%.c=%.o)

default: ../ljmd-parallel.x
library: ../libljmd-parallel.so

clean:
	rm -f *.mod *.o ../ljmd-parallel.x

# linker rule
../ljmd-parallel.x: $(OBJ)
	$(CC) -o $@ $(CFLAGS) $^ $(LDLIBS)

# compilation pattern rule for objects
%.o: %.c
	$(CC) -c $(CFLAGS) $<

../libljmd-parallel.so: ljmd.c
	$(CC) $(CFLAGS) -fPIC -shared $<

# dependencies
ljmd.o: ljmd.c
