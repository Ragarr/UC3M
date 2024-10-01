![[Pasted image 20230526125338.png]]
Un servidor recibe peticiones que debe procesar y realiza el siguiente proceso:
1. Recepción de petición: Cada petición requiere un cierto tiempo en operaciones de entrada/salida para ser recibida
2. Procesamiento de la petición: Un cierto tiempo de procesamiento en CPU
3. Envío de respuesta: Un cierto tiempo de entrada/salida para contestar.

Vamos a usar este ejemplo de codigo para simular un servidor.
```c
struct peticion {
	long id;
	/* Resto de campos necesarios */
	int tipo;
	char url[80];
	/* ... */
};
typedef struct peticion peticion_t;
void recibir_peticion (peticion_t * p); 
void responder_peticion (peticion_t * p);
```
```c
void recibir_peticion (peticion_t * p) 
{
	int delay;
	fprintf(stderr, "Recibiendo petición\n");
	p->id = petid++;
	/* Simulación de tiempo de E/S */
	delay = rand() % 5;
	sleep(delay);
	fprintf(stderr,"Petición %d recibida después de %d segundos\n", 
			p->id, delay);
}
```
```c
void responder_peticion (peticion_t * p) 
{
	int delay, i;
	double x;
	fprintf(stderr, "Enviando petición %d\n", p->id);
	/* Simulación de tiempo de procesamiento */
	for (i=0;i<1000000;i++) { x = 2.0 * i; }
	/* Simulación de tiempo de E/S */
	delay = rand() % 20;
	sleep(delay);
	fprintf(stderr, "Petición %d enviada después de %d segundos\n", 
			p->id, delay);
}
```

# Primera Solución 
Ejecutar de modo indefinido:
1. Recibir petición
2. Procesar peticion
## Implementación
```c
int main() {
	pe+cion_t p;
	for (;;){
		recibir_pe+cion(&p);
		responder_pe+cion(&p);
	}
	return 0;
}
```
## Problemas
Llegada de peticiones.
- Si dos peticiones llegan al mismo tiempo …
- Si una petición llega mientras otra se está procesando …

# Solución basada en procesos
Cada vez que llega una petición se crea un proceso hijo:
- El **proceso hijo** realiza el **procesamiento de la petición**.
- El **proceso padre** pasa a esperar la **siguiente petición**.
## Implementación
```c
#include "pe+cion.h"
#include <stdio.h>
#include <+me.h>
#include <sys/wait.h>
int main() {
	const int MAX_PETICIONES = 5;
	int i;
	time_t t1,t2;
	peticion_t p;
	int pid, hijos=0;
	t1 = time(NULL)
	for (i=0;i<MAX_PETICIONES;i++) {
		recibir_peticion(&p);
		do {
			fprintf(stderr, "Comprobando hijos\n");
			pid = waitpid(-1, NULL, WNOHANG);
			if (pid>0) { hijos--; }
		} while (pid > 0);
		pid = fork();
		if (pid<0) { perror("Error en la creación del hijo"); }
		if (pid==0) { responder_peticion(&p); exit(0); } /* HIJO */
		if (pid!=0) { hijos++; } /* PADRE */
	}
	fprinf(stderr, "Comprobando %d hijos\n", hijos);
	while (hijos>0) {
		pid = waitpid(-1, NULL, WNOHANG);
		if (pid>0) { hijos--; }
	} ;
	t2 = time(NULL);
	double dif = diUime(t2,t1);
	prinV("Tiempo: %lf\n",dif);
	return 0;
}
```
## Problemas
- Hace falta arrancar un proceso (fork) por cada petición que llega.
- Hace falta terminar un proceso (exit) por cada petición que termina.
- Excesivo consumo de recursos del sistema.
- No hay control de admisión. 
	- Problemas de calidad de servicio.

# Solución con hilos
Cada vez que se recibe una petición se crea un hilo.
Pool de hilos. 
- Se tiene un número fijo de hilos creados.
- Cada vez que se recibe una petición se busca un hilo libre ya creado para que atienda la petición.
	- Comunicación mediante una cola de peticiones.

# Solución con hilos  bajo demanda
Se tiene un hilo receptor encargado de recibir las peticiones.
Cada vez que llega una petición se crea un hilo y se le pasa una copia la petición al hilo recién creado. 
- Tiene que ser una copia de la petición porque la petición original se podría modificar

## Implementación
**main**: (crea el receptor)
```c
#include "peticion.h"
#include <stdio.h>
#include <time.h>
#include <pthread.h>
#include <semaphore.h>
sem_t snhijos;
int main() {
	time_t t1, t2;
	double dif;
	pthread_t thr;
	t1 = time(NULL);
	sem_init(&snhijos, 0, 0);
	pthread_create(&thr, NULL, 
	receptor, NULL);
	pthread_join(thr, NULL);
	sem_destroy(&snhijos);
	t2 = time(NULL);
	dif = difftime(t2,t1);
	printf("Tiempo: %lf\n",dif);
	return 0;
}
```
**receptor:**
```c
void * receptor (void * param) {
	const int MAX_PETICIONES = 5; int nservicio = 0; int i;
	peCcion_t p; pthread_t th_hijo;
	for (i=0;i<MAX_PETICIONES;i++) {
	recibir_peCcion(&p); nservicio++;
	pthread_create(&th_hijo, NULL, servicio, &p);
	}
	for (i=0;i<nservicio;i++) { 
		fprinO(stderr, "Haciendo wait\n");
		sem_wait(&snhijos);
		fprinO(stderr, "Saliendo de wait\n");
	}
	pthread_exit(0); return NULL;
}
```
**servicio**:
```c
void * servicio (void * p)
{
	peticion_t pet;
	copia_peticion(&pet,(peticion_t*)p);
	fprintf(stderr, "Iniciando servicio\n");
	responder_peticion(&pet);
	sem_post(&snhijos);
	fprintf(stderr, "Terminando servicio\n");
	pthread_exit(0); return NULL;
}
```
## Problema
La creación y terminación de hilos tiene un coste menor que la de procesos, pero sigue siendo un coste.
No hay control de admisión:
- ¿Que pasa si llegan muchas peticiones o las peticiones recibidas no terminan?

# Solución con pool de hilos
Un pool de hilos es un conjunto de hilos que se tiene creados desde el principio para ejecutar un servicio:
- Cada vez que llega una petición se pone en una cola de peticiones pendientes.
- Todos los hilos esperan a que haya alguna petición en la cola y la retiran para procesarla.

## Implementación
main: lanza la pool de servicios y el receptor
```c
#include "peticion.h"
#include <stdio.h>
#include <time.h>
#include <pthread.h>
#include <semaphore.h>
#define MAX_BUFFER 128
peticion_t buffer[MAX_BUFFER];
int n_elementos;
int pos_servicio = 0;
pthread_mutex_t mutex;
pthread_cond_t no_lleno;
pthread_cond_t no_vacio;
pthread_mutex_t mfin;
int fin=0;

int main() 
{
	time_t t1, t2;
	double dif;
	pthread_t thr;
	pthread_t ths[MAX_SERVICIO];
	const int MAX_SERVICIO = 5; int i;
	t1 = time(NULL);
	
	pthread_mutex_init(&mutex,NULL);
	pthread_cond_init(&no_lleno,NULL);
	pthread_cond_init(&no_vacio,NULL);
	pthread_mutex_init(&mfin,NULL);
	pthread_create(&thr, NULL, receptor, NULL);
	for (i=0;i<MAX_SERVICIO;i++) {
		pthread_create(&ths[i], NULL, servicio, NULL);
	}
	
	pthread_join(thr, NULL);
	for (i=0;i<MAX_SERVICIO;i++) {
		pthread_join(ths[i],NULL);
	}
	pthread_mutex_destroy(&mutex);
	pthread_cond_destroy(&no_lleno);
	pthread_cond_destroy(&no_vacio);
	pthread_mutex_destroy(&mfin);
	t2 = time(NULL);
	dif = difftime(t2,t1);
	printf("Tiempo: %lf\n",dif);
	return 0;
}
```
**receptor:** recibe una petición y la mete en el buffer de peticiones
```c
void * receptor (void * param){
	const int MAX_PETICIONES = 5;
	pe+cion_t p;
	int i, pos=0;
	for (i=0;i<MAX_PETICIONES;i++) 
	{
		recibir_pe+cion(&p);
		pthread_mutex_lock(&mutex);
		while (n_elementos == MAX_BUFFER){ 
			pthread_cond_wait(&no_lleno, &mutex); 
		}
		buffer[pos] = p;
		pos = (pos+1) % MAX_BUFFER;
		n_elementos++;
		pthread_cond_signal(&no_vacio);
		pthread_mutex_unlock(&mutex);
	}
	fprintf(stderr,"Finalizando receptor\n");
	pthread_mutex_lock(&mfin);
	fin=1;
	pthread_mutex_unlock(&mfin);
	pthread_mutex_lock(&mutex);
	pthread_cond_broadcast(&no_vacio);
	pthread_mutex_unlock(&mutex);
	fprintf(stderr, "Finalizado receptor\n");
	pthread_exit(0);
	return NULL;
} /* receptor */
```
**servicio:**
```c
void * servicio (void * param){
	peticion_t p;
	for (;;) {
		pthread_mutex_lock(&mutex);
		while (n_elementos == 0) {
			if (fin==1) {
				fprinf(stderr,"Finalizando servicio\n");
				pthread_mutex_unlock(&mutex);
				pthread_exit(0);
			}
			pthread_cond_wait(&no_vacio, &mutex);
		} // while lock
		fprintf(stderr, "Sirviendo posicion %d\n", pos_servicio);
		p = buffer[pos_servicio];
		pos_servicio = (pos_servicio + 1) % MAX_BUFFER;
		n_elementos --;
		pthread_cond_signal(&no_lleno);
		pthread_mutex_unlock(&mutex);
		responder_peticion(&p);
	}// for
	pthread_exit(0);
	return NULL;
```

# Comparación
![[Pasted image 20230526132617.png]]
