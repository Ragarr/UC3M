
# Comandos entrega y test
```
chmod +x probador_ssoo_p3.sh
zip ssoo_p3_100472050_100474969_100472007.zip Makefile bank.c queue.c queue.h autores.txt
./probador_ssoo_p3.sh ssoo_p3_100472050_100474969_100472007.zip
```
## Cosas que poner en la memoria
hemos hecho lo maximo posible por lo optimizacion (para que se puedan ejecutar las maximas operaciones en paralelo)
lo de inicializar las cuentas a -inf es una chapuza que toco hacer para no crear structs

# Sobre la practica

La implementacion mas facil es con un array (puntero) (*element)a elementos. No es ideal
Si implementamos un array de punteroos a elementos la estructura es mas sencilla ya que solo tenemos que mover el puntero (**element)
Util -> Valgrind para los errres de coredump
instalacion valgrind https://stackoverflow.com/questions/24935217/how-to-install-valgrind-properly
# Documentación de hilos
Se usa la biblioteca `pthread.h`

## int phtread_create();
```c
int pthread_create(pthread_t *thread,
	const pthread_attr_t *attr,
	void *(*func)(void *),
	void *arg)
```
Crea un hilo e inicia su ejecución.
- thread: Se debe pasar la dirección de una variable del tipo pthread_t que se usa como manejador del hilo. 
- attr: Se debe pasar la dirección de una estructura con los atributos del hilo. Se puede pasar NULL para usar atributos por defecto. 
- func: Función con el código de ejecución del hilo. 
- arg: Puntero al parámetro del hilo. Solamente se puede pasar un parámetro.

## phtread_t phtread_self();
Devuelve el identificador del thread que ejecuta la llamada.

## int pthread_join();
```c
int pthread_join(pthread_t thread, void **value)
```
El hilo que invoca la función se espera hasta que el hilo cuyo manejador se especifique haya terminado.
- thread: Manejador de del hilo al que hay que esperar. 
- value: Es un puntero que guardara el estado de terminación del hilo una vez que termine
## int pthread_exit();
```c
int pthread_exit(void *value)
```
Permite a un thread finalizar su ejecución, value es el estado de terminación del mismo.
Value no puede ser un puntero a una variable local.

## Ejemplo:
El siguiente programa crea dos threads que imprimen un mensaje en la consola y luego se unen a los hilos principales utilizando la función pthread_join(). También utiliza pthread_exit() para salir del hilo secundario.
En este programa, la función print_message() es la función que se ejecuta en cada hilo secundario. Esta función toma un argumento void * que se convierte en un puntero char * y se imprime en la consola. Luego utiliza pthread_exit() para salir del hilo secundario.
En la función principal, se crean dos hilos utilizando pthread_create(). Cada hilo se le pasa el mensaje que se imprimirá en la consola. Después de crear los hilos, el programa espera a que los hilos finalicen utilizando pthread_join(). Finalmente, el hilo principal utiliza pthread_exit() para salir del programa.
```c
#include <stdio.h>
#include <pthread.h>

void *print_message(void *ptr);

int main()
{
    pthread_t thread1, thread2;

    const char *message1 = "Thread 1";
    const char *message2 = "Thread 2";

    pthread_create(&thread1, NULL, print_message, (void *)message1);
    pthread_create(&thread2, NULL, print_message, (void *)message2);

    printf("Main thread waiting for threads to finish...\n");

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("Threads finished. Main thread exiting.\n");

    pthread_exit(NULL);
}

void *print_message(void *ptr)
{   // ptr es el puntero al mensaje que se debe imprimir
    char *message;
    message = (char *)ptr;
    printf("%s\n", message);
    pthread_exit(NULL);
}

```


## Atributos del thread
Son un conjunto de valores que se utilizan para personalizar el comportamiento de los hilos creados en un programa. Incluyen cosas como el tamaño de la pila, la política de planificación, el alcance de los hilos y otros valores que afectan el comportamiento del hilo.

```c
int pthread_attr_init(pthread_attr_t * attr);
```
se utiliza para inicializar un objeto de atributos de hilo con valores predeterminados. 
La función acepta un objeto de atributos de hilo  como argumento (donde se guardaran nuestros atributos) y establece todos sus atributos en sus valores por defecto.

```c
int pthread_attr_destroy(pthread_attr_t * attr); 
```
Se utiliza para destruir un objeto de atributos de hilo.

```c
int pthread_attr_setstacksize(pthread_attr_t * attr, 
							  int stacksize); 
```
Se utiliza para establecer el tamaño de la pila del hilo.
- attr: el objeto de atributos de hilo
- stacksize: puntero a una variable donde esta almacenado el tamaño de la pila que se quiere establecer.

```c
int pthread_attr_getstacksize(
						pthread_attr_t *attr, 
						int *stacksize);
```
Se utiliza para obtener el tamaño de la pila actualmente establecido para un objeto de atributos de hilo.
- attr: el objeto de atributos de hilo
- stacksize: puntero a una variable que almacenará el tamaño de la pila actual.



## Separación de hilos (desacoplamiento)
Un hilo vinculado al hilo principal es un hilo que ha sido creado por el hilo principal y está diseñado para trabajar en conjunto con el hilo principal. En otras palabras, el hilo secundario está vinculado al hilo principal porque forma parte del flujo de ejecución del programa principal. Si el hilo principal finaliza su ejecución, el hilo secundario vinculado no puede continuar su ejecución.
Por otro lado, un hilo desvinculado del hilo principal es un hilo que ha sido creado por el hilo principal, pero no está diseñado para trabajar en conjunto con el hilo principal. En otras palabras, el hilo secundario está desvinculado del hilo principal porque no forma parte del flujo de ejecución del programa principal. Si el hilo principal finaliza su ejecución, el hilo secundario desvinculado puede continuar su ejecución.
Si el hilo secundario necesita trabajar en conjunto con el hilo principal, entonces debe estar vinculado al hilo principal. Por otro lado, si el hilo secundario no necesita trabajar en conjunto con el hilo principal y puede seguir ejecutándose después de que el hilo principal finalice su ejecución, entonces debe estar desvinculado del hilo principal.


```c
int pthread_attr_setdetachstate(pthread_attr_t *attr,
								int detachstate)
```
Establece el el estado de desvinculación de un atributo de hilo. Toma dos argumetnos el objeto attributo del hilo y el estado de desvinculacion (detachstate).
- Si "detachstate" = PTHREAD_CREATE_DETACHED establece que el hilo estará desvinculado del hilo principal, por lo tanto el thread liberara sus recursos cuando finalice su ejecución.
- Si "detachstate" = PTHREAD_CREATE_JOINABLE establece que el hilo estará vinculado al hilo principal, por lo tanto no se liberan los recursos hasta que su padre use pthread_join().

```c
int pthread_attr_getdetachstate(pthread_attr_t *attr, 
								int *detachstate)
```
Obtiene el estado de separación actual del objeto de atributos de hilo especificado. Acepta dos argumentos: el objeto de atributos de hilo y un puntero a una variable que almacenará el estado de separación actual. 
- detachstate es la variable donde se almacenará el estado de desvinculación.



# Documentacion de semaforos
