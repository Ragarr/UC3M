CC=gcc
FLAGS=-g -Wall -Werror
OBJ= queue bank
LIBS= -pthread

all:  $(OBJ)
	@echo "***************************"
	@echo "Compilation successfully!"
	@echo ""

queue: queue.c
	$(CC) -c queue.c

bank:	bank.c
	$(CC) $(CFLAGS) $(LIBS) -o bank  bank.c queue.c

load:
	ld -o bank queue.o

clean:
	rm -f bank *.o
	@echo "***************************"
	@echo "Deleted files!"
	@echo  ""

