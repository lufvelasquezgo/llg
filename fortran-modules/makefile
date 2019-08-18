all: build run

build:
	gfortran -c functions.f90 -o functions.mod
	gfortran functions.f90 main.f90 -o main

run:
	./main

test:
	funit functions

clean:
	rm -rf *.mod *.o main
	funit --clean