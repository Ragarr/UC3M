from graph import Graph
from sys import maxsize
class MyGraph(Graph):
    def __init__(self, vertices, directed=True):
        super().__init__(vertices, directed)
    

            


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

print(g.minimumPath('A','F'))
