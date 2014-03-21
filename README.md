CoffeeMD
========

Molecular Dynamics code in python with c bindings.

This program is based on the original c code from Axel Kohlmeyer, 
[ljmd-c](https://github.com/akohlmey/ljmd-c) and refactored to
add python bindings. It is distributed under the terms of the GNU
General Public License.

Introduction
------------

This software was made during the ICTP [Workshop on Advanced Techniques 
for Scientific Programming and Management of Open Source Software 
Packages](http://cdsagenda5.ictp.it/full_display.php?ida=a13190), and
its main idea is to be able to *build* molecular dynamics simulation with
the flexibility that Python gives, leaving the hard math to c. Here, 
building means that the c library has the minimum it should have in order
to be able to run it with Python without losing much performance.

Making CoffeeMD
---------------

To compile the dynamic loading libraries, just type 

    $ make

on the parent directory. This will make both the parallel and the
serial library.

Input (in Python)
-----------------

The class mdsys_t defined in python/md_classes.py directory can be
used to input parameters in 3 different ways:

- On the screen, with the method screen_input
- Through a file, with the method file_input (see input examples *.inp
  in the examples folder)
- Through a GUI interface, with the method gui_input

The class Potential in python/potential.py can be used to create
different LUTs. There are predefined ones with LennardJones and
Morse potentials, and a HomeMade potential that takes as input
the functions for the force and the potential.

Algorithm Capabilities (in c)
-----------------------------

The c code takes a LUT of the potential and integrates it with a
typical [velocity verlet algorithm](http://en.wikipedia.org/wiki/Verlet_integration) in the microcanonical
ensemble. To reproduce the canonical ensamble, an Andersen
thermostat [Frenkel] is available as well.

[Frenkel] Understanding Molecular Simulation: From Algorithms to Applications


Output (in Python)
------------------

The output to file is managed through the method output in the
class mdsys_t. There is also a Result class in file python/result.py
that has the method graph, which makes plot of the energy.

General Implementation (in Python)
----------------------------------

The file python/main.py is a general implementation in Python that 
can be used as a template to make your own implementations of the code.

It accepts command line arguments when running it, to trigger the 
different input modes:

- screen mode:

    $ ./main.py

- file mode:

    $ ./main.py -f [--file] <filename.inp>

- GUI mode:

    $ ./main.py -g [--gui]

- for help, type:

    $ ./main.py -h [--help]
