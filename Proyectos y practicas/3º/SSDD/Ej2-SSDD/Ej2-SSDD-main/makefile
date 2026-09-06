CC = gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11 
LDFLAGS = -L. -lclaves -lpthread -lrt 

SERVER_SRC = servidor.c
CLIENT_SRC = cliente.c
LIB_SRC = claves.c
LIB_HEADER = claves.h

SERVER_OBJ = $(SERVER_SRC:.c=.o)
CLIENT_OBJ = $(CLIENT_SRC:.c=.o)
LIB_OBJ = $(LIB_SRC:.c=.o)

SERVER_BIN = servidor
CLIENT_BIN = cliente
LIBRARY = libclaves.so

.PHONY: all clean

all: $(LIBRARY) $(SERVER_BIN) $(CLIENT_BIN)  clean

$(SERVER_BIN): $(SERVER_OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(CLIENT_BIN): $(CLIENT_OBJ) $(LIBRARY)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

$(LIBRARY): $(LIB_OBJ)
	$(CC) -shared -o $@ $^

%.o: %.c $(LIB_HEADER)
	$(CC) $(CFLAGS) -fPIC -c -o $@ $<

clean:
	rm -f *.o