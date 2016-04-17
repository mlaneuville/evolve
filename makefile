BIN = evolve
OBJ = main.o config.o
CC = g++
FLAGS = -lyaml-cpp 

$(BIN): $(OBJ) *.hpp modules/*.hpp
	$(CC) -o $(BIN) $(OBJ) $(FLAGS)

$(OBJ): *.hpp

.cpp.o:
	$(CC) -c $*.cpp

clean:
	rm -f evolve *.o

all: $(BIN)

