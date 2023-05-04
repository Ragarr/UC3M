'''
Problemas - Listas simplemente enlazadas.
En la clase SList (con _head y _tail), implementa las siguientes funciones:
- remove(e): método que recibe un elemento, e, y borra la primera ocurrencia de e en
la lista (es decir, elimina el primer nodo que contiene a e). La función modifica la lista
y no devuelve nada. Si el elemento no existe en la lista, la función debe informar que
no existe.
- removeAll(e): función que recibe un elemento, e, y borra todas las ocurrencias de e
en la lista (es decir, elimina todos los nodos que contienen a e). La función modifica
la lista y no devuelve nada. Si el elemento no existe en la lista, la función debe
informar que no existe.
- getAtRev(index): función que recibe un índice, index, y devuelve el elemento en la
posición index empezando por el final. Por ejemplo:
l: 0->1->2->3->4, l.getAtRev(0)=4, l.getAtRev(1)=3, l.getAtRev(2)=2, l.getAtRev(3)=1,
l.getAtRev(4)=0,
● getMiddle(): función que devuelve el elemento que está en la mitad de la lista. Si la
lista tiene un número par de elementos, la función devolverá el elemento en la
posición len(l)//2 +1. Ejemplo: 1->2->3->4->5->6, l.getMiddle()=4
● count(e): función que recibe un elemento, e, y devuelve el número de veces que
ocurre en la lista. Si el elemento no existe en la lista, la función devuelve 0.
● isPalindrome(): función que comprueba si los elementos contenidos en la lista
forman una palabra palíndroma (por ejemplo, radar, aba, abba, abcba). Si es
palíndroma devuelve True, y en otro caso, False.
● isSorted(): función que comprueba si la lista está ordenada de forma ascendente (en
este caso devuelve True). En caso contrario, debe devolver False.
● removeDuplicatesSorted(): función que borra los elementos duplicados en una lista
ordenada. La función modifica la lista, no devuelve nada.
Ejemplo: l: 1->1->2->3->3->4->5->5, l: 1->2->3->4->5.
● removeDuplicates(): función que borra los elementos duplicados en una lista (no
tiene que estar ordenada). La función modifica la lista, no devuelve nada.
Ejemplo: l: 1->2->1->0->2->6->6->4->5->5, l: 1->2->0->6->4->5.
● swapPairwise(): función que intercambia los elementos que ocupan posiciones
contiguas. La función modifica la lista, no devuelve nada. Ejemplos:
l: 1->2->3->4->5, l:2->1->4->3->5
l: 1->2->3->4->5->6, l:2->1->4->3->6->5
● moveLast(): función que mueve el último elemento al principio de la lista, sin usar
ninguna de las funciones de la clase SList. La función modifica la lista, no devuelve
nada. Ejemplo: l:1->2->3->4->5->6, l: 6->1->2->3->4->5
● intersection(l2): función que recibe una lista l2 y devuelve una nueva lista que
contenga la intersección de ambas listas, la invocante y l2. Como precondición, se
exige que ambas listas están ordenadas de forma ascendente. Ejemplo:
l:1->2->3->4->5->6, l2: 0->1->2->3, output: 1->2->3.
● segregateOddEven(): función que modifica la lista invocante para que todos los
elementos pares aparezcan antes que los elementos impares. La función debe
respetar el orden de los elementos pares y el orden de los elementos impares.
Ejemplo: l: 17->15->8->12->10->5->4->1->7->6
l: 8->12->10->4->6->17->15->5->1->7
'''


from lib2to3.pytree import Node
from locale import currency
from multiprocessing.dummy import current_process
from operator import le
from os import curdir, remove


class SNode:
    def __init__(self, e) -> None:
        self.elem = e
        self.next = None


class SList:
    def __init__(self) -> None:
        self._head = None
        self._tail = None
        self._size = 0
    # metodos QOL

    def isEmpty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def __str__(self) -> str:
        text = '['
        current = self._head
        while current:
            text += str(current.elem)
            text += ","
            current = current.next
        text = text[:-1]+"]"
        return text
    # metodos propios

    def addFirst(self, e):
        node = SNode(e)
        if self.isEmpty():
            self._head = node
            self._tail = node
            self._size += 1
        else:
            node.next = self._head
            self._head = node
            self._size += 1

    def addLast(self, e):
        node = SNode(e)
        if self.isEmpty():
            self._head = node
            self._tail = node
            self._size += 1
        else:
            self._tail.next = node
            self._tail = node
            self._size += 1

    def removeFirst(self):
        if self.isEmpty():
            raise IndexError
        aux = self._head.elem
        self._head = self._head.next
        self._size -= 1
        return aux

    def insertAt(self, e, index):
        if self._size < index or index < 0:
            raise IndexError
        if index == 0:
            self.addFirst(e)
        elif index == len(self)-1:
            self.addLast(e)
        else:
            current = self._head
            node = SNode(e)
            for i in range(index-1):
                current = current.next
            node.next = current.next
            current.next = node
        self._size += 1

    def remove(self, e):
        if self.isEmpty():
            print('el elemento no existe en la lista')
            return
        if self._head.elem == e:
            self.removeFirst()
            return
        current = self._head
        while current.next and current.next.next:
            if current.next.elem == e:
                current.next = current.next.next
                self._size-=1
                return
            else:
                current = current.next
        if current.next.elem == e: #elimina el ultimo elemento en la lista
            self._tail=current
            current.next = None
            self._size-=1
            return
        print('el elemento no existe en la lista')

    def removeAll(self, e):
        if self.isEmpty():
            print('el elemento no existe en la lista')
            return
        while self._head.elem == e:
            self.removeFirst()
        current = self._head
        while current.next and current.next.next:
            if current.next.elem == e:
                current.next = current.next.next
                self._size -= 1
            else:
                current = current.next
        if current.next.elem == e:
            self._tail=current
            current.next = None
            self._size -= 1
            return
        print('el elemento no existe en la lista')

    def getAtRev(self, index):
        '''función que recibe un índice, index, y devuelve el elemento en la
        posición index empezando por el final. Por ejemplo:
        l: 0->1->2->3->4, l.getAtRev(0)=4, l.getAtRev(1)=3, l.getAtRev(2)=2, l.getAtRev(3)=1,
        l.getAtRev(4)=0'''
        current = self._head
        if index >= self._size or index < 0:
            print("error indice")
            return
        if index == self._size-1:
            return self._head.elem
        if index == 0:
            return self._tail.elem

        for i in range(self._size-index-1):
            current = current.next
        return current.elem

    def getMiddle(): 
        '''función que devuelve el elemento que está en la mitad de la lista. Si la
        lista tiene un número par de elementos, la función devolverá el elemento en la
        posición len(l)//2 +1. Ejemplo: 1->2->3->4->5->6, l.getMiddle()=4'''
        

a = SList()
for i in range(10):
    a.addFirst(i)


print(a,a._size)
a.remove(9)
print(a,a._size)
a.remove(0)
print(a,a._size)
a.remove(0)
print(a,a._size)

a.removeAll(6)
print(a,a._size)
print(a.getAtRev(6







))
print(a,a._size)
