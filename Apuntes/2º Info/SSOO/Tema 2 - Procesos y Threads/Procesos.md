Un proceso es un programa en ejecución. Cada ejecución de un programa da lugar a un proceso.
El proceso → unidad de procesamiento que gestiona el sistema operativo.
Un mismo programa puede dar a varios procesos (ejecutandolo dos veces por ej.)

Un proceso está formado por: 
- Código del programa: Instrucciones. 
- Conjunto de datos asociados a la ejecución del program

# Ciclo de vida de un proceso
Un proceso puede estar en 3 estados:
- En ejecucion, esta haciendo operaciones y requiere un procesador
- Bloqueado, esta esperando una señal o una entrada, etc. No necesita un procesador por que no esta haciendo nada.
- Listo, no se esta ejecutando pero ya no esta bloqueado y puede ejecutarse en cualquier momento
![[Pasted image 20230314205612.png]]

# Información del proceso
Tres categorías: 
- Información almacenada en el procesador. 
- Información almacenada en memoria. 
- Información adicional gestionada por el sistema operativo.

**Tablas del sistema operativo**
Tabla de procesos

| BCP Proceso A        | BCP Proceso B        | BCP Proceso c        |
| -------------------- | -------------------- | -------------------- |
| Estado(registros)    | Estado(registros)    | Estado(registros)    |
| Identificacion (pid) | Identificacion (pid) | Identificacion (pid) |
| Control              | Control              | Control              | 
Luego el sistema tiene otras tablas como la tabla de memoria, tabla de E/S o tabla de ficheros
![[Pasted image 20230314213548.png]]
## Estado del procesador (registros)
Incluye los valores de los registros del procesador:
Registros accesibles en modo usuario:
- Registros generales: Bancos de registros. 
- Contador de programa. 
- Puntero de pila. 
- Parte de usuario del registro de estado.
Registros accesibles en modo core:
- Parte privilegiada del registro de estado. 
- Registros de control de memoria (p.ej. RBTP).

Cuando el SO cambia de un proceso a otro debe hace un [[Cambio de contexto]]. Grardar todo el estado de procesador del proceso saliente y restaurar estado del procesador de proceso entrante.

## Imagen de memoria de un proceso

La imagen de memoria está formada por los espacios de memoria que un proceso está autorizado a utilizar.
Si un proceso genera una dirección que esta fuera del espacio de direcciones el HW genera un trap (cuando C da un error por un puntero fuera de memoria o etc).
### Modelos de imagen de memoria
#### Region única
Proceso con única región de tamaño fijo:
- Usado en sistemas sin memoria virtual.

Proceso con única región de tamaño variable:
- Sistemas sin memoria virtual: 
	- Necesita espacio de reserva ➔ Desperdicio de memoria. 
- Sistemas con memoria virtual: 
	- Espacio de reserva virtual ➔ Factible pero menos flexible que múltiples regiones.

#### Regiones múltiples
Proceso con un número variable de regiones de tamaño variable.
- Opción más avanzada (usada en versiones actuales de Windows y UNIX)
- Muy flexible: 
	- Regiones compartidas. 
	- Regiones con distintos permisos.

# Información del SO
El sistema operativo mantiene información adicional sobre los procesos en la Tabla de Procesos. 
## En el BCP
Un Bloque de control de Procesos (BCP) es cada entrada de la tabla que mantiene la información sobre un proceso y mantiene casi toda la info sobre un proceso:

**Información de identificación:**
-   Identificador de proceso (PID): Un número único que se asigna a cada proceso en el sistema.

**Estado del procesador:**
-   Contador de programa (PC): La dirección de la próxima instrucción que se ejecutará en el proceso.
-   Registros del procesador: Los valores actuales de los registros del procesador del proceso.

**Información de control del proceso:**
-   Estado del proceso: Indica si el proceso está en ejecución, suspendido o terminado.
-   Prioridad: Un valor que indica la importancia relativa del proceso en comparación con otros procesos en el sistema.
- Información de planificación.
-   Información de recursos: La cantidad de recursos del sistema (como la memoria, la CPU o los puertos de comunicaciones) que está utilizando actualmente el proceso.
-   Lista de archivos abiertos: Una lista de todos los archivos que el proceso tiene abiertos actualmente.
- Temporizadores
- ...

## Fuera del BCP
No toda la información referida a un proceso se almacena en el BCP.

### Tabla de paginas
Describe la imagen de memoria del proceso 
El BCP contiene el puntero a la tabla de páginas.

Razones:
- Tiene tamaño variable
- La compartición de memoria entre procesos requiere que sea externa al BCP

### Punteros de posición de los ficheros #wtf 
Si se añaden a la tabla de ficheros abiertos (en el BCP) no se pueden compartir.
Si se asocian al nodo-i se comparten siempre. 
Se ponen en una estructura común a los procesos y se asigna uno nuevo en cada servicio OPEN.

# Principios de la multitarea
Paralelismo real entre E/S y CPU (DMA: Acceso directo a memoria)
Alternancia en los [[Procesos]] de fases de E/S y de procesamiento
La memoria almacena varios procesos

Si hay un solo proceso hay mucho tiempo desperdiciado en E/S (franja amarilla):
![[Pasted image 20230314220816.png]]
En un sistema multitarea:
![[Pasted image 20230314221028.png]]
# Ventajas del multitarea
Facilita la programación, dividiendo los programas en procesos (modularidad).
Permite el servicio interactivo simultáneo de varios usuarios de forma eficiente.
Aprovecha los tiempos que los procesos pasan esperando a que se completen sus operaciones de E/S.
Aumenta el uso de la CPU.
# Multiprogramacion
El grado de multiprogramación es el numero de procesos activos. Cuanto mas grado de multiprogramacion hay mas se usa la CPU (mejor)
Necesidades de memoria principal: Sistema sin memoria virtual #wtf 
![[Pasted image 20230314221311.png]]
## Memoria en la multiprogramacion
Cuando tienes un sistema de memoria virtual (dividir la memoria en paginas) si tienes muchos procesos a cada uno le toca menos menos marcos de pagina.
Por lo tanto al aumentar el grado de multiprogramación: Desciende el tamaño del conjunto residente de cada proceso. Se produce [hiperpaginación](https://es.wikipedia.org/wiki/Hiperpaginaci%C3%B3n)antes de alcanzar un porcentaje alto de uso de CPU.
| Poca memoria fisica                  | Mucha memoria fisica                 |
| ------------------------------------ | ------------------------------------ |
| ![[Pasted image 20230314221953.png]] | ![[Pasted image 20230314222012.png]] |

Un cambio de contexto en sistemas operativos (SSOO) ocurre cuando el sistema cambia de la ejecución de un proceso a la ejecución de otro proceso. En otras palabras, cuando el procesador deja de ejecutar un proceso en particular y cambia su atención a otro proceso, se produce un cambio de contexto.
Durante un cambio de contexto, el sistema operativo guarda el estado actual del proceso que está siendo interrumpido, como los valores de los registros y los punteros de la pila, en la memoria y luego carga el estado del siguiente proceso que se va a ejecutar en la CPU. Esto permite que el sistema operativo cambie entre procesos y ofrezca la apariencia de que varios procesos están ejecutándose simultáneamente.
Los cambios de contexto son necesarios para permitir la [[Multitarea]] en los sistemas operativos, donde se pueden ejecutar varios procesos en la CPU al mismo tiempo.
Existen los cambios de contexto voluntarios e involuntarios:
**Cambio de contexto voluntario (C.C.V): **
- Proceso realiza llamada al sistema (o produce una excepción como un fallo de página) que implica esperar por un evento.
- Ejemplos: leer del terminal, fallo de página.
**Cambio de contexto involuntario (C.C.I):** 
- SO quita de la CPU al proceso (forzando su estado de En ejecución → listo) 
- Ejemplos: fin de rodaja de ejecución o pasa a listo proceso bloqueado de mayor prioridad

# Generación de ejecutables
La generación de ejecutables es el proceso mediante el cual se crea un archivo ejecutable a partir del código fuente de un programa. Este archivo es el que se carga en la memoria y se ejecuta en el sistema operativo.

El proceso de generación de ejecutables consta de varios pasos:
1.  Preprocesamiento: En esta etapa, el preprocesador examina el código fuente y realiza tareas como la inclusión de archivos de cabecera y la expansión de macros.
2.  Compilación: En esta etapa, el compilador traduce el código fuente a lenguaje de máquina. El resultado de esta etapa es un archivo objeto que contiene código máquina para las funciones y variables definidas en el código fuente.
3.  Enlazado: En esta etapa, el enlazador combina los archivos objeto generados en la compilación con las bibliotecas necesarias y genera un archivo ejecutable. Durante este proceso, el enlazador resuelve las referencias entre los archivos objeto y las bibliotecas y genera una tabla de símbolos que se utiliza para ubicar las funciones y variables necesarias en el archivo ejecutable.
4.  Empaquetado: En esta etapa, el archivo ejecutable se empaqueta en un formato adecuado para su distribución y uso. Por ejemplo, en sistemas operativos como Windows, el archivo ejecutable se empaqueta en un archivo con extensión .exe.

# Editor de enlaces (linker)
El editor de enlaces o linker es un programa que se utiliza en el proceso de compilación de un programa para combinar varios archivos objeto y bibliotecas en un único archivo ejecutable o en una biblioteca compartida. El editor de enlaces es una herramienta importante en el proceso de generación de ejecutables.
El editor de enlaces es responsable de resolver las referencias entre los diferentes archivos objeto y bibliotecas y de generar una tabla de símbolos que se utiliza para ubicar las funciones y variables necesarias en el archivo ejecutable o biblioteca compartida. Además, el editor de enlaces también puede realizar optimizaciones, como la eliminación de código redundante y la resolución de referencias a funciones inlining.
# Formato ELF
ELF (Executable and Linkable Format) es un formato de archivo comúnmente utilizado en sistemas operativos tipo Unix, como Linux, para representar ejecutables, bibliotecas compartidas y archivos objeto.
Fue diseñado para ser independiente del procesador y del sistema operativo, lo que significa que el mismo archivo ELF puede ser ejecutado en diferentes sistemas y arquitecturas. Además, el formato ELF permite la separación entre el código y los datos, lo que permite la asignación dinámica de memoria y la carga y descarga de bibliotecas compartidas durante el tiempo de ejecución.
Consta de un encabezado que describe la estructura del archivo, seguido de secciones que contienen el código, los datos y los símbolos utilizados en el programa. 
![[Pasted image 20230315213446.png]]
# Ejemplo de generacion de un ejecutable a partir de un archivo en C #wtf 
Supongamos el siguiente codigo
```c
# include <stdio.h>
int main()
{
    printf( "Hola mundo." );
    return 0;
}
```
El proceso de compilación y enlazado saeria el siguiente:
1.  Preprocesamiento: El preprocesador del compilador de C (gcc) procesa el archivo fuente, resuelve las directivas de preprocesador(def abajo) y genera un "**archivo preprocesado**". En el caso de nuestro ejemplo, el archivo preprocesado incluirá la cabecera stdio.h.
2.  Compilación: el compilador de C (gcc) convierte el archivo preprocesado en un **"archivo objeto"**. El archivo objeto contiene el código compilado, que aún no es un archivo ejecutable. En este paso, el compilador genera código de máquina a partir del código C del archivo preprocesado y guarda el resultado en el archivo objeto.
3.  Enlazado: La última fase del proceso es el enlazado, que combina el archivo objeto generado en la fase de compilación con las bibliotecas necesarias para generar un archivo ejecutable. En nuestro ejemplo, la biblioteca stdio.h es necesaria para usar la función printf(). El enlazador del compilador (ld) resuelve las referencias a las funciones de la biblioteca stdio.h y las vincula con el código compilado de la función main(). En este paso, también se realiza la optimización y se genera el archivo ejecutable. El resultado final es un archivo ejecutable que muestra "Hola mundo." en la salida estándar.
