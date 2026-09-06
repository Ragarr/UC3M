# Funciones
- S.O. multiplexa recursos entre procesos
	- Cada proceso cree que tiene una máquina para él solo. 
	- Gestión de procesos: Reparto de procesador. 
	- Gestión de memoria: Reparto de memoria.
- Objetivos:
	- Ofrecer a cada proceso un [[1 Gestor de memoria#Espacios logicos independientes|espacio lógico propio]]. 
	- Proporcionar [[1 Gestor de memoria#Protección de espacios de memoria|protección entre procesos]].
	- Permitir que los procesos [[1 Gestor de memoria#Comparticion de memoria|compartan memoria]]. 
	- Dar soporte a las [[1 Gestor de memoria#Regiones de memoria|regiones del proceso]]. 
	- Maximizar el grado de [[1 Gestor de memoria#Paginación|multiprogramación]]. 
	- Proporcionar a los procesos mapas de memoria muy grandes.

## Espacios lógicos independientes
El programa no conoce en que posición de memoria se ejecutara y genera referencias entre 0 y N. El sistema Operativo debe poder acceder a los espacios lógicos de los procesos.
En un sistema operativo multiprogramado, no se pueden colocar todos los programas a partir de la misma dirección de memoria física (p. ej. 0), por lo tanto, es necesario poder reubicar un programa a partir de una dirección de memoria física.
- Reubicación: Traducción de direcciones lógicas en direcciones físicas.
Las **dir. lógicas** son las direcciones de memoria generadas por el programa.
Las **dir. físicas** son las direcciones de memoria principal asignadas al proceso.
Ejemplo: Programa tiene asignada memoria a partir de 10.000, entonces a las direcciones logicas que genera el programa se le debe sumar 10.000.
Hay dos formas de reubicar las direcciones, Reubicación hardware y reubicación software.
## Reubicación Hardware
El hardware (MMU) es el encargado de la traducción. 
El SO se encarga de Almacenar por cada proceso su función de traducción y especifica al hardware que función aplicar a cada proceso.
## Reubicación Software
Se realiza la traducción de direcciones durante la carga del programa, por lo tanto la imagen en memoria del programa es distinta al ejecutable, desventajas:
- No asegura protección.
- No permite mover el programa en tiempo de ejecución.

# Protección de espacios de memoria 
En multiprogramación el SO debe asegurarse de que unos programas no invaden la memoria de otros, en consecuencia, en la traducción se deben crear espacios disjuntos. 
Es necesario validar todas las direcciones que genera el programa (la detección la hace el hardware del procesador y el tratamiento lo hace el SO). 
Además, la traducción permite impedir que los procesos accedan directamente a dispositivos de E/S.

# Compartición de memoria
Permitir que las direcciones lógicas de 2 o más procesos se corresponden con misma dirección física (bajo el control del SO). Ventajas:
- Procesos ejecutando el mismo programa comparten su código
- Mecanismo de comunicación entre procesos muy rápido.
Dificultad: requiere asignación no continua de 
![[Pasted image 20230412173552.png]]

# Regiones de memoria
- Mapa de proceso no homogéneo
	- Conjunto de regiones con distintas características
	- Ejemplo: Región de código (texto) no modificable
- Mapa de proceso
	- Regiones cambian de tamaño (p. ej. pila)
	- Se crean y destruyen regiones
	- Existen zonas sin asignar (huecos)
- Gestor de memoria debe dar soporte a estas características:
	- Detectar accesos no permitidos a una región
	- Detectar accesos a huecos
	- Evitar reservar espacio para huecos
- El SO debe guardar una tabla de regiones para cada proceso
## Gestión de información sobre las regiones
Información sobre bloques y huecos almacenada Internamente o externamente.
Soluciones:
- Lista única 
- Múltiples listas con huecos de tamaño variable 
- Múltiples listas con particiones estáticas
- Sistema buddy binario (huecos: 2n) 
- Mapa de bits
## Asignación de bloques de tamaño variable
Problema:
- Al borrar y crear procesos se crean huecos de distinto tamaño.
Solución:
- Compactar memoria, es demasiado lento si la memoria es muy grande

### Algoritmos de asignación de espacio
\+ Eficientes: menos fragmentación
- El hueco que mejor ajuste (best fit).
	- Selección: comprobar todos u ordenados por tamaño 
- El hueco que peor ajuste (worst fit) 
	- Selección: comprobar todos u ordenados por tamaño 
- El primer hueco que ajuste (first fit) 
	- Suele ser la mejor política en muchas situaciones 
- El próximo hueco que ajuste (next fit) 
	- Variación del primero que ajuste. 
	- Busca a partir del último asignado.
\+ Rápidos: menos tiempo de búsqueda
## Asignación de bloques de tamaño fijo
Asignar hueco pedido (fragmentación externa)
- El SO solo ve bloques
- Los 10 restantes están “pedidos” para el SO
![[Pasted image 20230412175440.png]]

# Paginación
- Mapa de memoria del proceso dividido en páginas
- Memoria principal dividida en marcos
	- tamaño marco=tamaño página
- Tabla de páginas (TP):
	- Asocia página y marco que la contiene
- Normalmente espacio lógico ≥ físico
## Tamaño de la página
Condicionado por diversos factores contrapuestos:
debe ser:
- potencia de 2 y múltiplo de sector de disco.
- Entre 1K y 16K
	- Más pequeño: Menor fragmentación interna, mejor ajuste a conjunto de trabajo
	- Más Grande: Tablas más pequeñas, mejor rendimiento de disco, más fragmentación interna.
Lo fija el procesador, algunos permiten configurar distintos tamaños.
