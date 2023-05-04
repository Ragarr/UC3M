from graph import Graph
from sys import maxsize


class Graph2(Graph):
    def min_number_edges(self, start: str, end: str) -> int:
        """returns the minimum number of edges from start to end, kind of dijskstra without weights"""
        visited = {}
        distances = {}
        for v in self._vertices.keys():
            visited[v] = False
            distances[v] = maxsize
        distances[start] = 0

        for n in range(len(self._vertices)):
            current = self.__closer_vertex(visited, distances)
            visited[current] = True

            for adjV in self._vertices[current]:
                v = adjV.vertex
                if visited[v] == False and distances[v] > distances[current]+1:
                    distances[v] = distances[current]+1
        
        return distances[end] if distances[end] != maxsize else 0

    def __closer_vertex(self, visited, distances):
        """This function is used by the min_number_edges function."""
        """ complexity: O(|V|)"""
        min = maxsize
        # buscamos cual es el vertice NO VISITADO mas cercano AL ORIGEN
        for vertex in self._vertices.keys():
            if distances[vertex] <= min and visited[vertex] == False:
                min = distances[vertex]  # update the new smallest
                min_vertex = vertex  # update the index of the smallest
        return min_vertex

    def transpose(self) -> 'Graph2':
        """returns a new graph that is the transpose graph of self"""
        """complexity: O(|V|+|E|)"""
        # we create a new graph to not modify the original
        new_graph = Graph2(self._vertices.keys())
        for current in self._vertices.keys():
            for edge in self._vertices[current]:
                new_graph.add_edge(edge.vertex, current, edge.weight)
        return new_graph

    def is_strongly_connected(self) -> bool:
        """This function checks if the graph is strongly connected.
        A directed graph is strongly connected when for any
        pair of vertices u and v, there is always a path from u to v.
        If the graph is undirected, the function returns True if the graph is
        connected, that is, there is a path from any vertex to any other vertex
        in the graph."""
        """ complexity: O(|V|+|E|)"""
        """si desde un vertice puedes alcanzar todos los vertices y desde el mismo 
        vertice en el grafo transpuesto tambien puedes alcanzar todos los vertices el grafo es fuertemente conexo"""

        # cojemos un origen cualquiera, es indiferente
        origin = list(self._vertices.keys())[0]
        visited = {v:False for v in self._vertices.keys()}  # almacenara los vertices visitados durante el DFS si un vertice no se visita es que es inalcanzable
        # comprobamos que vertice es alcanzable y cual no
        self.__DFS_aux(origin, visited)
        # comprobamos que todo sea true: todos son alcanzables
        if not all(visited.values()):
            return False
        if self._directed:
            aux = self.transpose()
            visited = {x: False for x in visited}
            # repetimos la busqueda
            aux.__DFS_aux(origin, visited)
            if not all(visited.values()):
                return False

        return True

    def __DFS_aux(self, vertex, visited: dict):
        """This function is used by the is_strongly_connected function."""
        """ complexity: O(|V|+|E|)"""
        visited[vertex] = True
        for adjV in self._vertices[vertex]:
            if not visited[adjV.vertex]:
                self.__DFS_aux(adjV.vertex, visited)
