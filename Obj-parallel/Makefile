# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS=-fopenmp -Wall -g -O3 -ffast-math -fomit-frame-pointer -fPIC
LDLIBS=-lm

# list of source files
SRC=evolution.c force.c helper.c list_cell.c
VPATH=../src
OBJ=$(SRC:%.c=%.o)

default: ../libcoffeemd-parallel.so

clean:
	rm -f *.mod *.o ../coffeemd-parallel.x ../libcoffeemd-parallel.so

# linker rule
coffeemd-parallel.x: $(OBJ) md.o
	$(CC) -o ../$@ $(CFLAGS) $^ $(LDLIBS)

../libicoffeemd-parallel.so: $(OBJ)
	$(CC) -o $@ $(CFLAGS) $^ -shared $(LDLIBS)

# compilation pattern rule for objects
%.o: %.c
	$(CC) -c $(CFLAGS) $<

%.c: %.h
