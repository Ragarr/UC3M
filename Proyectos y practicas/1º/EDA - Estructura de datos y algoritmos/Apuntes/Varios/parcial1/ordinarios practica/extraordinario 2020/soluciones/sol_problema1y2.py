# -*- coding: utf-8 -*-
"""sol-problema1y2.ipynb

# Problema 1: Listas Enlazadas (15 puntos)


Sea DList la implementación de lista doblemente enlazada (una versión simplificada con los métodos necesarios para inicializar una lista con elementos). 

Completa su función skipMdeleteN, recibe dos enteros M y N positivos. El método debe recorrer la lista, conservando M nodos, y entonces borrando los N nodos siguientes. El proceso debe continuar hasta que finalice el recorrido. La función debe modificar la lista. La función no devuelve nada. Pon atención a los siguientes ejemplos:


- Input: M = 1, N = 1, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->3<->5<->7<->9<->11<->13


- Input: M = 1, N = 2, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->4<->7<->10<->13  




- Input: M = 1, N = 3, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->5<->9<->13


- Input: M = 1, N = 4, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->6<->11

--------------------------------------

- Input: M = 2, N = 2, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->2<->5<->6<->9<->10<->13<->14 

- Input: M = 2, N = 3, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->2<->6<->7<->11<->12


- Input: M = 2, N = 4, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->2<->7<->8<->13<->14  
--------------------------------------

- Input: M = 3, N = 2, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->2<->3<->6<->7<->8<->11<->12<->13

- Input: M = 3, N = 3, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->2<->3<->7<->8<->9<->13<->14

- Input: M = 3, N = 4, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->2<->3<->8<->9<->10
--------------------------------------
- Input: M = 3, N = 11, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->2<->3

--------------------------------------
- Input: M = 14, N = 1, lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14
- Output: lista: 1<->2<->3<->4<->5<->6<->7<->8<->9<->10<->11<->12<->13<->14


#Problema 2 (5 puntos):
- ¿Cuál es la complejidad del método?. Razona (1 punto)
- Indica cuál es el mejor caso y su complejidad. Explica por qué (2 puntos).
- Indica cuál es el peor caso y su complejidad. Explica por qué (2 puntos).

Solución:

- Big-O=O(n). Aunque la solución tiene bucles anidados, en realidad cada nodo sólo se visita una única vez hasta el final de la lista. Por tanto, la complejidad es lineal. No existe mejor ni peor caso, porque es necesario recorrer toda la lista.       
- Best Case: Si M=0 o N=0 => O(1), no recorre la lista
- Worst Case: O(n), cada nodo sólo se visita una vez y se recorre toda la lista. Por tanto, la complejidad es lineal.'''
"""

class DNode:
  def __init__(self, elem, next=None, prev=None ):
    self.elem = elem
    self.next = next
    self.prev = prev


class DList:
    def __init__(self):
        """creates an empty list"""
        self.head=None
        self.tail=None
        self.size=0

    def __len__(self):
        """returns the number of elements of the list"""
        return self.size
    
    def add(self,e):
        """This functions adds e to the end of the list"""
        #create the new node
        newNode=DNode(e)
        
        if len(self)==0:
            self.head=newNode
        else:
            newNode.prev=self.tail
            self.tail.next=newNode
        
        #update the reference of head to point the new node
        self.tail=newNode
        #increase the size of the list  
        self.size=self.size+1


    def getAt(self,index):
        """Returns the elem at the index position in the list"""
        
        #first, check the index is a right position in the list
        if index<0 or index>=self.size:
            print(index,'error: index out of range')
            return None
        
        #we need to reach the node at the index position in the list
        i=0
        current=self.head
        while  i<index:
            current=current.next
            i+=1
        #here, current is the node at the index position in the list
        #we return its elem
        return current.elem

    def __str__(self):
        """Returns a string with the elements of the list"""
        temp=self.head
        result=''
        while temp:
            result=result+'<->'+str(temp.elem)
            temp=temp.next
        if len(result)>0:
            result=result[3:]
        return result
    
    def skipMremoveN(self,M,N):
        """Given two integers M and N. Traverse the linked list 
        such that you retain M nodes then delete next N nodes, 
        continue the same till end of the linked list."""

        """ Big-O= O(n). Aunque parezca que existan bucles anidados, cada nodo 
        sólo se visita una vez. Por tanto, la complejidad es lineal, O(n).     
        No hay mejor caso ni peor caso, porque siempre tenemos que recorrer la lista.                      
        - Best Case: M<=0 or N<=0 => O(1), no recorre la lista
        - Worst Case: O(n)"""


        if M<=0 or N<=0:
            print('M and N should be greater than 0')
            return
        
        node=self.head
        while node:
            for i in range(1,M):
                print(i,' skip:',node.elem)
                node=node.next
                if node==None:
                    return
                
            #print(M,'  skip:',node.elem)


            delNode=node.next
            count=0
            for i in range(1,N+1):
                if delNode==None:
                    break
                delNode=delNode.next
                count+=1
                

            #print('total deleted nodes:',count)
            node.next=delNode
            if delNode:
                delNode.prev=node
            else:
                self.tail=node
            
            self.size-=count


            #print()
            node=node.next

def initList():
    l=DList()
    for k in range(1,15):
        l.add(k)
    return l

for M in range(1,4):
    for N in range(1,15):
        l=initList()
        print('input list:\t\t ',l)
        print('skip {} nodes, then delete {} nodes'.format(M,N))
        l.skipMremoveN(M,N)
        print(l,' size:',len(l))
        print()


l=initList()
l.skipMdeleteN(14,1)

import unittest

class Test(unittest.TestCase):
  
    #static variable to save your mark
    mark=0
    
    def setUp(self):
        self.l=DList()
        for k in range(1,15):
            self.l.add(k)

    def testz_printMark(self):
        print('\n\n*************************')
        print("\tProvisional mark:",Test.mark)  
        print('*************************') 

 

    def test1_skipMdeleteN(self):
        print('\nCase 1: M=1, N=1')
        #1<->3<->5<->7<->9<->11<->13
        expected=[1,3,5,7,9,11,13]
        
        print('input:   ',str(self.l))
        self.l.skipMremoveN(1,1)
        print('result:  ',self.l)
        print('expected:',expected)
        #both lists should have the samel length
        self.assertEqual(len(self.l),len(expected))
        for i in range(len(self.l)):
            self.assertEqual(self.l.getAt(i),expected[i])
        print('\t\t mark += 2')
        Test.mark+=2

    def test2_skipMremoveN(self):
        print('\nCase 2: M=1, N=4')
        expected=[1,6,11]
        print('input:   ',str(self.l))
        self.l.skipMremoveN(1,4)
        print('result:  ',self.l)
        print('expected:',expected)
        #both lists should have the samel length
        self.assertEqual(len(self.l),len(expected))
        for i in range(len(self.l)):
            self.assertEqual(self.l.getAt(i),expected[i])
        print('\t\t mark += 2')
        Test.mark+=2

    def test3_skipMremoveN(self):
        print('\nCase 3: M=2, N=2')
        expected=[1,2,5,6,9,10,13,14]

        print('input:   ',str(self.l))
        self.l.skipMremoveN(2,2)
        print('result:  ',self.l)
        print('expected:',expected)
        #both lists should have the samel length
        self.assertEqual(len(self.l),len(expected))
        for i in range(len(self.l)):
            self.assertEqual(self.l.getAt(i),expected[i])
        print('\t\t mark += 2')
        Test.mark+=2

    def test4_skipMremoveN(self):
        print('\nCase 4: M=2, N=3')
        expected=[1,2,6,7,11,12]

        print('input:   ',str(self.l))
        self.l.skipMremoveN(2,3)
        print('result:  ',self.l)
        print('expected:',expected)
        #both lists should have the samel length
        self.assertEqual(len(self.l),len(expected))
        for i in range(len(self.l)):
            self.assertEqual(self.l.getAt(i),expected[i])
        print('\t\t mark += 2')
        Test.mark+=2

    def test5_skipMremoveN(self):
        print('\nCase 5: M=3, N=1')
        #1<->2<->3<->5<->6<->7<->9<->10<->11<->13<->14
        expected=[1,2,3,5,6,7,9,10,11,13,14]

        print('input:   ',str(self.l))
        self.l.skipMremoveN(3,1)
        print('result:  ',self.l)
        print('expected:',expected)
        #both lists should have the samel length
        self.assertEqual(len(self.l),len(expected))
        for i in range(len(self.l)):
            self.assertEqual(self.l.getAt(i),expected[i])
        print('\t\t mark += 2')
        Test.mark+=2

    def test6_skipMremoveN(self):
        print('\nCase 6: M=3, N=3')
        #1<->2<->3<->7<->8<->9<->13<->14
        expected=[1,2,3,7,8,9,13,14]

        print('input:   ',str(self.l))
        self.l.skipMremoveN(3,3)
        print('result:  ',self.l)
        print('expected:',expected)
        #both lists should have the samel length
        self.assertEqual(len(self.l),len(expected))
        for i in range(len(self.l)):
            self.assertEqual(self.l.getAt(i),expected[i])
        print('\t\t mark += 2')
        Test.mark+=2

    
    def test7_skipMremoveN(self):
        print('\nCase 7: M=3, N=11')
        #1<->2<->3
        expected=[1,2,3]

        print('input:   ',str(self.l))
        self.l.skipMremoveN(3,11)
        print('result:  ',self.l)
        print('expected:',expected)
        #both lists should have the samel length
        self.assertEqual(len(self.l),len(expected))
        for i in range(len(self.l)):
            self.assertEqual(self.l.getAt(i),expected[i])
        print('\t\t mark += 2')
        Test.mark+=2

    def test8_skipMremoveN(self):
        print('\nCase 8: M=14, N=1')
        expected=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

        print('input:   ',str(self.l))
        self.l.skipMremoveN(14,1)
        print('result:  ',self.l)
        print('expected:',expected)
        #both lists should have the samel length
        self.assertEqual(len(self.l),len(expected))
        for i in range(len(self.l)):
            self.assertEqual(self.l.getAt(i),expected[i])
        print('\t\t mark += 1')
        Test.mark+=1

#Comentar para usarlo en spyder
#unittest.main(argv=['first-arg-is-ignored'], exit=False)

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    unittest.main()