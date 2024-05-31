CC = gcc
CFLAGS = -Wall -Wextra  -g
LDFLAGS = -L. -llogger -lm -lpthread

server: server.c
	$(CC) $(CFLAGS) -o server server.c $(LDFLAGS)

.PHONY: clean
clean:
	rm -f server *.o *.so *.a