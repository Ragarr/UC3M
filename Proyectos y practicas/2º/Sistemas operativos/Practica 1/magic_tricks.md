## Probador comandos
cd 'Practica 1/p1_llamadas_2023'
zip ssoo_p1_100472050_100474969_100472007.zip Makefile mywc.c myenv.c myls.c autores.txt
python3 probador_ssoo_p1.py ssoo_p1_100472050_100474969_100472007.zip


 ## open(char *name , int flags) 
    - name es el puntero al nombre del archivo,
    - flags es el modo de apertura (O_RDONLY, O_WRONLY, O_RDWR)
        otros flags son: O_CREAT(si no existe lo crea), 
        O_TRUNC (trunca si se abre para escritura), 
        O_APPEND (puntero al final del archivo)
Devuelve o el descriptor del archivo o -1 si hay error.

El descriptor del archivo es un entero positivo que se usa para referirse al archivo
en las llamadas a las funciones de E/S (las demas funciones [write, read, close])

       
## close(int fd)
    - fd es el descriptor del archivo
Devuelve 0 si todo va bien o -1 si hay error.

El proceso pierde la asociación con el archivo (lo cierra).

    
## read(int fd, char *buf, int nbytes)
    - fd es el descriptor del archivo
    - buf es el puntero al buffer donde se almacenan los datos leidos
    - nbytes es el numero de bytes a leer (en este caso bufsiz)
Devuelve el numero de bytes leidos o -1 si hay error.

Transfiere nbytes bytes del archivo asociado al descriptor fd a la variable
(buffer) buf, si se rebasa el final del archivo se leen los bytes que queden.

Si se llega al final del archivo spre devuelve 0.
    

## write(int fd, char *buf, int nbytes)
    - fd es el descriptor del archivo
    - buf es el puntero al buffer donde se almacenan los datos a escribir
    - nbytes es el numero de bytes a escribir
Devuelve el numero de bytes escritos o -1 si hay error.

Transfiere nbytes bytes del buffer buf al archivo asociado al descriptor fd.

Puede escribir menos bytes de los que se le piden, por ejemplo si se llena el disco,
se llega al tamaño maximo de un archivo o se interrumpe por una señal.

Si se llega al final del archivo aumenta el tamaño del archivo.


## opendir(char *name)
    - name es el puntero al nombre del directorio
    - toma el nombre del directorio y devuelve un puntero a una estructura DIR
    - si hay error devuelve NULL
    - opendir(".") abre el directorio actual
    - opendir("..") abre el directorio padre

## DIR 
    - es un puntero a un directorio
    - es un tipo de dato que contiene la información necesaria para poder leer un directorio
    - no sabes su estructura interna porque es privada. 
    - puedes usar funciones para acceder a ella como opendir, readdir(lee la lista de archivos), closedir, 
    
## readdir(DIR *dirp)
    - dirp es el puntero a la estructura DIR
    - devuelve un puntero a una estructura dir_ent, que es una estructura de datos que contiene información sobre un archivo en un directorio
    - si hay error o no quedan archivos por leer devuelve NULL
    - para poder recibir el dir_ent como retorno de esta función, se debe declarar un puntero a dir_ent y asignarle el valor de la función
    - al devolver un puntero a un dir_ent, para leer los nombres de los archivos se debe usar el operador flecha (->) en lugar del punto (.)
    - (*dir_ent)->d_name


## struct dir_ent
{
    d_ino /* numero de inodo */
    d_off /* donde empieza el archivo en el directorio (puntero interno a la carpeta) */
    d_reclen /* longitud de esta entrada */
    d_name /* nombre del archivo */
    d_type /* tipo de archivo */
    }

## cd (comando de consola)
    - cambia el directorio actual de trabajo
    - cd .. cambia al directorio padre
    - cd / cambia al directorio raiz
    - cd <nombre de carpeta> cambia al directorio indicado, siempre que exista
    - cd - cambia al directorio anterior

## ls (comando de consola)
    - lista los archivos y directorios del directorio actual pero tambien contiene 2 archivos ocultos: . y .. que son el directorio actual y el directorio padre respectivamente y te permite navegar entre ellos con el comando cd . y cd ..