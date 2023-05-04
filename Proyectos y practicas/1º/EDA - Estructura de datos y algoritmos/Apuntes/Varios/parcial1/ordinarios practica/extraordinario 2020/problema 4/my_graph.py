from dis import dis
from locale import currency
from graph import Person, Contacts
from sys import maxsize
import os

class contacts2(Contacts):
    def __init__(self):
        super().__init__()
    
    def getSuggestions(self,p:Person, minimumJumps:int):
        visited={v:False for v in self.vertices}
        distances={v:maxsize for v in self.vertices}
        distances[p]=0

        for n in range(len(self.vertices)):
            current = self.__closer_vertex(origin=p,visited=visited, distances=distances)
            visited[current] = True
            for adjV in self.vertices[current]:
                if visited[adjV] == False and distances[adjV] > distances[current]+1:
                    distances[adjV] = distances[current]+1
        out=[]
        for v in distances.keys():
            if distances[v]>= minimumJumps:
                out.append(v)
        os.system('cls')
        print({x.name:visited[x] for x in visited.keys()})
        print({x.name:distances[x] for x in distances.keys()})
        return out
    
    def __closer_vertex(self,origin,distances,visited):
        min = maxsize
        # buscamos cual es el vertice NO VISITADO mas cercano AL ORIGEN
        for vertex in self.vertices.keys():
            if distances[vertex] <= min and visited[vertex] == False:
                min = distances[vertex]  # update the new smallest
                min_vertex = vertex  # update the index of the smallest
        return min_vertex

#Create delivery points
pA=Person('Isa',666889900)             #A
pB=Person('Ana',666887700)
pC=Person('Bea',555887755)
pD=Person('Cris',333224411)
pE=Person('Joe',444887766)
pF=Person('JoseL',222776644)
pG=Person('Leo',322776644)
pH=Person('Fran',388776644)
pI=Person('Mia',388776644)
pJ=Person('Ruth',388776644)
pK=Person('Blas',388776644)
        

graph=contacts2()
persons=[pA,pB,pC,pD,pE,pF,pG,pH,pI,pJ,pK]
for p in persons:
    graph.addPerson(p)

         
graph.addConnection(pA,pB)      #Isa<->Ana
graph.addConnection(pA,pC)      #Isa<->Bea
graph.addConnection(pA,pD)      #Isa<->Cris

graph.addConnection(pB,pG)      #Ana<->Leo

graph.addConnection(pC,pD)      #Bea<->Cris

graph.addConnection(pD,pE)      #Cris<->Joe
graph.addConnection(pD,pF)      #Cris<->JoseL
graph.addConnection(pD,pH)      #Cris<->Fran

graph.addConnection(pF,pI)      #JoseL<->Mia

graph.addConnection(pG,pI)      #Leo<->Mia

graph.addConnection(pI,pJ)      #Mia<->Ruth

graph.addConnection(pJ,pK)      #Ruth<->Blas

#print(graph)

for p in persons:
    for i in range(1,5):
        print('sugestions for '+p.name+' con at least '+str(i)+':') 
        suggestions=graph.getSuggestions(p,i)
        print('\t',end=' ')
        if len(suggestions)==0:
            break
        for s in suggestions:
            print(s.name, end=' ')
        print()

import unittest


class Test(unittest.TestCase):
    


    #provisional mark
    mark=0

    def setUp(self):
        print('\ninitializing data...\n')
        
        #Create delivery points
        self.pA=Person('Isa',666889900)             #A
        self.pB=Person('Ana',666887700)
        self.pC=Person('Bea',555887755)
        self.pD=Person('Cris',333224411)
        self.pE=Person('Joe',444887766)
        self.pF=Person('JoseL',222776644)
        self.pG=Person('Leo',322776644)
        self.pH=Person('Fran',388776644)
        self.pI=Person('Mia',388776644)
        self.pJ=Person('Ruth',388776644)
        self.pK=Person('Blas',388776644)

        
        self.persons=[self.pA,self.pB,self.pC,self.pD,self.pE,self.pF,self.pG,self.pH,self.pI,self.pJ,self.pK]
        
        self.graph=contacts2()
        
        for p in self.persons:
            self.graph.addPerson(p)
            
    
        self.graph.addConnection(self.pA,self.pB)      #Isa<->Ana
        self.graph.addConnection(self.pA,self.pC)      #Isa<->Bea
        self.graph.addConnection(self.pA,self.pD)      #Isa<->Cris

        self.graph.addConnection(self.pB,self.pG)      #Ana<->Leo

        self.graph.addConnection(self.pC,self.pD)      #Bea<->Cris


        self.graph.addConnection(self.pD,self.pE)      #Cris<->Joe
        self.graph.addConnection(self.pD,self.pF)      #Cris<->JoseL
        self.graph.addConnection(self.pD,self.pH)      #Cris<->Fran

        self.graph.addConnection(self.pF,self.pI)      #JoseL<->Mia

        self.graph.addConnection(self.pG,self.pI)      #Leo<->Mia


        self.graph.addConnection(self.pI,self.pJ)      #Mia<->Ruth

        self.graph.addConnection(self.pJ,self.pK)      #Ruth<->Blas

    def testz_printNota(self):
        print('\n\n*************************')
        print("\t Provisional mark:",Test.mark)  
        print('*************************')
        
    def test1_getSuggestions(self):
        print('Case 1: minimumJumps=1')
        result=self.graph.getSuggestions(self.pA,1)
        expected=[self.pB,self.pC,self.pD,self.pE,self.pF,self.pG,self.pH,self.pI,self.pJ,self.pK]
        
        #print('result:')
        #for p in result:
        #    print(p)

        #print('expected:')
        #for p in expected:
        #    print(p)
    
        self.assertEqual(len(result),len(expected))
        self.assertCountEqual(result,expected)
        print('\t\t mark += 3')
        Test.mark+=3
      
    def test2_getSuggestions(self):
        print('Case 2: minimumJumps=2')
        result=self.graph.getSuggestions(self.pA,2)
        expected=[self.pE,self.pF,self.pG,self.pH,self.pI,self.pJ,self.pK]
        
        #print('result:')
        #for p in result:
        #    print(p)

        #print('expected:')
        #for p in expected:
        #    print(p)
    
        self.assertEqual(len(result),len(expected))
        self.assertCountEqual(result,expected)
        print('\t\t mark += 4')
        Test.mark+=4

    def test3_getSuggestions(self):
        print('Case 3: minimumJumps=3')
        result=self.graph.getSuggestions(self.pA,3)
        expected=[self.pI,self.pJ,self.pK]
        
        #print('result:')
        #for p in result:
        #    print(p)

        #print('expected:')
        #for p in expected:
        #    print(p)
    
        self.assertEqual(len(result),len(expected))
        self.assertCountEqual(result,expected)
        print('\t\t mark += 4')
        Test.mark+=4

    def test4_getSuggestions(self):
        print('Case 4: minimumJumps=4')
        result=self.graph.getSuggestions(self.pA,4)
        expected=[self.pJ,self.pK]
        
        #print('result:')
        #for p in result:
        #    print(p)

        #print('expected:')
        #for p in expected:
        #    print(p)
    
        self.assertEqual(len(result),len(expected))
        self.assertCountEqual(result,expected)
        print('\t\t mark += 4')
        Test.mark+=4

    def test5_getSuggestions(self):
        print('Case 5: minimumJumps=5')
        result=self.graph.getSuggestions(self.pA,5)
        expected=[self.pK]
        
        #print('result:')
        #for p in result:
        #    print(p)

        #print('expected:')
        #for p in expected:
        #    print(p)
    
        self.assertEqual(len(result),len(expected))
        self.assertCountEqual(result,expected)
        print('\t\t mark += 4')
        Test.mark+=4

    def test6_getSuggestions(self):
        print('Case 6: minimumJumps=6')
        result=self.graph.getSuggestions(self.pA,6)
        expected=[]
        
        #print('result:')
        #for p in result:
        #    print(p)

        #print('expected:')
        #for p in expected:
        #    print(p)
    
        self.assertEqual(len(result),len(expected))
        self.assertCountEqual(result,expected)
        print('\t\t mark += 1')
        Test.mark+=1
    
#Comentar para usarlo en spyder
#unittest.main(argv=['first-arg-is-ignored'], exit=False)

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    unittest.main()