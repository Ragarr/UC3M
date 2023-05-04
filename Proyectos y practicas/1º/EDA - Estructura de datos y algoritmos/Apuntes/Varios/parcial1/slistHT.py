# -*- coding: utf-8 -*-
"""
Created on Sun May  1 12:59:47 2022

@author: SECRETARIA
"""

# -*- coding: utf-8 -*-
class SNode:
    def __init__(self, e, next_node: 'SNode' = None):
        self.elem = e
        self.next = next_node

class SList:
    """This is the implementation of a singly linked list. We use 
    a reference to the first node, named _head, and also a reference 
    to the last node, named as _tail. Also, we keep an attribute, _size,
    to store the number of nodes"""
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0
    
    def __len__(self):
        return self._size
    
    def is_empty(self) -> bool:
        """Checks if the list is empty"""
        # return self._head == None
        return len(self) == 0

    def __str__(self) -> str:
        """Returns a string with the elements of the list"""

        node = self._head
        result = '['
        while node:
            if type(node.elem) == int:
                result += str(node.elem) + ", "
            else:
                result += "'" + str(node.elem) + "', "
            node = node.next
        
        if len(result) > 1:
            result = result[:-2]
        result += ']'
        return result

    def add_first(self, e: object):
        """ Add a new element, e, at the beginning of the list"""
        # create the new node
        new_node = SNode(e)
        # the new node must point to the current head
        if self.is_empty():
            self._tail = new_node
        else:
            new_node.next = self._head

        # update the reference of head to point the new node
        self._head = new_node
        # increase the size of the list
        self._size += 1

    def add_last(self, e: object):
        """Adds a new element, e, at the end of the list"""
        # create the new node
        new_node = SNode(e)
        # the last node must point to the new node
        # now, we must update the tail reference
        if self.is_empty():
            self._head = new_node
        else:
            self._tail.next = new_node
        
        self._tail = new_node
        # increase the size of the list
        self._size += 1

    def remove_first(self) -> object:
        """Removes the first element of the list"""
        result = None
        if self.is_empty():
            print('Error: list is empty!')
        else:
            # gets the first element, which we will return later
            result = self._head.elem
            # updates head to point to the new head (the next node)
            self._head = self._head.next
            # if the list only has one node, tail must be None
            if self._head is None:
                self._tail = None
            self._size -= 1
        
        return result

    def remove_last(self):
        """Removes and returns the last element of the list"""
        result = None
        if self.is_empty():
            print('Error: list is empty!')
        elif len(self) == 1:
            result = self.remove_first()
        else:
            result = self._tail.elem
            penult = self._head
            while penult.next != self._tail:
                penult = penult.next
            
            penult.next = None
            self._tail = penult
            self._size -= 1
        
        return result

    def getAt(self, index: int) -> object:
        """return the element at the position index.
        If the index is an invalid position, the function
        will return None"""
        result = None
        if index not in range(0, len(self)):
            print(index, 'Error getAt: index out of range')
        else:
            node = self._head
            count = 0
            while node and count < index:
                node = node.next
                count += 1
            # node is at the position index
            result = node.elem

        return result

    def index(self, e: object) -> int:
        """returns the first position of e into the list.
        If e does not exist in the list, 
        then the function will return -1"""
        node = self._head
        index = 0
        while node:
            if node.elem == e:
                return index
            node = node.next
            index += 1
            
        # print(e,' does not exist!!!')
        return -1 

    def insertAt(self, index: int, e: object) -> None:
        """This method inserts a new node containing the element e at the index
        position in the list"""
        if index not in range(0, len(self)+1):
            print(index, 'Error insertAt: index out of range')
        elif index == 0:
            self.add_first(e)
        elif index == len(self):
            self.add_last(e)
        else:
            node = self._head
            for _ in range(index-1):
                node = node.next
            # node is at index-1
            new_node = SNode(e)
            new_node.next = node.next
            # previous must point with its next reference to the new node
            node.next = new_node
            self._size += 1
      
    def removeAt(self, index: int) -> object:
        """This method removes the node at the index position in the list"""
        result = None
        if index not in range(len(self)): 
            print(index, 'Error removeAt: index out of range')
        elif index == 0:
            result = self.remove_first()
        elif index == len(self)-1:
            result = self.remove_last()
        else:
            # we must reach the node before the node at the index position
            node = self._head
            for _ in range(index-1):
                node = node.next
                
            # node is the node at index -1 position
            # node.next is the node at index position
            aux = node.next  # node to remove
            result = aux.elem
            node.next = aux.next
            self._size -= 1
        
        return result


if __name__ == '__main__':
    import random
    l1 = SList()
    for _ in range(5):
        l1.add_last(random.randint(-5, 5))

    print('Content of l1:', l1)
    print('len(l1):', len(l1))
    print()

    while not l1.is_empty():
        print('after remove_first()={}, l1={}, len={}'.format(l1.remove_first(), l1, len(l1)))

    for _ in range(3):
        x = random.randint(-5, 5)
        l1.add_first(x)
        print('after addFirst({}), l1={}, len={}'.format(x, l1, len(l1)))

    print('Content of l1:', l1)
    print('len(l1):', len(l1))
    print()

    while not l1.is_empty():
        print('after removeLast()={}, l1={}, len={}'.format(l1.remove_last(), l1, len(l1)))
    print('---------------------')
    for _ in range(3):
        x = random.randint(-5, 5)
        l1.add_first(x)
        l1.add_last(x)

    print('Content of l1:', l1)
    print('len(l1):', len(l1))
    print()

    for i in range(len(l1)):
        print(' getAt({})={}'.format(i, l1.getAt(i)))
    print()

    for _ in range(3):
        x = random.randint(-5, 5)
        print(' index({})={}'.format(x, l1.index(x)))
    print()

    print('Content of l1:', l1)
    print('len(l1):', len(l1))
    print()

    x = 666
    l1.insertAt(0, x)
    print(' insertAt(0,{}), l1={}, len={}'.format(x, l1, len(l1)))
    l1.insertAt(len(l1), x)
    print(' insertAt(len(l1),{}), l1={}, len={}'.format(x, l1, len(l1)))
    l1.insertAt(len(l1)//2, x)
    print(' insertAt(len(l1)//2,{}), l1={}, len={}'.format(x, l1, len(l1)))
    print()
    print()

    print(' removeAt(0)={}, l1={}, len={}'.format(l1.removeAt(0), l1, len(l1)))
    print(' removeAt(len(l1)-1)={}, l1={}, len={}'.format(l1.removeAt(len(l1)-1), l1, len(l1)))
    print(' removeAt(len(l1)//2+1)={}, l1={}, len={}'.format(l1.removeAt(len(l1)//2+1), l1, len(l1)))