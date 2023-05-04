# Creación de procesos
Los procesos pueden crear otros procesos mediante llamadas al sistema. Este proceso se puede repetir recursivamente creando una estructura familiar.

Cuando se crea un proceso el padre y el hijo continuan ejecutandose en paralelo o el padre espera a que alguno o todos sus hijos hayan terminado de ejecutarse.
El proceso hijo es un clon del padre (en cuanto a memoria).

## Asignacion de recursos al nuevo proceso
El padre debe repartir sus recursos con el proceso hijo o compartir todos o parte de ellos con él. Así se evita así que un proceso bloquee el sistema multiplicándose indefinidamente.

## Creación de procesos en UNIX
Un proceso hijo puede invocar una llamada al sistema **exec*()*** sustituyendo su imagen en memoria por un programa diferente.
![[Pasted image 20230316115320.png]]
El padre puede dedicarse a crear más hijos, o esperar a que termine el hijo. mediante wait() se saca al padre de la cola de listos hasta que el hijo termina.
## Copy on write (COW)
Fork es muy ineficiente pues se copian muchos datos que podrian compartirse, ademas si al final se carga otra imagen (exec) es todiabia peor.
Copy-on-Write es una técnica que retrasa o evita la copia de los datos al hacer el fork
- Los datos se marcan de manera que si se intentan modificar se realiza una copia para cada proceso (padre e hijo)
- Ahora fork() sólo copia la tabla de páginas del padre (no las páginas) y crea un nuevo BCP para el hijo
## Esquema de Fork:
![[Pasted image 20230316115638.png]]
## Esquema de exec:
![[Pasted image 20230316115725.png]]
# Terminación de procesos
Cuando un proceso termina todos los recursos asignados son liberados (memoria, ficheros abiertos, entradas en tablas,...) y el jernel notifica al proceso padre de que su hijo a terminado.
Un proceso puede terminar voluntariamente (llamando a exit) o involuntariamente (abortado por ctrl-c u otro proceso que haga kill).
Si un proceso termina puede que sus hijos no sean afectados o que terminen todos en cascada (VMS). En UNIX los procesis qe terminan pasan a depender de el proceso _init_ y el proceso finalizado pasa a estar en modo Zombie hasta que su padre recoje el codigo de finalización.

# Ciclo de vida de un proceso
![[Procesos#Ciclo de vida de un proceso]]
# Expulsion a disco (swap)
Cuando existen muchos procesos en ejecución el rendimiento puede bajar por [[Multitarea#Memoria en la multiprogramacion|hiperpaginacón]]. para evitarlo el SO expulsa procesos al area de intercambio del disco (de esta forma se introducen nuevos estados de procesos, Bloqueado y suspendido Y Listo y suspendido).
![[Pasted image 20230316120807.png]]
# Tipos de planificación
Hay tres niveles de planificación:
- a corto plazo: Selecciona el siguiente proceso
- a medio plazo: Selecciona que procesos se añaden o retiran de la memoria principal.
- a largo plazo: Realiza el control de admision de procesos a ejecutar

Luego hay 2 tipos de planificacion:
- No apropiativa: El proceso en ejecucion mientras lo desee
- Apropiativa: El SO puede expulsar a un proceso de la CPU
## Puntos de planificación
El SO tiene varios momentos donde decidir su planificación:
- Cuando un proceso se bloquea en espera de un evento
- Cuando se produce una interrupción
- Un procesa finaliza

## Colas de procesos
Los procesos listos para ejecutar se mantienen en una cola.
### Implementación
El SO mantiene diversas colas de procesos.
La cola esta formada por punteros al BCP

# Algoritmos de planificación
## Medidas
Los algoritmos se rijen por:
- Utilización de CPU
	- Porcentaje de uso de la CPU
	- **Maximizar**
- Productividad:
	- Numero de trabajos terminados por ud. de tiempo
	- **Maximizar**
- Tiempo de retorno $T_{q}$
	- Tiempo que esta un proceso en el sistema. Instante final ($T_{f}$) menos instante inicial ($T_{i}$).
	- **Minimizar**

- Tiempo de servicio (Ts): 
	- Tiempo dedicado a tareas productivas (cpu, entrada/salida). $T_{s}=T_{CPU}+T_{E/S}$
- Tiempo de espera (Te): 
	- Tiempo que un proceso pasa en colas de espera. Te = Tq – Ts ¨ 
- Tiempo de retorno normalizado (Tn): 
	- Razón entre tiempo de retorno y tiempo de servicio. Tn = Tq/Ts 
	- Indica el retardo experimentado.

#todo