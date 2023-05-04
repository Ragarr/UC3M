 import copy
from graph import Graph, AdjacentVertex
import random
g=Graph([1,2,3,4,5,6,7,8,9])

for i in range(15):
    g.add_edge(random.randint(1,9),random.randint(1,9))

print(g._vertices)

# distances es una lista de diccionarios que contiene la distancia de cada vertice a start y su vertice predecesor
# distances=[{vertex: [float('inf'), None]} for vertex in self._vertices.keys()]
g2= copy.deepcopy()

'''visited_vertices = []
        for vertex in self._vertices.keys():
            distances = {vertex: [str('inf'), None]}
        distances[start]=[0,None]
        current=start
        for AdjVertex in self._vertices[current]:
            visited_vertices.append(current)
            if distances[AdjVertex.vertex][0] > 1+distances[distances[AdjVertex.vertex][1]][0]: # la distancia del anterior + 1
                distances[AdjVertex.vertex] = [1+distances[distances[AdjVertex.vertex][1]][0],distances[AdjVertex.vertex][1]]'''


'''
D={}
for vertex in self._vertices.keys():
    if vertex == start:
        D[vertex]=[0,None]
    else:
        D[vertex]=[float('inf'),None]
D[start]=[0,None]
cola = Queue()
current=start
while current:
    for edge in self._vertices[current]:
        cola.put(edge)
    while not cola.empty():
        vertex=cola.get()
        if D[vertex][1]==None: # not visited yet from this node
            D[vertex]=[1+D[current][0],current]
        
        elif D[vertex][0]>D[D[vertex][1]][0]+1: # visited and newer distance is shorter
            D[vertex]=[D[D[vertex][1]][0]+1,D[vertex][1]]
    nearest=[float('inf'),None]
    for k,v in D.items():  
        if v[0]<nearest[0]:
            nearest=[v[0],k]
    return self._min_number_edges()
'''