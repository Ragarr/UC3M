# GRAFOS
index:
- saber que es un grafo y sus principales propiedades
- conocer el metodo de implemetnacion, que no la implementacion 
## DEFINICION
Un grafo es un conjunto de datos conectados entre si con cualquier tipo de conexion
los nodos se llaman nodo o vertices y los punteros aristas.

Un grafo es un conjunto de vertices y aristas.
V={v1,v2,v3,v4,v5,v6,...}
son pares de vertices
A= {(v1,v2),(v1,3)...)}
si todos los pares son de la forma {(v1,v2),(v2,v1)} es un grafo no dirigido, si no todos los pares tienen su inversa es un grafo dirigido.

En un grafo no ponderado todas las aristas tienen el mismo peso, en un grafo ponderado cada arista tiene su propio peso.

un grafo simple no tiene bucles, no tiene aristas paralelas.
un grafo simple dirigido solo puede tener (numero de aristas = n) n(n-1) aristas, si no es dirigido puede tener (n(n-1))/2.

un grafo denso es el que tiene muchas aristas para el conjunto total de nodos.

un nodo escaso es que tiene casi las mismas aristas que vertices.

un camino se representa como una secuencia de vertices por los que se pasa.
un camino simple es aquel que no repite vertices e su recorrido.

en realidad para los enlaces se usa una matriz de n*n con valor True si esta vinculado False si no, este metodo es bueno para grafos densos(tiene una complejidad espacial cuadratica y una temporal de n), si el grafo es escaso mejor usamos otras cosas.

si tenemos un grafo escaso es mejor crear una lista con las adyacencias (es lo mismo pero solo pongo los que estan conectados en vez de todos), la ocplejidad espacial es n si es escaso aun que tiende a n2 si el grafo es denso.
## IMPLEMENTACION
nosotros implementamos con diccionarios, de la forma:
graph= {'nodo':[lista de aristas (vertices con los que es adyacente)]}
si es un grafo ponderado, el dic tiene:
graph= {'nodo':[(vecino, peso),(vecino2, peso)]} tambien se hace creando clase vertice

## Recorridos
que recorridos vamos a ver?
- recorrido en amplitud (BFS)
- recorrido en profundidad (DFS)

### BFS
visito el nodo y los que estan conectados a el con una arista, luego cogo el primero que he visitado y que repito el algoritmo, etc.
implementacion con colas
### DFS
Visito primero los vecinos del nodo hasta que no tiene mas aristas.
implementacion con colas

## Algoritmo de Dijkstra
