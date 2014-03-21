# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS=-Wall -g -O3 -ffast-math -fomit-frame-pointer -fPIC
LDLIBS=-lm

# list of source files
SRC=evolution.c force.c helper.c list_cell.c 
VPATH=../src
OBJ=$(SRC:%.c=%.o)

default: ../libcoffeemd-serial.so

clean:
	rm -f *.mod *.o ../coffeemd-serial.x ../libcoffeemd-serial.so

# linker rule
coffeemd-serial.x: $(OBJ) md.o
	$(CC) -o $@ $(CFLAGS) $^ $(LDLIBS)

../libcoffeemd-serial.so: $(OBJ)
	$(CC) -o $@ $(CFLAGS) $^ -shared $(LDLIBS)

# compilation pattern rule for objects
%.o: %.c %.h
	$(CC) -c $(CFLAGS) $<
