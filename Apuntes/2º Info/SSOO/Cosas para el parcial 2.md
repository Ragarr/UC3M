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

# Concurrencia - mutex
## En main:
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

## En los threads:
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