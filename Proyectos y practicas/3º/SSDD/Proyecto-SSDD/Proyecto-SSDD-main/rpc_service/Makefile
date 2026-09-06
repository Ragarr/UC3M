CC=gcc
RPCGEN=rpcgen

# Flags de compilación
CFLAGS=-fPIC -g -I/usr/include/tirpc -I.
LDFLAGS=-L/usr/lib64 -ltirpc -lnsl -lpthread -ldl 
RPCFLAGS= -NMa

# Fuentes y objetos
RPCSRC=rpc_logger.x
SOURCES_CLNT=rpc_logger_clnt.c
SOURCES_SVC=rpc_logger_svc.c
OBJECTS_CLNT=$(SOURCES_CLNT:.c=.o)
OBJECTS_SVC=$(SOURCES_SVC:.c=.o)

all: liblogger.so rpc_logger_server

# Genera los archivos de cliente y servidor RPC
$(SOURCES_CLNT) $(SOURCES_SVC): $(RPCSRC)

# Objetivos de compilación
liblogger.so: logger.o $(OBJECTS_CLNT) $(OBJECTS_XDR)
	$(CC) -shared -o $@ $^ $(LDFLAGS)

rpc_logger_server: rpc_logger_server.o $(OBJECTS_SVC) $(OBJECTS_XDR)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Regla genérica para compilar C a objetos
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Limpieza de archivos generados
clean:
	rm -f *.o rpc_logger_server liblogger.so

.PHONY: all clean
