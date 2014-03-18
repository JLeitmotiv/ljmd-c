# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS=-Wall -g -O3 -ffast-math -fomit-frame-pointer -fPIC
LDLIBS=-lm

# list of source files
SRC=evolution.c force.c helper.c list_cell.c velverlet.c
VPATH=../src
OBJ=$(SRC:%.c=%.o)

default: ../libljmd-serial.so ../ljmd-serial.x

clean:
	rm -f *.mod *.o ../ljmd-serial.x ../libljmd-serial.so

# linker rule
../ljmd-serial.x: $(OBJ) ljmd.o
	$(CC) -o $@ $(CFLAGS) $^ $(LDLIBS)

../libljmd-serial.so: $(OBJ)
	$(CC) -o $@ $(CFLAGS) $^ -shared $(LDLIBS)

# compilation pattern rule for objects
%.o: %.c
	$(CC) -c $(CFLAGS) $<
