# Tratamiento de ficheros
## open(char \*name , int flags)

- name es el puntero al nombre del archivo,
- flags es el modo de apertura (O_RDONLY, O_WRONLY, O_RDWR)

Otros flags son: 
- O_CREAT(si no existe lo crea).
- O_TRUNC (trunca si se abre para escritura).
- O_APPEND (puntero al final del archivo).
Devuelve o el descriptor del archivo o -1 si hay error.

El descriptor del archivo es un entero positivo que se usa para referirse al archivo.
en las llamadas a las funciones de E/S (las demas funciones: write, read, close)


## close(int fd)

- fd es el descriptor del archivo

Devuelve 0 si todo va bien o -1 si hay error.
El proceso pierde la asociación con el archivo (lo cierra).

## unlink(const char* path);
Argumentos:
- path nombre del fichero
Devuelve:
- Devuelve 0 ó -1 si error.
Descripción:
Decrementa el contador de enlaces del fichero. Si el contador es 0, borra el fichero y libera sus recursos.


## lseek(int fd, off_t offset, int whence);
Argumentos: 
- fd Descriptor de fichero 
- offset desplazamiento 
- whence base del desplazamiento 
Devuelve: 
 - La nueva posición del puntero ó -1 si error.
 Descripción: 
- Coloca el puntero de acceso asociado a fd 
- La nueva posición se calcula: n SEEK_SET posición = offset n SEEK_CUR posición = posición actual + offset n SEEK_END posición = tamaño del fichero + offset


## fnctl(int fildes, int cmd /* arg*/ ...);

Argumentos: 
- fildes descriptor de ficheros ¤ cmd mandato para modificar atributos, puede haber varios. 
Devuelve: 
- 0 para éxito ó -1 si error 
Descripción: 
- Modifica los atributos de un fichero abierto.


## dup(int fd);
Devuelve un descriptor de fichero que comparte todas las propiedades del fd ó -1 si error. 
Descripción: 
	Crea un nuevo descriptor de fichero que tiene en común con el anterior: n Accede al mismo fichero n Comparte el mismo puntero de posición n El modo de acceso es idéntico. ¤ El nuevo descriptor tendrá el menor valor numérico posible.

## read(int fd, char *buf, int nbytes)

- fd es el descriptor del archivo
- buf es el puntero al buffer donde se almacenan los datos leidos
- nbytes es el numero de bytes a leer (en este caso bufsiz)

Devuelve el numero de bytes leidos o -1 si hay error.
Transfiere nbytes bytes del archivo asociado al descriptor fd a la variable (buffer) buf, si se rebasa el final del archivo se leen los bytes que queden.

Si se llega al final del archivo devuelve 0.


## write(int fd, char *buf, int nbytes)

- fd es el descriptor del archivo
- buf es el puntero al buffer donde se almacenan los datos a escribir
- nbytes es el numero de bytes a escribir

Devuelve el numero de bytes escritos o -1 si hay error.
Transfiere nbytes bytes del buffer buf al archivo asociado al descriptor fd.
Puede escribir menos bytes de los que se le piden, por ejemplo si se llena el disco, se llega al tamaño maximo de un archivo o se interrumpe por una señal.

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

Esta formada por:
- d_ino /* numero de inodo */
- d_off /* donde empieza el archivo en el directorio (puntero interno a la carpeta) */
- d_reclen /* longitud de esta entrada */
- d_name /* nombre del archivo */
- d_type /* tipo de archivo */

# hay mas
en este [documento](https://aulaglobal.uc3m.es/pluginfile.php/6015756/mod_resource/content/1/Tema1.L2-Servicios-del-SO.pdf) , importante las proyecciones.
