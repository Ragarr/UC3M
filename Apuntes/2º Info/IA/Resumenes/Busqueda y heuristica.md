# Búsqueda
Consiste en encontrar la secuencia de operaciones que nos conducen de un estado inicial a un estado solución.
Cada problema puede tener distintas instancias, la instancia de un problema consiste en asignarle un estado inicial y estados objetivos (o función objetivo a veces).
En un problema de búsqueda se asume que el entorno es cerrado, con unas opciones discretas (fijas) y es determinista (no hay probabilidades).

## Representación de un problema de búsqueda
El problema se representa representan mediante un grafo, la búsqueda per se consiste en recorrer el grafo en un orden concreto. 
La búsqueda luego se representa como un árbol, si el grafo del problema tiene ciclos, el árbol de búsqueda es infinito. Los ciclos se pueden controlar evitando los estados repetidos en la búsqueda.

### Árbol
El nodo superior es el estado inicial, las acciones son aristas, los sucesores del nodo son aquellos estados a los que puedo llegar desde el estado actual y se conectan con aristas, los sucesores se procesan de izquierda a derecha (depende del algoritmo de búsqueda).
Ejemplo, 8-puzzle:
											![[Pasted image 20230521184214.png]]
### Propiedades de los árboles
- fr: Factor ramificación 
	- Número de opciones que tiene cada nodo
- p: Profundidad
	- Mínimo número de acciones hasta una solución desde un inicio dado.
- m: 
	- Máxima longitud de un camino.

## Comparar problemas
Se comparan mediante los siguientes parámetros
- **Completitud**: Encuentra una solución.
- **Optimalidad**: Encuentra la mejor solución.
- **Complejidad temporal**: Tiempo que tarda en función del tamaño del problema.
- **Complejidad espacial**: Memoria que requiere en función del tamaño del problema.
Las medidas siempre se calculan para el peor caso.

# Búsqueda sin información
En este tipo de búsqueda, el algoritmo explora el espacio de búsqueda sin tener en cuenta la información adicional que podría ayudar a encontrar una solución más rápidamente.
Se puede resolver con un algoritmo en amplitud o en profundidad.

### Amplitud
1. Crear lista ``ABIERTA`` con el nodo inicial`` I`` (estado inicial)
2. ``ÉXITO``=Falso
3. Hasta que ``ABIERTA`` esté vacía O ``ÉXITO``
4. Quitar de ``ABIERTA`` el primer nodo ``N``
5. Si N tiene sucesores ENTONCES EXPANDE(N):
	1. Generar los sucesores de ``N ``(sin repeticiones)
	2. Crear punteros desde los sucesores hacia ``N``
	3. Si algún sucesor es ``nodo meta``. Entonces ``ÉXITO``=Verdadero
	4. Si no Añadir los sucesores al final de ``ABIERTA``
6. Si ``ÉXITO`` ENTONCES ``Solución``=camino desde ``I`` a ``N`` por los punteros Si no ``Solución``=fracaso
Ejemplo, 8-puzzle:
![[Pasted image 20230521185134.png]]
#### Propiedades
- Completa. Si existe, encuentra siempre solución 
- Óptima. Encuentra siempre la solución menos profunda. Con costes uniformes, es la óptima. 
- El control de ciclos se introduce por eficiencia
Complejidad espacial y temporal $\approx O(fr^p)$

### Profundidad
Es muy básica aunque se puede retocar. Siempre expandes el nodo más a la izquierda, salvo que esté repetido.

### Profundidad con retroceso (backtracking)
RETROCESO significa que se vuelve al siguiente nodo en la lista ABIERTA si se da alguna de las siguientes circunstancias:
- No hay sucesores del nodo que se expande
- Control de ciclos:
	- En nodos ya generados
	- Sólo en lista ABIERTA
	- En camino actual: almacena y comprueba el camino actual, únicamente se evita expandir nodos que están repetidos en este camino

- Se ha llegado al límite de profundidad, (Profundidad con límite incremental: se va incrementando este límite).
- Se sabe que el estado no conduce a la solución: método de Ramificación y Poda (Branch and Bound).
#### Algoritmo
1. Crear lista ``ABIERTA`` con el nodo inicial ``I`` y su ``profundidad`` (0) 
2. ``ÉXITO``=Falso y ``M``=Profundidad Máxima 
3. Hasta que ``ABIERTA`` esté vacía O ``ÉXITO`` 
	1. Quitar de ``ABIERTA`` el primer nodo ``N`` de profundidad ``P`` Si (``P < M``) Y ``N`` tiene sucesores 
	2. Generar los sucesores de ``N`` (sin ciclos) 
	3. Crear punteros desde los sucesores hacia ``N`` 
	4. Si algún sucesor es nodo meta 
		- Entonces ``EXITO``=Verdadero 
		- Si no Añadir los sucesores al principio de ``ABIERTA`` con profundidad ``P``+1 
	5. Si ``EXITO`` Entonces ``Solución``=camino desde ``I`` a ``N`` por los punteros Si no ``Solución``=fracaso
#### Propiedades
- **No Completa**. No garantiza encontrar la solución. Pero se hace completa si se añade detección de ciclos y retroceso.
- **No Óptima**. Encuentra la solución más próxima a la rama por la que busca, no necesariamente la que se encuentra a menor profundidad.
- **Eficiente**, cuando la meta está alejada del estado inicial, o hay problemas de memoria
Complejidad espacial: $\approx O(fr·m)$
Complejidad temporal:  $\approx O(fr^m)$

# Búsqueda heurística
La búsqueda heurística es un método de búsqueda que utiliza conocimiento parcial sobre un problema para resolver problemas eficientemente en ese problema.
Las funciones heurísticas se representan como h(n) y se descubren resolviendo modelos simplificados del problema real.
Las heurísticas admisibles son aquellas que **nunca sobreestiman** el coste real $h^*(n)$ de alcanzar la solución desde el nodo n: $h(n) ≤ h^*(n)$.
Ejemplo, 8-puzzle:
**$h(n)$ es el número de casillas mal colocadas**.
![[Pasted image 20230521193915.png]]
$h(1)=4$
$h(n)$**'Manhattan', suma de las distancias de cada pieza a su destino.**
![[Pasted image 20230521194013.png]]
$h2(n) = 5$

## Algoritmo de escalada
El algoritmo de escalada es un algoritmo de búsqueda local que comienza en un nodo inicial y busca el mejor vecino en su vecindario. Si el mejor vecino es mejor que el nodo actual, se mueve al vecino y repite el proceso hasta que no haya un vecino mejor.
Necesita una función de evaluación que indique el mejor nodo y se puede intentar maximizar o minimizar la función.
### Algoritmo
1. ``N``=Estado-inicial 
2. ``EXITO``=Falso 
3. Hasta que ``camino_sin_salida(N) ``O ``EXITO`` 
	1. Generar los sucesores de ``N`` 
	2. SI algún sucesor es ``estado_final`` 
		- ENTONCES ``EXITO``=Verdadero 
		- SI NO 
			1. Evaluar cada nodo con ``f(n) ``
			2. ``N``=mejor sucesor 
4. Si ``ÉXITO`` 
	1. Entonces  ``solución``=camino desde nodo del Estado-inicial al nodo N por los punteros 
	3. Si no, ``Solución``=fracaso

### Problemas
Es un algoritmo *greedy* lo cual tiene los siguientes inconvenientes, se puede atascar:
- En máximos o mínimos.
- Si se encuentra una meseta.
- Si se encuentra un punto con varios máximos o mínimos locales.
Se puede solucionar con backtracking, dando más de un paso en cada iteración o con reinicios aleatorios.

### Propiedades
- **No completo**: no tiene por qué encontrar la solución
- **No óptimo**:  no siendo completo, tampoco se puede garantizar que sea óptimo
- **Eficiente**: rápido y útil si la función es monótona (de)creciente

## Algoritmo Primero el mejor
Utiliza una función heurística para evaluar los nodos y seleccionar el mejor nodo para expandir.
El algoritmo comienza en el nodo inicial y expande el nodo con la mejor evaluación heurística. Si el nodo expandido no es el objetivo, se expanden sus sucesores y se selecciona el mejor sucesor para expandir. El proceso continúa hasta que se encuentra el objetivo o no hay más nodos para expandir.
El algoritmo de primero el mejor es **completo y óptimo si la función heurística es admisible** y consistente.

## Algoritmo A*
Es una variación optimizada del algoritmo Dijkstra que permite estudiar los grafos de forma excepcional y tiene un rango de aplicación especial. 
Se utiliza para encontrar el camino más corto entre dos nodos de un grafo ponderado 
A* utiliza una función heurística para estimar el costo restante de llegar al nodo objetivo. La función heurística debe ser admisible, lo que significa que nunca puede sobreestimar el costo restante. 
A* es un algoritmo **completo y óptimo** si se cumple la condición de admisibilidad de la función heurística.
## Sobre la heuristica
Si una heuristica da un valor $h1(n)< h2(n)$ podemoi deceir que $h1(n)$ esta menos informada o mas relajada que $h2(n)$.
