from numpy import minimum
from graph import Graph
from sys import maxsize

class MyGraph(Graph):
    def __init__(self, vertices, directed=True):
        super().__init__(vertices, directed)
    

    def closer_vertex(self,origin,visited,distances):
        min=maxsize
        for vertex in self._vertices.keys():
            if distances[vertex] <= min and visited[vertex] == False:
                min = distances[vertex]  # update the new smallest
                min_vertex = vertex  # update the index of the smallest

        return min_vertex


    def dijkstra(self,start,end):
        distances={v:maxsize for v in self._vertices.keys()}
        visited={v:False for v in self._vertices.keys()}
        previus={v:None for v in self._vertices.keys()}
        
        distances[start]=0

        for _ in self._vertices.keys():
            u=self.closer_vertex(start,visited,distances)
            visited[u]=True
            for e in self._vertices[u]:
                if distances[e._vertex]>distances[u]+1:
                    distances[e._vertex]=distances[u]+1
                    previus[e._vertex]=u
        return previus # devolvemos el valor q(≧▽≦q)

        
    def minimumPath(self,start,end):
        paths=self.dijkstra(start,end)
        current=end
        out=[]
        while current!=start:
            out.append(current)
            current=paths[current]
        return out


labels=['A', 'B', 'C', 'D', 'E','F','G']    
# Create a given graph  
g = MyGraph(labels)  
g.addEdge('A', 'B')
g.addEdge('B', 'C')
g.addEdge('B', 'D')
g.addEdge('B', 'E')
g.addEdge('C', 'E')
g.addEdge('D', 'E')
g.addEdge('E', 'F')
g.addEdge('G', 'D')

print(g)

print(g.minimumPath('A','B'))