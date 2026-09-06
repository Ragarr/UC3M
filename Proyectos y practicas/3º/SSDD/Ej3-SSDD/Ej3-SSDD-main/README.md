# Ej3-SSDD


## Instalacion y uso de RPCGEN
1) Hay que tener instalado los siguientes paquetes:
             libtirpc-common
             libtirpc-dev 
             libtirpc3 
             rpcsvc-proto 
             rpcbind 

2) Para compilar el ejemplo suma.x:


`rpcgen -NMa suma.x`


```          
Siendo suma.x:

        program SUMAR {
            version SUMAVER {
                    int  SUMA(int a, int b) = 1;
                    int RESTA(int a, int b) = 2;
            } = 1;
    } = 99;
```


3) Editar el Makefile.suma y cambiar:


```
CFLAGS += -g -I/usr/include/tirpc
LDLIBS += -lnsl -lpthread -ldl -ltirpc
```


4) Compilar el ejemplo con make -f Makefile.suma

5)  Arrancar rpcbind:

```
sudo mkdir -p /run/sendsigs.omit.d/
sudo /etc/init.d/rpcbind restart
```


export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
export HOST=localhost