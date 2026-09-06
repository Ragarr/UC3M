El propósito de este documento es aclararse con varios conceptos teóricos y acumular todas las putas
LIBRERIAS:
```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
```


# NOTA: 
los procesos tienen una tabla de descriptores de ficheros, que por defecto se corresponden 0
con entrada estandar (teclado), 1 salida estandar (pantalla), 2 salida de errores estandar (pantalla)
Dichos descriptores de ficheros de cada proceso realmente son el índice de la tabla interna 
del sistema operativo, que comunica con teclado y pantalla.
Al hacer fork(), SE COPIA LA TABLA con todos los descriptores de ficheros del padre. Es decir, que
si el padre tenia abierto un fichero watafac.txt, el hijo tambien y con el MISMO descriptor de fichero
(que es realmente el indice de la tabla)

# TEORIA: 
si queremos modificar la tabla de descriptores de fichero de nuestro proceso debemos usar 
2 funciones: close() y dup().

- close(int fd): esta función elimina la entrada en la tabla del el fichero de la posición "fd".
Asi se desvincula el archivo del0 proceso. Usado con open() se puede modificar el archivo asociado
a un descriptor y poner por ejemplo en la salida estandar de errores un archivo .txt.

- dup(int fd): esta función busca el siguiente hueco disponible de la tabla de descriptores de 
fichero para un nuevo vinculo. Este vinculo sera con el MISMO archivo de la posicion "fd" en la tabla.
Es decir, que ahora tenemos 2 descriptores distintos y vinculados al mismo archivo.

## 1. Pipes: 
Una tubería es un fichero especial, que al ser creada con pipe(), reserva 2 entradas de la 
tabla (con 2 fd), una para lectura y otra para escritura. Dentro de un mismo proceso NO sirve para 
nada, sino que sirve para comunicar procesos emparentados: uno escribe (en entrada estandar), y el 
otro lee (en salida estandar). Los pipes tienen 4 fases:

CREACION:       
```
                int p1[2] ;
                pipe(p1) ;  //p1[0] == lectura, p1[1] == escritura
```
FORK:
```
fork()      // al crear un hijo, se crean 2 pipes (uno en padre y otro en hijo)
```

REDIRECCION:
```            
                if (0!=pid) {   // estamos en proceso padre
                close(1);
                dup(p1[1]);     // redirigimos la salida estandar del padre, para enviarsela al hijo 
```
LIMPIEZA        
```
close(p1[1]) ;  // eliminamos la tuberia
                close(p1[0]);
                }
```
IGUAL EN HIJO:
```
                else {          // estamos en el proceso hijo
                close(0);
                dup(p1[0]);     // redirigimos la entrada estandar del hijo, para recibirla del padre
                close(p1[0]);
                close(p1[1]);
                }
```

## 2. Variables de entorno:
Cuando se crea un nuevo proceso hijo, este hereda todas las Variables de
entorno de su padre, ademas de los parametros de entrada.
int main(int argc, char** argv, char** envp) las variables de entorno estan en un vector: el tercer 
parametro.
LLAMADAS DE ENTORNO: 
- char * getenv(const char * var); 
Su parametro unico es el nombre de la variable de entorno, y su salida es el valor de esta

- int setenv(const char * var, const char * val, int overwrite);
Funcionalidad: sirve para modificar variable de entorno
Parametros: 1) nombre de variable de entorno, 2) valor nuevo de variable de entorno 3) sobreescribir
el contenido anterior
Salida: error o ok

- int putenv(const char * par); ????


crear zip y probar:

```
chmod +x probador_ssoo_p2.sh
zip ssoo_p2_100472050_100474969_100472007.zip msh.c autores.txt
./probador_ssoo_p2.sh ssoo_p2_100472050_100474969_100472007.zip
```