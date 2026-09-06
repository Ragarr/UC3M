from implementaciones.graph import *
from colas import Queue

class Graph2(Graph):
    def min_number_edges(self, start, end):
        if start not in self._vertices.keys() or end not in self._vertices.keys():
            print(start,'or', end, ' does not exist!')
            return 0
        if start == end:
            return 0
        visited = {}
        distance = {}
        for v in self._vertices:
            visited[v] = False
            distance[v] = 0
        Q = Queue()
        distance[start] = 0

        Q.put(start)
        visited[start] = True
        while not Q.empty(): # O(n)
            x = Q.get() #elimina el primer elemento de la cola y lo almacena en x
            for i in self._vertices[x]: # O(n^2) recorre todos los vertices adyacentes a x
                if visited[i.vertex] == False: # O(1) comprobamos que no hayan sido visitados previamente
                    Q.put(i.vertex) 
                    visited[i.vertex] = True
                    distance[i.vertex] = distance[x] + 1          
        return distance[end]
