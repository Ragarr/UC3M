import sys
class Graph():
    def __init__(self,labels):
        """uses a dictionary to represent the graph"""
        self.vertices={}
        for v in labels:
            self.vertices[v]=[]
       
    def addEdge(self, start, end):
        """adds an edge from start to end"""
        if start not in self.vertices.keys():
            return
        if end not in self.vertices.keys():
            return
        self.vertices[start].append(end)

    def minDistance(self, distances, visited): 
        """This functions returns the vertex (index) with the mininum distance. We 
        only consider the set of vertices that have not been visited"""
        # Initilaize minimum distance for next node 
        min = sys.maxsize 

        #returns the vertex with minimum distance from the non-visited vertices
        for i in self.vertices: 
            if distances[i] <= min and visited[i] == False: 
                min = distances[i] 
                min_index = i 
    
        return min_index 
    
    def minDistance(self, distances, visited): 
        """This functions returns the vertex (index) with the mininum distance. We 
        only consider the set of vertices that have not been visited"""
        # Initilaize minimum distance for next node 
        min = sys.maxsize 

        #returns the vertex with minimum distance from the non-visited vertices
        for i in self.vertices: 
            if distances[i] <= min and visited[i] == False: 
                min = distances[i] 
                min_index = i 
    
        return min_index

    def dijkstra(self,origin):
        visited={v:False for v in self.vertices.keys()}
        distance={v:sys.maxsize for v in self.vertices.keys()}
        previus={v:None for v in self.vertices.keys()}

        distance[origin]=0
        for _ in self.vertices.keys():
            current=self.minDistance(distance,visited)
            visited[current]=True
            for adj in self.vertices[current]:
                if not visited[adj] and distance[adj]>distance[current]+1:
                    distance[adj]=distance[current]+1
                    previus[adj]=current
        
        return previus

        


    def minimumPath(self,start,end): 
        """returns a list containing the minimum path from start to end"""
        if not start in self.vertices or not end in self.vertices:
            return []
        path = self.dijkstra(start)
        out=[end]
        current=end
        while out[-1]!=start:
            if current:
                out.append(path[current])
                current=path[current]
            else:
                return []
        out.reverse()
        return out if len(out)!=1 else []
            

        

                


