'''Sea SList la clase que representa una lista simplemente enlazada e implementa las operaciones del tipo abstracto de datos Lista, 
estudiada en la asignatura.

Esta clase sólo tiene como atributos la referencia al primer nodo, head, y el tamaño de la lista, size.

Se pide:

Crea una subclase SList2 de SList. Dicha subclase debe proporcionar un método, removeSmaller, que reciba un parámetro x, y que elimine de 
la lista todos aquellos nodos cuyos elementos son menores que x. El método no devuelve nada. 
El método no puede incluir llamadas a otros métodos de la clase SList o utilizar otras listas auxiliares (de ningún tipo).'''
from dato_Slist import SList
import random

class SList2(SList):
    def __init__(self):
        super().__init__()
    def removeSmaller(self,x):
        while self.head:
            if self.head.elem<x:
                self.head=self.head.next 
                self.size-=1
            else:
                break
        current=self.head
        while current and current.next and current.next.next: # evaluara desde el primero hasta el penultimo
            if isinstance(current.next.elem,(int,float)) and current.next.elem<x:
                    current.next=current.next.next
                    self.size-=1
            else:
                current=current.next
        while current and current.next: #evaluara penultimo
                if isinstance(current.next.elem,(int,float)) and current.next.elem<x:
                    current.next=None
                    self.size-=1
                else:
                    current=current.next

import unittest

class Test(unittest.TestCase):
    def setUp(self):
      
      self.x1=0
      self.input=SList2()
      self.output1=SList2()
      
      for e in [7,3,2,10,0,2,8,0,0,4,1,1,10,6,0,3,0,5,3,1]:
        self.input.addLast(e)
        self.output1.addLast(e)

      self.x2=8
      self.output2=SList2()
      for e in [10,8,10]:
        self.output2.addLast(e)
    
      self.x3=100

    def test_removeSmaller1(self):
      print()
      print('Caso 1: borramos menores que ', self.x1,' en una lista vacía')
      lEmpty=SList2()
      lEmpty.removeSmaller(self.x1)
      self.assertEqual(len(lEmpty),0)
     
    def test_removeSmaller2(self):
      print()
      print('Caso 2: no existen valores menores a ', self.x1, 'en la lista')
      print('Antes de llamar a removeSmaller: ', self.input)
      self.input.removeSmaller(self.x1)
      print('Después:',self.input)
      print('Lista esperada:',self.output1)
      self.assertEqual(len(self.input),len(self.output1))

      for i in range(len(self.input)):
        self.assertEqual(self.input.getAt(i),self.output1.getAt(i))

    def test_removeSmaller3(self):
      print()
      print('Caso 3: si existen menores que ', self.x2, ' en la lista')
      print('Antes de llamar a removeSmaller: ', self.input)
      self.input.removeSmaller(self.x2)
      print('Después:',self.input)
      print('Lista esperada:',self.output2)
      print()
      self.assertEqual(len(self.input),len(self.output2))

      for i in range(len(self.input)):
        self.assertEqual(self.input.getAt(i),self.output2.getAt(i))

    def test_removeSmaller4(self):
      print()
      print('Caso 4: todos son menores que ', self.x3, '')
      print('Antes de llamar a removeSmaller: ', self.input)
      self.input.removeSmaller(self.x3)
      print('Después:',self.input)
      print('Lista esperada:',SList2())
      print()
      self.assertEqual(len(self.input),0)

    

#Comentar para usarlo en spyder
#unittest.main(argv=['first-arg-is-ignored'], exit=False)

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    unittest.main()
