# dijsktra
from graph import Graph, AdjacentVertex

class mygraph(Graph):
    def __init__(self, vertices, directed=True):
        super().__init__(vertices, directed)
    
    def minimun_path(self,a,b):
        """returns the minimun distance from point a to point b using dijkstra's
        algorithm"""
        
