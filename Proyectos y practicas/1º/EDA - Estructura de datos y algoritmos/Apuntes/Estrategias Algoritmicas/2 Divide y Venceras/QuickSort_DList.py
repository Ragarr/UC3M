from dlist import DList
from dlist import DNode
from random import randint

def quicksort(A: list):
    if A != None and len(A) > 1:
        _quicksort(A, 0, len(A)-1)

def _quicksort(A: list, left: int, right:int):
    m = (left + right) // 2
    p = A[m]
    i = left
    j = right
    while i<= j:
        while A[i] < p:
            i += 1
        while A[j] > p:
            j -= 1

        if i <= j:
            A[i], A[j] = A[j] , A[i]
            i += 1
            j -= 1

    if left < j:
        _quicksort(A, left, j)
    if right > i:
        _quicksort(A, i, right)

class DLIST_QUICKSORT(DList):
    def quicksortDL(self):
        if self._size > 1:
            self._quicksortDL(0, self._size - 1)
        return

    def _quicksortDL(self, start: int, end: int):
        m = (start + end) // 2
        current = self._head
        for i in range(m):
            current = current.next

        pivot = current.elem
        'primero buscamos los nodos en las posiciones start y end.'
        # current = self._head
        # for n in range(start + end):
        #     current = current.next
        #     if n == start - 1:
        #         forward = current
        #     if n == (start + end - 1)
        #         backward = current
        currentf = self._head
        for n in range(start):
            currentf = currentf.next

        currentb = self._tail
        for n in range( self._size -1 - end ):
            currentb = currentb.prev

        'ahora sí podemos hacer el algoritmo de quicksort'
        i = start
        j = end
        print('start:', currentf.elem, '\nend:', currentb.elem, '\npivot:', pivot)
        while i<= j:
            print('Entro bucle1:')
            print('i:', i)
            print('i_elem:', currentf.elem)
            while currentf.elem < pivot:
                # hay que mover nodo e indice x separado para mantener las 2 referencias y poder comparar nodos con nodos e indices con indices
                currentf = currentf.next
                i += 1
                print('i:', i)
                print('i_elem:', currentf.elem)

            print('j:', j)
            print('j_elem:', currentb.elem)
            while currentb.elem > pivot:
                currentb = currentb.prev
                j -= 1
                print('j:', j)
                print('j_elem:', currentb.elem)

            if i <= j:
                print('Intercambiamos:', currentf.elem, 'y', currentb.elem)
                if i < j:
                    # si i == j no hace falta intercambiar los elementos
                    currentf.elem, currentb.elem = currentb.elem, currentf.elem

                # siempre que movemos el índice, debemos también mover el puntero del nodo dentro de la lista!!
                i += 1
                currentf = currentf.next
                j -= 1
                currentb= currentb.prev

            print(self)
        if start < j:
            self._quicksortDL(start, j)
        if end > i:
            self._quicksortDL(i, end)

        return

L = DLIST_QUICKSORT()
lista = [5, 4, 3, 2, 3, 0, 14]
for i in lista:
    L.addFirst(i)

print(L)

L.quicksortDL()

print(L)




