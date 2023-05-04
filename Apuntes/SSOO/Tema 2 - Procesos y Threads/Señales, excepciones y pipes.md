Hola bebeeeee JAJAJAJAJA
Tqm, q tengas un buen dia. 
Ah y eres muy mono btw.

# Señales
Son un mecanismo para comunicar eventos a los procesos.
Las [[Excepciones]] son señales
Cuando un proceso recibe una señal la procesa **inmediatamente**
Cuando llega una señal el proceso puede:
- ignorar la señal, siempre que sea immune a la misma
- invocar la rutina de tratamiento por defecto
- invocar a una rutina de tratamiento propia
Permiten avisar a un proceso de la ocurrencia de un evento y reaccionar a dicho evento. Ejemplo:
- un proceso recibe la señal SIGCHLD cuando termina un proceso hijo
![[Pasted image 20230313110835.png]]
## Tratamiento
- El SO transmite las señales al proceso. El proceso debe estar preparado para recibirla. 
	- especificando ub precedimiento de señal con signaction
	- direccion de la rutina de tratamiento (nombre)
- Enmascarando la señal con sigprogmask
- ignorando la señal 
	- tratamiento con SIG_IGN
- si no esta preparado: accion por defecto (SIG_DFL)
	- el proceso, en general, muere.
	- Hay algunas señales que se ignoran o tienen otro efecto
- Para enviar una señal a un proceso: 
	- int kill(pid_t pid, int sig); 
- El servicio pause() para el proceso hasta que recibe una señal

## Enviar una señal
Para enviar una señal a un proceso: 
```int kill(pid_t pid, int sig); ```
-  CTRL-C -> SIGINT 
- CTRL-Z -> SIGSTOP
Un proceso se puede enviar una señal a sí mismo 
``` 
#include <signal.h>
int raise(int sig); 
```
el servicio pause() pausa el prrama hasta que recibe una señal cualquiera

## Lista de señales
El sistema operativo cuenta con un conjunto definido de señales 
- Archivo en “include”: signal.h 
Señales importantes: 
- SIGILL instrucción ilegal 
- SIGALRM vence el [[Temporizadores|temporizador]] 
- SIGKILL mata al proceso 
- SIGSGEV violación segmento memoria 
- SIGUSR1 y SIGUSR2 reservadas para el uso del programador.
![[Pasted image 20230313111707.png]]
## Servicios POSIX para la gestion de señales
int kill(pid_t pid, int sig);  
Envía al proceso "pid" la señal "sig“. 
- Casos especiales: 
	- pid=0 -> Señal a todos los procesos con gid igual al gid del proceso. 
	- pid < -1 -> Señal a todos los proceso con gid igual al valor absolute de pid.
int sigaction(int sig, struct sigaction *act, struct sigaction *oact) 
- Permite especificar la acción a realizar como tratamiento de la señal "sig” 
- La configuración anterior se puede guardar en “oact"
- /*act es la estructura que define como actuar
### Struct sigaction
```
struct sigaction { 
void (*sa_handler)(); /* Manejador */ 
sigset_t sa_mask; /* Señales bloqueadas */ 
int sa_flags; /* Opciones */ };
```
Manejador: 
- SIG_DFL: Acción por defecto (normalmente termina el proceso). 
- SIG_IGN: Ignora la señal. 
- Dirección de una función de tratamiento. 
Máscara de señales a bloquear durante el manejador. 
Opciones normalmente a cero.

## Conjuntos de señales
Por ejemplo para la mascara de señales bloqueadas.
signo es el numero identificativo de la señal

int sigemptyset(sigset_t * set); 
- Crea un conjunto vacío de señales. 
int sigfillset(sigset_t * set); 
- Crea un conjunto lleno con todas la señales posibles. 
int sigaddset(sigset_t * set, int signo); 
- Añade una señal a un conjunto de señales. 
int sigdelset(sigset_t * set, int signo);
- Borra una señal de un conjunto de señales.
int sigismember(sigset_t * set, int signo); 
- Comprueba si una señal pertenece a un conjunto.

Ejemplo:
Ignorar la señal SIGINT 
- Se produce cuando se pulsa la combinación de teclas Ctrl+C 
```c
struct sigaction act; 
act.sa_handler = SIG_IGN; 
act.flags = 0; 
sigemptyset(&act.sa_mask); 
Sigaction(SIGINT, &act, NULL);
```

Este código en C está configurando una acción para manejar la señal SIGINT (interrupción del teclado) usando la función `sigaction()`.

El código crea una estructura `struct sigaction` llamada `act`, que es utilizada para especificar la acción que debe tomar el programa cuando se recibe la señal SIGINT. Luego se configura `act.sa_handler` para que ignore la señal SIGINT, lo que significa que el programa no tomará ninguna acción cuando se reciba esta señal.

`act.flags` se establece en 0, lo que significa que no se están estableciendo banderas adicionales.

`sigemptyset(&act.sa_mask)` inicializa el conjunto de señales vacío, lo que significa que la acción especificada por `act.sa_handler` se aplicará sólo a la señal SIGINT y no a ninguna otra señal.

Finalmente, se llama a `sigaction()` con los siguientes argumentos: `SIGINT` como la señal a manejar, `&act` como la estructura que especifica la acción a tomar, y `NULL` como puntero a una estructura `struct sigaction` para almacenar la acción anterior de la señal (en este caso, no se necesita almacenar la acción anterior).

Ejemplo: Capturar SIGSEV
```c
/*Programa que provoca que se eleve la seneal SIGSEGV escribiendo en la posicion 0 de memoria la captura. */ 
#include … 
#include 
void capturar_senyal(int senyal){ 
	printf(“Error por ocupacion indebida de memoria\n");
	signal(SIGSEGV,SIG_DFL);
	} 
main(void){ 
	int *p; 
	signal(SIGSEGV,capturar_senyal); 
	printf ("Ya he colocado el manejador\n"); 
	p=0; 
	printf ("Voy a poner un 5 en la variable\n"); 
	*p=5; 
	}
```

# Temporizadores
El SO tiene un temporizador por cada proceso (caso UNIX)
Sirven para cuando se hace un sleep(tiempo); por ejemplo.
- Se mantiene en el BCP del proceso un contador del tiempo que falta para que venza el temporizador. 
- La rutina del sistema operativo actualiza todos los temporizadores. 
- Si un temporizador llega a cero se ejecuta la función de tratamiento.

En UNIX el sistema operativo envía una [[Señales, excepciones y pipes|señal]] SIGALRM al proceso cuando vence su temporizador.
## Servicios POSIX para temporizadores 
```int alarm(unsigned int sec);```
Establece un temporizador. 
-  Si el parámetro es cero, desactiva el temporizador.
Ejemplo: imprimir un mensaje cada 10 segundos:
```c
#include <signal.h>
#include <stdio.h>
void tratar_alarma(void) 
{
	printf("Activada \n");
}

int main() 
{
	struct sigaction act;    /* establece el manejador para SIGALRM */
	act.sa_handler = tratar_alarma;
	act.sa_flags = 0; /* ninguna acción especifica */
	sigaction(SIGALRM, &act, NULL);
	act.sa_handler = SIG_IGN; /* ignora SIGINT */
	sigaction(SIGINT, &act, NULL);
	for(;;)
	{ /* recibe SIGALRM cada 10 segundos */
		alarm(10);
		pause();
	}
}
```
# Excepciones
El hardware detecta condiciones especiales:
- Fallo de página, escritura a página de solo lectura, desbordamientos de pila, violación de segmento, syscall...
Transfiere control al SO para su tratamiento, que: 
- Salva [[Procesos#Información del proceso|contexto del proceso]] 
- Ejecuta rutina si es necesario 
	- Envía una señal al proceso indicando la excepción

# Redirecciones y pipes
## Redireccion
Son mecanismos utilizados para redirigir la entrada o salida de datos de una aplicación o proceso a otro destino. En un sistema operativo, la redirección puede ser realizada por la línea de comandos, el shell, o a través de programas específicos.
### Redireccion de entrada
La redirección de entrada se utiliza para redirigir la entrada de un archivo o dispositivo a un programa. Por ejemplo, si queremos ejecutar un programa que lee datos desde la entrada estándar (stdin) y queremos proporcionar los datos desde un archivo en lugar de escribirlos manualmente, podemos redirigir la entrada del programa al archivo con el comando "<" en la línea de comandos.
### Redireccion de salida
La redirección de salida se utiliza para redirigir la salida de un programa a un archivo o dispositivo en lugar de a la pantalla. Por ejemplo, si queremos guardar la salida de un programa en un archivo en lugar de que se muestre en la pantalla, podemos redirigir la salida del programa al archivo con el comando ">" en la línea de comandos.
## Pipes
 Las pipes se utilizan para pasar la salida de un proceso a la entrada de otro proceso, de modo que los datos se transmiten en tiempo real y sin necesidad de guardarlos en un archivo temporal.
 Las pipes se crean mediante el carácter "|" (pipe) en la línea de comandos o en el shell de un sistema operativo. 
 Ejemplo:
 Teniendo el siguiente archivo de texto f1.txt:
```txt
uno, dos, tres 
cuatro, cinco, seis 
siete, ocho, nueve 
diez, once, doce
```
y hacemos el siguiente comando:
```bash
head -3 f1 | tail -1
```
Ese comando hara lo siguiente, paso a paso:
1.  El comando ``head -3 f1`` muestra las **primeras tres líneas** del archivo "f1". Como el archivo "f1" tiene cuatro líneas, la salida del comando sería:
	```txt
	uno, dos, tres
	cuatro, cinco, seis, 
	siete, ocho, nueve`
	```
2. La pipe "|" se utiliza para redirigir la salida del comando anterior al siguiente comando. En este caso, la salida del comando "head -3 f1" se utiliza como entrada del comando "tail -1".
3. El comando "tail -1" muestra la última línea de su entrada. En este caso, la entrada es la salida del comando "head -3 f1". Por lo tanto, el comando "tail -1" muestra la última línea de esas tres líneas, que es:
	```txt
	siete, ocho, nueve
	```
Por lo tanto, en resumen, el comando "head -3 f1 | tail -1" muestra la tercera línea del archivo "f1", que es "siete, ocho, nueve".
## Descriptores y pipes
### Descriptores de fichero 
(no es muy importante/util)
El sistema operativo mantiene una tabla interna con la información real de contacto con los dispositivos y ficheros con los que los procesos piden comunicarse. Los descriptores de ficheros son el índice de la tabla que hay por proceso, cuyo contenido es a su vez el índice de la tabla interna del sistema operativo.
Cuando se pide un nuevo descriptor de ficheros (al abrir un fichero) se busca el primer hueco libre de la tabla del proceso y el índice de esa posición es el descriptor asignado.
Es decir, el sistema operativo tiene una tabla de ficheros. El proceso tiene una tabla interna de ficheros que ha abierto. el FD es el indice de la tabla interna, la cual te da el indice de la tabla del sistema.
### duplicacion de descriptores
la funcion `dup(fd);` crea un duplicado del descriptor del fichero, es decir hace que dos entradas distintas de la tabla interna del proceso apunten a la misma entrada de la tabla del sistema.
- `int dup(fd)` devuelve el nuevo descriptor del archivo

### Fork
Cuando se hace un fork se duplica la tabla de ficheros del proceso.

## Pipes
Una tubería es un fichero especial que se crea con la llamada al sistema pipe() Dicha llamada crea la tubería y reserva dos descriptores de ficheros: lectura y escritura
uso de pipe():
```C
int p[2];
pipe(p);
read(p[0],buffer,SIZE);
write( p[1], buffer, strlen(buffer));
```
crea dos descriptores que guarda en un array que se le pase como parametro. el primer descriptor es de SOLO lectura y el segundo de SOLO escritura.
### Fork
si creas una tuberia y haces un fork(); padre e hijo podran leer y escirbir en la misma tuberia.
### Ejemplo
```c
...
// creacion del pipe
int p1[2] ;
pipe(p1) ;
pid = fork();
if (0!=pid) {
	...
	// redireccion del padre
	close(1);
	dup(p1[1]);
	// limipeza del padre
	close(p1[1]) ;
	close(p1[0]);
	…
}
else {
	...
	// redireccion del hijo
	close(0);
	dup(p1[0]);
	// limpieza del hijo
	close(p1[0]);
	close(p1[1]);
	…
}
```
### Problemas de los pipes
- Semi-duplex: 
	- en un sentido: los datos son escritos por un proceso en un extremo de la tubería y leídos por otro proceso desde el otro extremo del mismo. 
- Solo se pueden u:lizar entre procesos emparentados, que tengan un ancestro en común. 
- La lectura es destruciva.


# Entorno de un proceso
Proxima clase :D


