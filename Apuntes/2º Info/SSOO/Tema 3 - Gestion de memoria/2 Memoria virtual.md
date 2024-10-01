La memoria virtual sirve para que muchos procesos (que cada vez necesitan más memoria) puedan funcionar a la vez en la RAM. Ej.: cada proceso tiene 2 Gbytes y hay 1024 procesos por máquina, necesitamos 2 Tbytes…
Con MV. el SO ofrece al proceso un mapa lógico de 2 Gbytes y el gestor de memoria reparte la RAM entre los procesos según se necesita dándoles páginas de forma dinámica en la RAM.

SO mantiene una Tabla de Páginas (TP) por cada proceso.
```
TP es una estructura de datos que se utiliza para almacenar la información de la memoria virtual de un proceso
```
De tal manera que en función del contexto se notifica a la MMU (mem. Manager unit) de qué dirección física debe usar `[P,Dp] → [Df]`.
- El SO mantiene una única TP para el propio SO
- Un proceso en modo usuario solo puede acceder a su TP (SO puede acceder a todas las TP)
- Un proceso en modo sistema puede acceder a su TP y a la del SO (Los procesos comparten mapa del sistema operativo)

# Niveles de Jerarquía de memoria 
- M. Secundaria
	- Componente único con multiplexación espacial (se guarda múltiple info en un mismo canal)
	- Traducción: t. regiones y páginas, no jerarquía de traducción
- M. Principal
	- Componente único con multiplexación espacial/temporal
	- Traducción: t. páginas, jerarquía de traducción (TP/TLB)
		- TLB con o sin PID. En MP una TLB/CPU
```
TLB (Translation Lookaside Buffer) es un caché de traducción de direcciones que se utiliza para mejorar el rendimiento de la memoria virtual. Es un tipo de memoria caché que almacena las traducciones de direcciones virtuales a direcciones físicas. ¿Te gustaría saber más sobre algún tema en particular?
```
- Memoria caché (en general N niveles)
	- Puede tener N componentes (MP o caché de I/D separadas)
	- No jerarquía de traducción. Dos esquemas de traducción:
		- virtual: ID lógico; acceso TLB y caché en paralelo: con o sin PID
		- física: ID físico; acceso TLB y caché no en paralelo

# Gestión de memoria del SO
Gestión de la memoria física: 
En iniciación SO recibe información de memoria física y crea la tabla de marcos.
Gestión del mapa del SO:
- Fase inicial: SO crea e inicia TP del sistema 
	- SO contiguo en memoria → uso de superpáginas
- Fase estable: Marcos restantes para procesos y SO
	- Para SO: asociación de marco con mapa SO
	- Para proceso: asociación con mapa usuario + asociacion temporal de SO
	- Alternativa: mapa de SO incluye toda memoria física, no requiere asociación temporal pero es menos flexible

# Fundamentos de la MV
M. virtual: SO gestiona niveles de m. principal y m. secundaria
- Sube por demanda; Baja por expulsión

Aplicable por proximidad de referencias:
- Procesos solo usan parte de su mapa en intervalo de tiempo 
- Parte usada (conjunto de trabajo) en m. principal (conjunto residente)
Beneficios:
- Aumenta el grado de multiprogramación
- Permite ejecución de programas que no quepan en mem. Principal

Basada en paginación: Uso del bit de validez
- Página no residente se marca como no válida
- En acceso: Excepción de fallo de página
# SWAP
El intercambio (swapping) consiste en reservar espacio en disco para almacenar las páginas de procesos en ejecución que no caben en memoria.
Disco (swap): respaldo de memoria 
- Swap out: expulsa/suspende proceso (al disco) si no hay sitio
	- Hay diversos criterios para expulsar: mejor si bloqueado
- Swap in: reanudación de proceso expulsado (y listo)
## Preasignacion del swap 
- Si se hace preasignacion del swap para cada página nueva se le asigna una página de swap: Tamaño M. Virtual = Swap
- Si no se hace preasignacion del swap solo swap para páginas que dan fallo
	- Tamaño M. Virtual = RAM + Swap
## Ciclo de vida de una página privada en fichero
![[Pasted image 20230414115002.png]]
## Fallo de página
- Si dirección inválida ⇾ Aborta proceso o le manda señal.
- Si no hay ningún marco libre (consulta T. marcos) 
	- Reemplazo: pág. P marco M → P inválida
- Hay marco libre (se ha liberado o lo había previamente):
	- Inicia lectura de página en marco `M
	- Conecta entrada de TP a `M
- Fallo de página en modo sistema no siempre es error:
	- Acceso a página de usuario no residente
	- Página de SO no residente o propagar cambios mapa SO
- Prepaginación: trae páginas por anticipado (no por demanda)

## Política de reemplazo
Tipo de reemplazo: local o global, factores a tener en cuenta:
- Tiempo de residencia
- Frecuencia de uso
- *Frescura* de la página
También en caché de sistemas de ficheros
Objetivo: Minimizar la tasa de fallos de página.
- Poca sobrecarga y MMU estándar
Algoritmo óptimo (MIN): Irrealizable
- Página residente que tardará más en accederse
## Algoritmo LRU
- Página residente menos recientemente usada (frescura)
- Proximidad de referencias: si se ha usado recientemente, posiblemente se use en el futuro próximo
- No anomalía de Belady(): algoritmo de pila
```
La anomalía de Belady es un fenómeno en el que aumentar el número de marcos de página en un sistema de memoria virtual puede aumentar la tasa de fallos de página. Esto va en contra de la intuición, ya que uno esperaría que tener más marcos de página reduciría la tasa de fallos de página. La anomalía solo ocurre en ciertos algoritmos de reemplazo de página, como el algoritmo FIFO (First-In, First-Out).
```
- Difícil implementación estricta (hay aproximaciones):
	- Precisaría una MMU específica
- Sí se usa como tal en caché de sistemas de ficheros
# Retención de páginas en memoria
Se pueden marcar como páginas no reemplazables, se aplica a páginas del propio SO `SO con páginas fijas en memoria es más sencillo`, También se aplica mientras se hace DMA (acceso directo) sobre una página. Servicio para fijar en memoria una o más páginas de su mapa:
- Adecuado para procesos de tiempo real
- Puede afectar al rendimiento del sistema
- En POSIX el servicio `mlock`
# Política de reparto de espacio
## Estrategia de asignación fija (reemplazo local)
La estrategia de asignación fija implica que el número de marcos asignados a un proceso es constante. Esto significa que el conjunto residente de un proceso no cambia durante su ejecución. 
Esta estrategia no se adapta a las distintas fases del programa, pero tiene un comportamiento relativamente predecible. 
La arquitectura del sistema impone un número mínimo de marcos que deben asignarse a cada proceso.
## Estrategia de asignación dinámica
La estrategia de asignación dinámica implica que el número de marcos asignados a un proceso varía según su evolución.
Cuando se combina con el reemplazo local, esta estrategia tiene un comportamiento relativamente predecible. Sin embargo, cuando se combina con el reemplazo global, su comportamiento es difícilmente predecible.

# Hiperpaginación (Thrashing)
La hiperpaginación (thrashing) se refiere a una situación en la que hay una tasa excesiva de fallos de página en un proceso o en el sistema. Esto puede ocurrir tanto con la asignación fija como con la asignación variable de memoria. En el caso de la asignación fija, la hiperpaginación ocurre en el proceso, mientras que en el caso de la asignación variable, ocurre en el sistema.
![[Pasted image 20230414123348.png]]
