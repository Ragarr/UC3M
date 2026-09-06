CC=gcc

CFLAGS=-Wall -Werror


%.o: %.c 
	$(CC) -c -o $@ $< $(CFLAGS)


all:	cat size ls

	
cat:	mywc.o
	$(CC) $(CFLAGS) -o mywc  mywc.o 

size:	myenv.o
	$(CC) $(CFLAGS)  -o myenv  myenv.o

ls: 	myls.o
	$(CC) $(CFLAGS)  -o myls myls.o


clean:
	rm -f mywc myls myenv
	rm *.o
