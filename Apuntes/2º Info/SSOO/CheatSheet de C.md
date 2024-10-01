# [[Procesos]]
se incluye en la biblioteca `unistd.h`
- ``pid_t fork(void)
	- Duplica el proceso que invoca la llamada. 
	- El proceso padre y el proceso hijo siguen **<mark style="background: #FFB8EBA6;">ejecutando el mismo programa</mark>**. 
	- El proceso <mark style="background: #FFB8EBA6;">hijo hereda los ficheros abiertos</mark> del proceso padre. 
	- Se copian los descriptores de archivos abiertos. 
	- Se desactivan las alarmas pendientes.
	- Devuelve:
		- -1 el caso de error. 
		- En el proceso padre: el identificador del proceso hijo.
		- En el proceso hijo: 0

``void exit(status)
- Se cierran todos los descriptores de ficheros abiertos. 
- Se liberan todos los recursos del proceso. 
- Se libera el BCP del proceso

``pid_t wait(int* status)
La función espera a que se produzca un cambio en el estado de uno de los procesos secundarios que estén siendo supervisados por el proceso principal y devuelve información sobre el estado del proceso hijo.
status" es un puntero a una variable de tipo "int" que se utiliza para almacenar información sobre el estado del proceso hijo.

## Servicio exec
Cambia la imagen del proceso actual. 
`` int execl(const char *path, const char *arg, ...)
- path: Ruta al archivo ejecutable. 

``int execvp(const char *file, char *const argv\[])
- file: Busca el archivo ejecutable en todos los directorios especificados por PATH.
- Descripción: 
	- Devuelve -1 en caso de error, en caso contrario no retorna. 
	- El mismo proceso ejecuta otro programa. 
	- Los ficheros abiertos permanecen abiertos. 
	- Las señales con la acción por defecto seguirán por defecto, las señales con manejador tomarán la acción por defecto

# Threads

**Lanzar un thread**
```c
int pthread_create(pthread_t *thread,
	const pthread_attr_t *attr,
	void *(*func)(void *),
	void *arg)
```
Crea un hilo e inicia su ejecución.
- `thread`: Se debe pasar la dirección de una variable del tipo pthread_t que se usa como manejador del hilo. 
- `attr`: Se debe pasar la dirección de una estructura con los atributos del hilo. Se puede pasar NULL para utilizar atributos por defecto. 
- `func`: Función con el código de ejecución del hilo. 
- `arg`: Puntero al parámetro del hilo. Solamente se puede pasar un parámetro.

**Esperar que un thread termine**
```c
int pthread_join(pthread_t thread, void **value)
```
- `thread`: Manejador de del hilo al que hay que esperar. 
- `value`: Es un puntero que guardara el estado de terminación del hilo una vez que termine

**Terminar un thread**
```c
int pthread_exit(void *value)
```
Value es el valor que devuelve (no puede ser un puntero a una var. local)

## Concurrencia - mutex
### En main
- inicializar los mutex y las variables de condición.
- Lanzar los threads.
- Esperar los threads.
- Destruir los mutex y las var. de condición.
```c
pthread_mutex_t mutex; /* mutex de acceso al buffer compartido */
pthread_cond_t no_lleno; /* controla el llenado del buffer */
pthread_cond_t no_vacio; /* controla el vaciado del buffer */
main(int argc, char *argv[]){
	pthread_t th1, th2;
	pthread_mutex_init(&mutex, NULL);
	pthread_cond_init(&no_lleno, NULL);
	pthread_cond_init(&no_vacio, NULL);
	
	pthread_create(&th1, NULL, Productor, NULL);
	pthread_create(&th2, NULL, Consumidor, NULL);
	
	pthread_join(th1, NULL);
	pthread_join(th2, NULL);
	
	pthread_mutex_destroy(&mutex);
	pthread_cond_destroy(&no_lleno);
	pthread_cond_destroy(&no_vacio);
	exit(0);
```

### En los threads
1. Bloquear el mutex
2. Esperar variables de condicion
3. Zona crítica
4. Enviar señales 
5. Liberar mutex
```c
void Productor(void) { /* codigo del productor */
	while(1){
		pthread_mutex_lock(&mutex); /* acceder al buffer */
		while (n_elementos == MAX_BUFFER){ /* si buffer lleno */
			pthread_cond_wait(&no_lleno, &mutex); /* se bloquea */
		}
		// TRATAR DATOS Y COMPROBAR SALIDA DE BUCLE
		pthread_cond_signal(&no_vacio); /* buffer no vacio */
		pthread_mutex_unlock(&mutex);
	}
	if (soy el ultimo productor en terminar){
		pthread_cond_broadcast(&no_vacio);
	}
	pthread_exit(0);
}
```
```c
void Consumidor(void) { /* codigo del sonsumidor */
	while(1){ 
		pthread_mutex_lock(&mutex); /* acceder al buffer */
		while (n_elementos == 0){ /* si buffer vacio */
			pthread_cond_wait(&no_vacio, &mutex); /* se bloquea */
		}
		// TRATAR DATOS Y COMPROBAR SALIDA DE BUCLE
		pthread_cond_signal(&no_lleno); /* buffer no lleno */
		pthread_mutex_unlock(&mutex);
		printf("Consume %d \n", dato); /* consume dato */
	}
	pthread_exit(0);
}
```

# Memoria - proyecciones

 **Proyección:**
 ```c
 void *mmap(void *direc, size_t lon, int prot, int flags, int fd, off_t desp);
 ```

  `void *direc`, dirección donde proyectar. Si es `NULL` el SO elige una.
- `size_t lon`, especifica el número de bytes a proyectar
- `int prot`, Protección para la zona (se pueden combinar con |):
	- `PROT_READ`: Se puede leer. 
	- `PROT_WRITE`: Se puede escribir. 
	- `PROT_EXEC`: Se puede ejecutar. 
	- `PROT_NONE`: No se puede acceder a los datos.
- `int flags`, Propiedades de la región:
	- `MAP_SHARED`: La región es compartida. Las modificaciones afectan al fichero. <mark style="background: #ABF7F7A6;">Los procesos hijos comparten la región</mark>. 
	- `MAP_PRIVATE`: La región es privada. El fichero no se modifica. <mark style="background: #ABF7F7A6;">Los procesos hijos obtienen duplicados no compartidos.</mark> 
	- `MAP_FIXED`: El fichero debe proyectarse en la dirección especificada por la llamada.
- `int fd`, Descriptor del fichero que se desea proyectar en memoria.
- `off_t desp`, Desplazamiento inicial sobre el archivo.

**Desproyección**
	**`void munmap(void *direc, size_t lon);`** 
Desproyecta parte del espacio de direcciones de un proceso desde la dirección ``direc`` hasta ``direc``+``lon``.


# Archivos y directorios

**Abrir fichero**
 ```c
int open(const char * path, int flags, [mode_t mode])`
```
- ``flags``: ``O_RDONLY, O_WRONLY, or O_RDWR.
- ``mode``: ``O_CREAT, O_APPEND, O_TRUNC, …
- Devuelve un descriptor de fichero (o -1 si error).

**Cerrar Fichero**
```c
int close(int fildes)
```
Cierra un archivo abierto anteriormente asociado al descriptor ``fildes`` (o -1 si error).

**leer fichero**
```c
ssize_t read(int fd, void * buf, size_t nbyte)
```
- ``fd`` es el descriptor del archivo
- ``buf`` es el puntero al buffer donde se almacenan los datos leidos
- ``nbytes`` es el numero de bytes a leer (en este caso bufsiz)
- Devuelve el numero de bytes leidos o -1 si hay error.
Transfiere nbytes bytes del archivo asociado al descriptor fd a la variable (buffer) buf, si se rebasa el final del archivo se leen los bytes que queden.
Si se llega al final del archivo devuelve 0.


**Crear directorio**
```c
int mkdir(const char *name, mode_t mode);
```
- **name**: nombre del directorio
- **mode**: bits de protección
- **Devuelve**: 0 ó -1 si error
- **Descripción**:
  - Crea un directorio de nombre `name`.
  - `UID_dueño = UID_efectivo`
  - `GID_dueño = GID_efectivo`

**Borrar directorio**
```c
int rmdir(const char *name);
```
- **name**: nombre del directorio
- **Devuelve**: 0 ó -1 si error
- **Descripción**:
  - Borra el directorio si está vacío.
  - Si el directorio no está vacío, no se borra.

**Abrir directorio**
```c
DIR *opendir(char *dirname);
```
- **dirname**: puntero al nombre del directorio
- **Devuelve**:
  - Un puntero para utilizarse en `readdir()` o `closedir()`.
  - NULL si hubo error.
- **Descripción**: Abre un directorio como una secuencia de entradas. Se coloca en el primer elemento.

**Cerrar directorio**
```c
int closedir(DIR *dirp);
```
- **dirp**: puntero devuelto por `opendir()`
- **Devuelve**: 0 ó -1 si error.
- **Descripción**: Cierra la asociación entre `dirp` y la secuencia de entradas de directorio.

**Leer directorio**
```c
struct dirent *readdir(DIR *dirp);
```
- **dirp**: puntero retornado por `opendir()`
- **Devuelve**:
  - Un puntero a un objeto del tipo `struct dirent` que representa una entrada de directorio.
  - NULL si hubo error.
- **Descripción**:
  - Devuelve la siguiente entrada del directorio asociado a `dirp`.
  - Avanza el puntero a la siguiente entrada.
  - La estructura es d
  - 
  - ependiente de la implementación. Debería asumirse que tan solo se obtiene un miembro: `char *d_name`.

**Rebobinar directorio**
```c
void rewindir(DIR *dirp);
```
- **dirp**: puntero devuelto por `opendir()`
- **Descripción**: Sitúa el puntero de posición dentro del directorio en la primera entrada.


**mover puntero de fichero**
```c
off_t lseek(int fd, off_t offset, int whence) 
```

- ``offset`` es lo que quieres desplazar, puede ser negativo o positivo
- ``whence`` es desde donde empiezas a contar
	- ``SEEK_SET`` → desde el principio del fichero. 
	- ``SEEK_CUR`` → desde la posición actual 
	- ``SEEK_END`` → desde el final del fichero.
- Modifica el valor del apuntador del descriptor ``fd`` en el archivo, a la posición explícita en desplazamiento (``offset``) a partir de la referencia impuesta en origen (``whence``). 
- Retorno = -1 → Error de posicionamiento.

**crear enlace a fichero**
```c
int link(const char *nombre, const char *nuevo);
```
- Crea un hard link con nombre ``nuevo`` al archivo ``nombre``.
- Incrementa contador de enlaces del fichero ``nombre``.

**crear enlace simbolico a un enlace ¿?¿?**
```c
int symlink(const char *nombre, const char *nombre_enlace);
```
- Crea un enlace simbólico hacia ``nombre`` desde ``nombre_enlace``. 
- Crea un nuevo archivo ``nombre_enlace`` que incluye ``nombre`` como únicos datos.

**borrar enlace de fichero**
```c
int unlink(const char *nombre);
```
- Borra el archivo ``nombre`` siempre que NO tenga enlaces hard pendientes (contador enlaces = 0) y nadie lo tenga abierto.
- Si hay enlaces duros (contador enlaces > 0) , se decrementa el contador de enlaces.
- Si algún proceso lo tiene abierto, se espera a que lo cierren todos.