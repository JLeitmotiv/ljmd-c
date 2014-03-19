# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS=-fopenmp -g -Wall -O3 -ffast-math -fomit-frame-pointer -fPIC
LDLIBS=-lm

# list of source files
SRC=evolution.c force.c helper.c list_cell.c velverlet.c
VPATH=../src
OBJ=$(SRC:%.c=%.o)

default: ../libljmd-parallel.so ../ljmd-parallel.x

clean:
	rm -f *.mod *.o ../ljmd-parallel.x ../libljmd-parallel.so

# linker rule
../ljmd-parallel.x: $(OBJ) ljmd.o
	$(CC) -o $@ $(CFLAGS) $^ $(LDLIBS)

../libljmd-parallel.so: $(OBJ)
	$(CC) -o $@ $(CFLAGS) $^ -shared $(LDLIBS)

# compilation pattern rule for objects
%.o: %.c
	$(CC) -c $(CFLAGS) $<
