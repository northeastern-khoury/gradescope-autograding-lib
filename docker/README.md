# CS3650 Gradescope Base Image
## Purpose
This repository defines the build process for the base autograder image for CS 3650, Computer Systems.
No autograding code is provided as part of this image.
To build an autograder, create a separate repo with the autograder code where the Dockerfile's FROM directive points to <insert chosen name here>. 

## Tooling
The following toolchains are provided:
 - GCC
 - Clang

The following utilities are provided:
 - Valgrind

## Maintainers
Tariq Sachleben, Khoury Systems <t.sachleben@northeastern.edu>
