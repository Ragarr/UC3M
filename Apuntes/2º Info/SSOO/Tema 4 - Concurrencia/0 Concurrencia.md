- Concurrencia. 
- Condiciones de carrera.

# Concurrencia
## Tipos de concurrencia.
**Concurrencia aparente**:
- Hay más procesos que procesadores.
- Los procesos se multiplexan en el tiempo 
- Pseudoparalelismo.

**Concurrencia real**: 
- Cada proceso se ejecuta en un procesador. 
- Se produce una ejecución en paralelo. 
- Paralelismo real.

## Modelos de programación concurrente
- **Único Procesador**
	- El sistema operativo se encarga de repartir el tiempo entre los procesos (planificación expulsiva/no expulsiva).
- **Multiprocesador**
	- Se combinan paralelismo real y pseudoparalelismo. (Normalmente hay más procesos que CPU’s)
- **Sistema distribuido **
	- Varios computadores conectados por red

## Ventajas de la ejecución concurrente
1. Facilita la programación. 
	- Diversas tareas se pueden estructurar en procesos separados.
	- Servidor Web: Un proceso encargado de atender a cada petición. 
2. Acelera la ejecución de cálculos. 
	- División de cálculos en procesos ejecutados en paralelo. 
	- Ejemplos: Simulaciones, Mercado eléctrico, Evaluación de carteras financieras. 
3. Mejora la interactividad de las aplicaciones. 
	- Se pueden separar las tareas de procesamiento de las tareas de atención de usuarios. 
	- Ejemplo: Impresión y edición.
4. Mejora el aprovechamiento de la CPU. 
	- Se aprovechan las fases de E/S de una aplicación para procesamiento de otras

## Tipos de procesos concurrentes
- **Independientes**: procesos que se ejecutan concurrentemente pero sin ninguna relación. 
	-  No necesitan comunicarse. 
	- No necesitan sincronizarse. 
	- Ejemplo: Dos intérpretes de mandatos de dos usuarios ejecutados en distintos terminales.
- **Cooperantes:** Procesos que se ejecutan concurrentemente con alguna interacción entre ellos.
	- Pueden comunicarse entre sí. 
	- Pueden sincronizarse. 
	- Ejemplo: Servidor de transacciones organizado en proceso receptor y procesos de tratamiento de peticiones.

## Interacciones entre procesos:
- **Acceso a recursos compartidos**. 
	- Procesos que comparten un recurso. 
	- Procesos que compiten por un recurso. 
	- Ejemplo: Servidor de peticiones en la que distintos procesos escriben en un registro de actividad (log). 
- **Comunicación**. 
	- Procesos que intercambian información. 
	- Ejemplo: Receptor de peticiones debe pasar información a proceso de tratamiento de petición. 
- **Sincronización**.
	- Un proceso debe esperar a un evento en otro proceso. 
	- Ejemplo: Un proceso de presentación debe esperar a que todos los procesos de cálculo terminen.

# Condiciones de carrera
Cuando de varios programas que se ejecutan en paralelo dependen entre ellos, su resultado se vuelve impredecible, para eso existen las condiciones de carrera.
El funcionamiento de un proceso y su resultado debe ser independiente de su velocidad relativa de ejecución con respecto a otros procesos. Es necesario garantizar que el orden de ejecución no afecte al resultado

## Exclusión mutua y sección crítica

 **Sección crítica**: Es una sección de código que acede a un recurso compartido y que no puede ser ejecutada por más de un hilo o proceso simultáneamente. Es deci, una seccion de codigo que debe ser ejecutada en excusión mutua. 
 **Exclusión mutua**: Es una técnica que permite que dos o más procesos no puedan ejecutar simultáneamente una sección crítica.

### Problemas de la sección crítica
#### Interbloqueos
Se produce al admitirse exclusión mutua para más de un recurso. 
1. El proceso P1 entra en la sección crítica para el recurso A. 
2. El proceso P2 entra en la sección crítica para el recurso B. 
3. El proceso P1 solicita entrar en la sección crítica para el recurso B (queda a la espera de que P2 la abandone). 
4. El proceso P2 solicita entrar en la sección crítica para el recurso A (queda a la espera de que P1 la abandone).
5. **Todos están bloqueados**
#### Inanición.
Un proceso queda indefinidamente bloqueado en espera de entrar en una sección crítica.
1. El proceso P1 entra en la sección crítica del recurso A. 
2. El proceso P2 solicita entrar en la sección crítica del recurso A. 
3. El proceso P3 solicita entrar en la sección crítica del recurso A. 
4. El proceso P1 abandona la sección crítica del recurso A.
5. El proceso P2 entra en la sección crítica del recurso A. 
6. El proceso P1 solicita entrar en la sección crítica del recurso A. 
7. El proceso P2 abandona la sección crítica del recurso A. 
8. El proceso P1 entra en la sección crítica del recurso A.
9. …
10. El proceso P3 nunca consigue entrar e la seccion critica del recurso A
![[Pasted image 20230423205109.png]]

### Condiciones para la exclusión mutua
- Solamente se permite que un proceso pueda estar simultáneamente en la sección crítica de un recurso.
- No debe ser posible que un proceso que solicite acceso a una sección crítica sea postergado indefinidamente.
- Cuando ningún proceso esté en una sección crítica, cualquier proceso que solicite su entrada lo hará sin demora.
- No se puede hacer suposiciones sobre la velocidad relativa de los procesos ni el número de procesadores.
- Un proceso permanece en su sección crítica durante un tiempo finito.²

### Soluciones a la sección crítica → sincronización
Cualquier mecanismo que solucione el problema de la sección crítica debe proporcionar sincronización entre procesos.
- Cada proceso debe solicitar permiso para entrar en la sección crítica
- Cada proceso debe indicar cuando abandona la sección crítica
#### Alternativas de implementación
**Desactivar interrupciones**.
- El proceso no sería interrumpido. 
- Solamente sería válido en sistemas monoprocesador.
**Instrucciones máquina**. 
- Test and set o swap. 
- Implica espera activa. 
- Son posibles inanición e interbloqueo.
**Otra alternativa**: Soporte del sistema operativo.

#### Solución Peterson
SOLO para 2 procesos
1. Asume que instrucciones LOAD y STORE son atómicas, no interrumpibles.
2. Los 2 procesos comparten 2 variables: `int turno`;  `Boolean flag[2]`
	- Turno: indica quien entrará en la sección crítica.
	- Flag: indica si un proceso está listo para entrar en la sección crítica.
		- `flag[i] = true` implica que $P_{i}$ está listo.

```
do { 
	flag[i] = TRUE; 
	turn = j; 
	while (flag[ j ] && turn == j); 
		critical section 
	flag[ I ] = FALSE; 
		remainder section 
} while (TRUE);
```
## Semáforos
Sincronización de procesos mediante un mecanismo de señalización-> semáforo.
Se puede ver un semáforo como una variable entera con tres operaciones asociadas. 
- Iniciación a un valor no negativo. 
- `semWait`: Decrementa el contador del semáforo. n Si `s<0` -> El proceso se bloquea.
- `semSignal`: Incrementa el valor del semáforo. n Si `s<=0`, -> Desbloquea un proceso.
### Secciones críticas y semáforos
```
Código no crítico 
… 
semWait(s); 
Código de sección crítica 
semSignal(s); 
… 
Código no crítico
```
![[Pasted image 20230423210327.png]]
- Rojo: sección crítica
- Azul: sección no crítica.
- Blanco: parado

### Problema lector escritor
Los lectores tienen prioridad. Si hay algún lector en la sección crítica, otros lectores pueden entrar. Un escritor solamente puede entrar en la sección crítica si no hay ningún proceso. El problema es la inanición para escritores. Los escritores tienen prioridad. Cuando un escritor desea acceder a la sección crítica no se admite la entrada de nuevos lectores.

Código **lector**
```c
for(;;) {
	semWait(lec);
	nlect++; 
	if (nlect==1) 
		semWait(escr); 
	semSignal(lec); 
	realizar_lect(); 
	semWait(lec); 
	nlect--; 
	if (nlect==0) 
		semSignal(escr); 
	semSignal(lec); 
}
```
Código **escritor**
```
for(;;) { 
	semWait(escr); 
	realizar_escr(); 
	semSignal(escr); 
}
```

### Problema del productor consumidor
Un proceso produce elementos de información (productor). Otro proceso consume elementos de información(consumidor). Se tiene un espacio de almacenamiento intermedio.
```c
for (;;) { 
	x= producir(); 
	semWait(s); 
	v[fin] = x; 
	fin++; 
	semSignal(s); 
	semSignal(n) 
} 
```
```c
int m; 
for (;;) { 
	semWait(n); 
	semWait(s); 
	y=v[inicio]; 
	inicio++; 
	semSignal(s); }
```
