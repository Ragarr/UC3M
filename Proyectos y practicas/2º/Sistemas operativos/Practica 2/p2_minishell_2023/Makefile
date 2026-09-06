CC=gcc
FLAGS=-Wno-implicit-function-declaration
CFLAGS=-I.
OBJ = msh.o 
INC= parser.o
LIBS=-lparser -lpthread

%.o: %.c 
	$(CC) $(FLAGS) -c -o $@ $< $(CFLAGS)

msh: $(OBJ)
	$(CC) $(FLAGS) -L. -o $@ $< $(LIBS) -Wl,-rpath=.

clean:
	rm -f ./msh.o ./msh
