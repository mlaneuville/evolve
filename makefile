BIN = evolve
OBJ = main.o config.o
CC = g++
FLAGS = -lyaml-cpp 

$(BIN): $(OBJ) *.hpp modules/*.hpp
	$(CC) -o $(BIN) $(OBJ) $(FLAGS)

$(OBJ): *.hpp

.cpp.o:
	$(CC) -c $*.cpp -std=c++11

clean:
	rm -f evolve *.o

all: $(BIN)

paper: prep configs runs figs

prep:
	rm -f evolve *.o
	make evolve
	rm -rf paper
	mkdir -p paper/runs
	mkdir -p paper/figs

configs:
	python generate_initial_conditions.py -f paper/runs/init -n 8 -m man-ox -v 0.20

runs:
	python run_multi_config.py -f paper/runs/init

figs:
	python processing/generate_single_plot.py paper/runs/init/*.txt -c Atmosphere0 -c CCrust2  \
																	-l 'Atmosphere' -l 'Continents' \
																	-e -o paper/figs/FIG3A.eps -n '(a)'
	python processing/generate_single_plot.py paper/runs/init/*.txt -c LMantle2 -c UMantle2 \
                                            					    -l 'Lower mantle'  -l 'Upper mantle'  \
                                            						-e  -o paper/figs/FIG3B.eps -n '(b)'
	python processing/generate_single_plot.py paper/runs/init/*.txt -c Oceans1     -e  -o paper/figs/FIG3C.eps -n '(c)'
	python processing/generate_single_plot.py paper/runs/init/*.txt -c Oceans2         -o paper/figs/FIG3D.eps -n '(d)'

.PHONY: clean paper prep configs runs figs
