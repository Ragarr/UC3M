import random


class edge():
    def __init__(self, origin, destiny, weight=None,) -> None:
        self.weight=weight
        self.origin=origin
        self.destiny=destiny
        self.visited=False
    
    def __str__(self) -> str:
        return '{}->{}'.format(self.origin,self.destiny)


class graph():
    def __init__(self,directed=False,vertices:list=[]) -> None:
        self.graph={}
        self.directed = directed
        for i in vertices:
            self.graph[i]=[]
    def insert(self,vertex):
        self.graph[vertex]=[]

    def connect(self,vertex1,vertex2,weight=None):
        if vertex1==vertex2:
            return
        if self.directed:
            self.graph[vertex1].append(edge(vertex1,vertex2,weight))
        else:
            self.graph[vertex1].append(edge(vertex1,vertex2,weight))
            self.graph[vertex2].append(edge(vertex2,vertex1,weight))

    def __str__(self) -> str:
        text=''
        for k,v in self.graph.items():
            text+='{}:'.format(str(k))
            for edge in v:
                text += '{}, '.format(str(edge))
            text+='\n'
        return text

    def bfs(self,node):
        print(node)
        node.visited=True
        for i in self.graph[node]:
            if i.visited:
                pass
            else:
                self.bfs(i)
        node.visited=False

l=['A','B','C','D','E']    
g=graph(False,l)
print(g)
for i in range(10):
    g.connect(random.choice(l),random.choice(l))
print(g)