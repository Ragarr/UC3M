'''
las listas(arrays) ocupan lugares contiguos de memoria, solo puede hacerlo asi.
si se queda sin espacio debe borrar todos y reposicionarlos, sin embargo son 
muy rapidas
'''
'''
una lista enlazada permite almacenar donde se decida, para crear una lista
enlacada necesitas la clase lista y la clase nodo (SNose es la clase nodo de
la lista simplemente enlazada) que contiene cualquier objeto (tiene la info 
como tal), tiene dos atributos: 
    -elem(el contenido como tal -otro objeto-)
    -next(apunta al siguiente elemento)
la clase SList(lista simple) con dos atributos:
    -head(primer nodo)
    -size(numero de elementos que la forman)
'''




from multiprocessing.dummy import current_process
from select import select
from socket import AddressFamily
class SNode:
    def __init__(self, elem) -> None:
        self.elem = elem
        self.next = None

    def __str__(self) -> str:
        return str(self.elem)

class SList:
    def __init__(self) -> None:
        self._head = None
        self._size = 0

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

    def addFirst(self, elemento):
        node = SNode(elemento)
        node.next = self._head
        self._head = node
        self._size += 1

    def removeFirst(self):
        if self.isEmpty():
            raise IndexError
        aux = self._head.elem
        self._head = self._head.next
        self._size -= 1
        return aux

    def addLast(self, e):
        if self.isEmpty:
            self.addFirst(e)
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = SNode(e)
            self._size += 1

    def insertAt(self, e, index):
        if self._size < index:
            raise IndexError
        current = self._head
        node = SNode(e)
        for i in range(index-1):
            current=current.next
        node.next=current.next
        current.next=node
        self._size+=1
    
    def removeOdd(self):
        #elimina los elementos numeros impares
        if self.isEmpty():
            raise IndexError
        current=self._head
        while self._head and self._head.elem%2!=0: #
            self._head=self._head.next
            
        
        while current and current.next:
            if current.next.elem %2 !=0:
                current.next=current.next.next
                self._size-=1
            else:
                current=current.next


        



lista = SList()
for i in range(21,0,-2):
    lista.addLast(i)
lista.removeOdd()
print(lista,lista._size)