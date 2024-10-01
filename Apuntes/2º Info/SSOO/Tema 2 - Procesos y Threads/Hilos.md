Los hilos son una especie de proceso pero mas lijero qe comparte mapa de memoria, ficheros abiertos, señales, temporizadores y semáforos con el resto de hilos del proceso.
# Beneficios
bla bla bla

# Modelos de hilos
## Muchos a uno
Hace corresponder múltiples hilos de usuario a un único hilo del núcleo.
En caso de llamada bloqueante se bloquean todos los hilos, en multiprocesadores no se pueden ejecutar varios hilos a la vez.

## Uno a uno
Hace corresponder un hilo del kernel a cada hilo de usuario.
Suele estar restringido el numero de hilos que se pueden crear.

## Muchos a muchos
Este modelo multiplexa los threads de usuario en un número determinado de threads en el kernel.
El núcleo del sistema operativo se complica mucho.

# Aspectos de diseño
## Llamadas a fork y exec
 Si se llama a fork desde un hilo o se duplica el proceso con todos sus hilos (mas apropiado) o se duplica un proceso solo con el hilo que llama a fork (mas eficiente).
 Para solucionar esto, en linux existen dos versiones de fork:
 - fork();-> crea una copia exacta del proceso actual, incluyendo todos los hilos que se estén ejecutando en ese momento.
 - clone(); -> permite que el proceso hijo comparta ciertos recursos, como el espacio de direcciones de memoria y el descriptor de archivos, con el proceso padre.

## Cancelacion de hilos
Situación en la que un hilo notifica a otros que deben terminar.
Hay dos opciones:
- **Cancelación asíncrona**: Se fuerza la terminación inmediata del hilo, lo cual genera problemas con los recursos asignados al hilo.
- **Cancelación diferida**: El hilo comprueba periódicamente si debe terminar.
`pthread__cancel();` manda una señal para la cancelación de un hilo.
 
## Procesamiento de solicitudes
Las aplicaciones que reciben peticiones y las procesan pueden usar hilos para el tratamiento.
- El tiempo de creación/destrucción del hilo supone un retraso (aunque sea menor que el de creación/destrucción de un proceso).
- No se establece un límite en el número de hilos concurrentes
- Si llega una avalancha de peticiones se pueden agotar los recursos del sistema.
### Thread pools
Se crea un conjunto de hilos que quedan en espera a que lleguen peticiones.
- Minimiza el retardo: El hilo ya existe.
- Mantiene un límite sobre el número de hilos concurrentes.
# Planificacón de hilos
La planificación de ejecución de threads se basa en el modelo de prioridades y no utiliza el modelo de segmentación por segmentos de tiempo (como los procesos).
Un thread continuará ejecutandose en la CPU hasta pasar a un estado que no le permita seguir en ejecución.
Si se quiere alternancia entre threads, se debe asegurar que el thread permite la ejecución de otros threads, por ejemplo usando sleep().

API permite especificar la planifiación (PCS o SCS) durante creación thread:
- PTHREAD_SCOPE_PROCESS: el thread usa planificación PCS
- PTHREAD_SCOPE_SYSTEM: el thread usa planificación SCS
Para usuarios, Linux y Mac OS X solo permiten PTHREAD_SCOPE_SYSTEM.

# Atributos de  hilos
Algunos de los atributos más importantes que se pueden establecer son los siguientes:
-  Detach state: Este atributo indica si un hilo es separable o no. Un hilo separable puede liberar sus recursos cuando finaliza sin necesidad de ser unido con pthread_join. En cambio, un hilo no separable debe ser unido con pthread_join para liberar sus recursos.
- Stack size: Este atributo establece el tamaño de la pila del hilo en bytes. La pila es el espacio de memoria utilizado por el hilo para almacenar variables y datos temporales. Si la pila es demasiado pequeña, se pueden producir errores de desbordamiento de pila.
-  Scope: Este atributo indica si un hilo es local o global. Un hilo local solo puede ser utilizado dentro de la función que lo crea, mientras que un hilo global puede ser utilizado en todo el programa.
-  Scheduling policy: Este atributo determina la política de planificación de los hilos. Hay varias políticas de planificación disponibles, como FIFO, RR (round-robin) y prioridad.
-  Priority: Este atributo establece la prioridad del hilo. Un hilo con una prioridad más alta se ejecuta antes que un hilo con una prioridad más baja. La prioridad se utiliza para determinar qué hilo se ejecuta primero en caso de que haya varios hilos listos para ejecutarse.
Todos estos atributos se modifican o se ven con:
`pthread_attr_[set|get]attrname();`
ejemplo: `pthread_attr_setdetachstate()`