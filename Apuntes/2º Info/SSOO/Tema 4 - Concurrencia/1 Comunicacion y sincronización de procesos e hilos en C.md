# Semaforos
`#include <semaphore.h>
Un semáforo debe ser una variable de memoria compartida

Hay dos tipos de semáforo
- Con nombre:
	- puede ser usado por distintos procesos que conozcan el nombre. No requiere memoria compartida.
	- `sem_t *semaforo; //nombrados
- Sin nombre
	- pueden ser utilizados solo por el proceso que los crea (y sus threads) o por procesos que tengan una zona de memoria compartida.
	- `sem_t semaforo; // no nombrado

## Semáforos en POSIX

- `int sem_init(sem_t *sem, int shared, int val);`: 
	- Esta función inicializa un semáforo sin nombre. 
		- `sem_t *sem`: puntero al semáforo a inicializar
		- `int shared`: valor booleano que indica si el semáforo será compartido entre procesos
		- `int val`: valor entero que indica el valor inicial del semáforo
		- Devuelve 0 si la inicialización se realizó correctamente, de lo contrario devuelve -1.

- `int sem_destroy(sem_t *sem);`: 
	- Esta función destruye un semáforo sin nombre previamente inicializado. 
		- `sem_t *sem`: puntero al semáforo a destruir
		- Devuelve 0 si la destrucción se realizó correctamente, de lo contrario devuelve -1.

- `sem_t *sem_open(char *name, int flag, mode_t mode, int val);`: 
	- Esta función abre (o crea) un semáforo con nombre. 
		- `char *name`: nombre del semáforo
		- `int flag`: bandera que indica el modo de apertura del semáforo (puede ser O_CREAT, O_EXCL, O_TRUNC, O_RDONLY, O_WRONLY o O_RDWR)
			- O_CREAT lo crea. 
			- O_CREAT | O_EXECL. Lo crea si no existe, -1 en caso de que exista.
			- Con flag 0. Si no existe devuelve -1.
		- `mode_t mode`: modo de acceso al semáforo (por ejemplo, S_IRUSR para permiso de lectura para el usuario que creó el semáforo)
		- `int val`: valor inicial del semáforo
		- Devuelve un puntero al semáforo si se pudo abrir (o crear) correctamente, de lo contrario devuelve SEM_FAILED.

- `int sem_close(sem_t *sem);`: 
	- Esta función cierra un semáforo con nombre previamente abierto. 
		- `sem_t *sem`: puntero al semáforo a cerrar
		- Devuelve 0 si el cierre se realizó correctamente, de lo contrario devuelve -1.

- `int sem_unlink(char *name);`: 
	- Esta función borra un semáforo con nombre. 
		- `char *name`: nombre del semáforo a borrar
		- Devuelve 0 si se pudo borrar el semáforo correctamente, de lo contrario devuelve -1.

- `int sem_wait(sem_t *sem);`:
	- Esta función realiza la operación wait sobre un semáforo, disminuyendo su valor en 1. Si el valor del semáforo es 0, el proceso se bloquea hasta que el valor del semáforo sea mayor que 0.
		- `sem_t *sem`: puntero al semáforo sobre el que se realizará la operación wait.
		- La función devuelve 0 si la operación se realizó correctamente, de lo contrario devuelve -1.
	
- `int sem_trywait(sem_t *sem);`:
	- Esta función intenta realizar la operación wait sobre un semáforo, disminuyendo su valor en 1. Si el valor del semáforo es 0, la función devuelve inmediatamente con un valor de -1.
		- `sem_t *sem`: puntero al semáforo sobre el que se intentará realizar la operación wait.
		- La función devuelve 0 si la operación se realizó correctamente, de lo contrario devuelve -1.

- `int sem_post(sem_t *sem);`:
	- Esta función realiza la operación signal sobre un semáforo, aumentando su valor en 1. Si hay procesos bloqueados esperando en el semáforo, uno de ellos se desbloqueará.
		- `sem_t *sem`: puntero al semáforo sobre el que se realizará la operación signal.
		- La función devuelve 0 si la operación se realizó correctamente, de lo contrario devuelve -1.

- `int sem_getvalue(sem_t *sem, int *sval);`:
	- Esta función obtiene el valor actual de un semáforo y lo guarda en la variable apuntada por `sval`.
		- `sem_t *sem`: puntero al semáforo del que se desea obtener el valor.
		- `int *sval`: puntero a la variable en la que se guardará el valor del semáforo.
		- La función devuelve 0 si se pudo obtener el valor correctamente, de lo contrario devuelve -1.

## Secciones críticas con semáforos
```c
sem_wait(s); /* entrada en la seccion critica */ 
< seccion critica > 
sem_post(s); /* salida de la seccion critica */
```
El semáforo debe tener valor inicial 1 o superior
![[Pasted image 20230424190330.png]]

## Ejemplos
### Productor-consumidor
```c
# define MAX_BUFFER 1024 /* tamanio del buffer */
# define DATOS_A_PRODUCIR 100000 /* datos a producir */ 

sem_t elementos; /* elementos en el buffer */
sem_t huecos; /* huecos en el buffer */
int buffer[MAX_BUFFER]; /* buffer comun */

void main(void){
	pthread_t th1, th2; /* identificadores de threads */
	/* inicializar los semaforos */
	sem_init(&elementos, 0, 0);
	sem_init(&huecos, 0, MAX_BUFFER);
	/* crear los procesos ligeros */
	pthread_create(&th1, NULL, Productor, NULL);
	pthread_create(&th2, NULL, Consumidor, NULL); 
	/* esperar su finalizacion */
	pthread_join(th1, NULL);
	pthread_join(th2, NULL);
	sem_destroy(&huecos);
	sem_destroy(&elementos);
	exit(0);
}

```
![[Pasted image 20230424190957.png]]
#### Hilo productor
```c
void Productor(void) /* codigo del productor */
{
	int pos = 0; /* posicion dentro del buffer */
	int dato; /* dato a producir */
	int i;
	for(i=0; i < DATOS_A_PRODUCIR; i++ ) {
		dato = i; /* producir dato */
		sem_wait(&huecos); /* un hueco menos */
		buffer[pos] = i;
		pos = (pos + 1) % MAX_BUFFER;
		sem_post(&elementos); /* un elemento mas */
	}
	pthread_exit(0);
}
```
#### Hilo consumidor
```c
void Consumidor(void) /* codigo del Consumidor */
{
	int pos = 0;
	int dato;
	int i;
	for(i=0; i < DATOS_A_PRODUCIR; i++ ) {
		sem_wait(&elementos); /* un elemento menos */
		dato = buffer[pos];
		pos = (pos + 1) % MAX_BUFFER;
		sem_post(&huecos); /* un hueco mas */
		/* cosumir dato */
	}
	pthread_exit(0);
}
```

# Mutex y variables condicionales
## Mutex
Un mutex es un mecanismo de sincronización indicado para procesos ligeros.
Es un semáforo binario (puede estar en dos estados: bloqueado o desbloqueado) 

Cuando un hilo de ejecución necesita acceder al recurso compartido, **primero intenta bloquear el mutex**. Si el mutex está desbloqueado, se bloquea y el hilo puede acceder al recurso compartido. Si el mutex está bloqueado, el hilo espera hasta que el mutex se desbloquee por otro hilo.

Tiene dos operaciones atómicas:
- wait Bloquea al proceso ligero que la ejecuta y le expulsa del mutex 
- signal Desbloquea a uno o varios procesos suspendidos en la variable condicional. El proceso que se despierta compite de nuevo por el mutex
Conveniente ejecutarlas entre lock y unlock
![[Pasted image 20230424192749.png]]

### Secciones críticas con Mutex
```c
lock(m); /* entrada en la seccion critica */ 
< seccion critica > 
unlock(s); 
/* salida de la seccion critica */
``` 
La operación unlock debe realizarla el mismo proceso ligero que ejecutó lock

## Variables condicionales
Las variables de condición funcionan junto con los mutex. 

Cuando un hilo adquiere un mutex, si la condición que necesita no se cumple, se bloqueará en la variable de condición asociada a ese mutex. Cuando otro hilo completa la tarea necesaria y cambia la condición, puede despertar al hilo original al enviar una señal a la variable de condición. 

En resumen, las variables de condición se utilizan para esperar a que se cumpla una condición antes de continuar la ejecución de un programa.

## Uso en POSIX
Todas las funciones se incluyen en `pthread.h`
### Funciones  de Mutex
- `int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);`: 
	- Esta función inicializa un objeto de mutex.
		- `pthread_mutex_t *mutex`: puntero al objeto de mutex a inicializar.
		- `const pthread_mutexattr_t *attr`: puntero a la estructura de atributos del mutex, o NULL si se desea utilizar los atributos predeterminados.
		- Devuelve 0 si la inicialización se realizó correctamente, de lo contrario devuelve un código de error.
- `int pthread_mutex_lock(pthread_mutex_t *mutex);`: 
	- Esta función bloquea el mutex.
		- `pthread_mutex_t *mutex`: puntero al objeto de mutex a bloquear.
		- La función se bloquea si el mutex ya está bloqueado por otro hilo y espera hasta que el mutex esté libre.
		- Devuelve 0 si se realizó correctamente el bloqueo, de lo contrario devuelve un código de error.
- `int pthread_mutex_unlock(pthread_mutex_t *mutex);`: 
	- Esta función desbloquea el mutex.
		- `pthread_mutex_t *mutex`: puntero al objeto de mutex a desbloquear.
		- La función fallará si el mutex no está bloqueado.
		- Devuelve 0 si se realizó correctamente el desbloqueo, de lo contrario devuelve un código de error.
- `int pthread_mutex_destroy(pthread_mutex_t *mutex);`: 
	- Esta función destruye el objeto de mutex.
		- `pthread_mutex_t *mutex`: puntero al objeto de mutex a destruir.
		- La función fallará si el mutex está bloqueado.
		- Devuelve 0 si la destrucción se realizó correctamente, de lo contrario devuelve un código de error.

### Funciones para el resto de variables de condición

- `int pthread_cond_init(pthread_cond_t *cond, const pthread_condattr_t *attr);`: Esta función inicializa una variable de condición. Recibe como argumentos la variable de condición a inicializar y un puntero a los atributos de la variable de condición. Devuelve 0 si se realizó correctamente la inicialización y -1 en caso de error.

- `int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex);`: Esta función bloquea el hilo actual hasta que la variable de condición sea señalada. La función espera a que se señale la variable de condición y el mutex está bloqueado. Devuelve 0 si se realizó correctamente el bloqueo y -1 en caso de error.

- `int pthread_cond_signal(pthread_cond_t *cond);`: Esta función señala la variable de condición, despertando a uno de los hilos que está esperando por ella. Devuelve 0 si se realizó correctamente la señalización y -1 en caso de error.

- `int pthread_cond_broadcast(pthread_cond_t *cond);`: Esta función señala la variable de condición, despertando a todos los hilos que están esperando por ella. Devuelve 0 si se realizó correctamente la señalización y -1 en caso de error.

- `int pthread_cond_destroy(pthread_cond_t *cond);`: Esta función destruye la variable de condición. Devuelve 0 si se realizó correctamente la destrucción y -1 en caso de error.

Dentro de una seccion critica si que se ejecutan los signal

## Productor-consumidor con mutex
```c
#define MAX_BUFFER 1024 /* tamanio del buffer */
#define DATOS_A_PRODUCIR 100000 /* datos a producir */
pthread_mutex_t mutex; /* mutex de acceso al buffer compartido */

pthread_cond_t no_lleno; /* controla el llenado del buffer */
pthread_cond_t no_vacio; /* controla el vaciado del buffer */

int n_elementos; /* numero de elementos en el buffer */
int buffer[MAX_BUFFER]; /* buffer comun */
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
}
```
### Productor
```c
void Productor(void) { /* codigo del productor */
	int dato, i ,pos = 0;
	for(i=0; i < DATOS_A_PRODUCIR; i++ ) {
		dato = i; /* producir dato */
		
		pthread_mutex_lock(&mutex); /* acceder al buffer */
		while (n_elementos == MAX_BUFFER){ /* si buffer lleno */
			pthread_cond_wait(&no_lleno, &mutex); /* se bloquea */
		}
		// un consumidor lo ha desbloqueado
		buffer[pos] = i;
		
		pos = (pos + 1) % MAX_BUFFER;
		
		n_elementos ++;
		// por si acaso algun consumidor esta esperando, le señalamos
		// que el bufer ya no esta vacio
		pthread_cond_signal(&no_vacio); /* buffer no vacio */
		pthread_mutex_unlock(&mutex);
	}
	pthread_exit(0);
}
```

### Consumidor
```c
void Consumidor(void) { /* codigo del sonsumidor */
	int dato, i ,pos = 0;
	for(i=0; i < DATOS_A_PRODUCIR; i++ ) { 
		pthread_mutex_lock(&mutex); /* acceder al buffer */
		
		while (n_elementos == 0){ /* si buffer vacio */
			pthread_cond_wait(&no_vacio, &mutex); /* se bloquea */
		}
		dato = buffer[pos];
		pos = (pos + 1) % MAX_BUFFER;
		n_elementos --;
		// por si algun productor estuviera esperando le señalamos que
		// se ha desbloqueado un hueco en el buffer
		pthread_cond_signal(&no_lleno); /* buffer no lleno */
		pthread_mutex_unlock(&mutex);
		printf("Consume %d \n", dato); /* consume dato */
	}
	pthread_exit(0);
}
```
