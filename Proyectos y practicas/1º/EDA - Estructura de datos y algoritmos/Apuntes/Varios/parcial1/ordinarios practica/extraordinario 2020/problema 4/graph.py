# -*- coding: utf-8 -*-
"""sol-Problema4-Graph-26Jun.ipynb


#Problem 4 - Grafos

La clase Contacts es la implementación basada en grafos de una red profesional (por ejemplo, una red como Linkedin). En particular, los vértices del grafo son las personas y las aristas las posibles conexiones entre ellas. Cada persona está representada por su nombre y su número de teléfono.


Implemente una función, llamada getSuggestions, que toma una persona p y un número entero positivo minimumJumps. La función debe devolver una lista con todas las personas conectadas con P con al menos minimumJumps saltos de separación. En otras palabras, cada una de las personas de la lista está a una distancia mínima de minimumJumps conexiones con P.
"""


class Person():
    
    def __init__(self,name,phone_number):
        self.name = name
        self.phone_number = phone_number

        
    def __eq__(self,other):
        if other==None:
            return False
        
        return self.name==other.name and self.phone_number==other.phone_number
        
    def __str__(self):
        
        str_person = "Name: {}; Phone number: {}".format(self.name,self.phone_number)
        return str_person

    def __hash__(self):
        #print('The hash is:')
        return hash((self.name, self.phone_number))

class Contacts():
    
    def __init__(self):
        #vertices
        self.vertices={}
        
    
    def addPerson(self,person):
        self.vertices[person]=[]
    
    def __str__(self):
        result=''
        for p in self.vertices.keys():
            result+=str(p)+':\n'
            for friend in self.vertices[p]:
                result+='\t'+str(friend)
            result+='\n'
            
        return result
    

        
    def addConnection(self,person1,person2):
        #print('new connection:',point1,point2)
        if person1 not in self.vertices.keys():
            print(str(person1) + ' does not exist!!!')
            return
        if person2 not in self.vertices.keys():
            print(str(person2) + ' does not exist!!!')
            return
            
        self.vertices[person1].append(person2)
        self.vertices[person2].append(person1)
    
    def areConnected(self,person1,person2):
        if person1 not in self.vertices.keys():
            print(str(person1) + ' does not exist!!!')
            return
        if person2 not in self.vertices.keys():
            print(str(person2) + ' does not exist!!!')
            return
            

        return person2 in self.vertices[person1]