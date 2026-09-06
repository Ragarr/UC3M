from dlist import DNode
from dlist import DList

class DList2(DList):
    def __init__(self):
        super().__init__()
    
    def removeDuplicatesSorted(self): 
        '''función que borra los elementos duplicados en una lista
        ordenada. La función modifica la lista, no devuelve nada.'''
        current=self._head
        while current:
            if current.elem==current.next.elem:
                current.next=current.next.next
            else:
                current=current.next
    def sort(self):
        pass
    def removeDuplicates(self): 
        '''función que borra los elementos duplicados en una lista (no
        tiene que estar ordenada). La función modifica la lista, no devuelve nada.'''
        # complejidad n^2
        current=self._head
        while current:
            check=self._head
            while check:
                if current.elem==check.elem and current is not check:
                    if check.prev and check.next: # check esta en medio
                        check.prev.next=check.next
                        check.next.prev=check.prev
                    elif check.prev: # check es el ultimo
                        check.prev.next=check.next
                    elif check.next: # check es el primero
                        check.next.prev=check.prev
                check=check.next
                self._size-=1
            current=current.next


l=DList2()
for i in range(10):
    l.addFirst(i)
for i in range(10):
    l.addLast(i)
    # l.addFirst(i*i)

print(l)
l.removeDuplicates()
print(l)

