'''
ademas de tener next tienen prev que hace referencia al nodo anterior
'''
'''
init isempty len str addfirst inseertat(indice,e) removeat(indice)
'''
class Node:
    def __init__(self,e,next=None,prev=None) -> None:
        self.elem=e
        self.next=next
        self.prev=prev


class DList:
    def __init__(self) -> None:
        self._head=None
        self._tail=None
        self._size=0
   
    def isEmpty(self):
        return self._size==0
    def __len__(self):
        return self._size

    def addFirst(self,e):
        node=Node(e)
        if self.isEmpty():
            self._head=node
            self._tail=node
            self._size+=1
        else:
            self._head.prev=node
            node.next=self._head
            self._head=node
            self._size+=1
    
    def addLast(self,e):
        node=Node(e)
        if self.isEmpty():
            self._head=node
            self._tail=node
            self._size+=1
        else:
            self._tail.next=node
            node.prev=self._tail
            self._tail=node
            self._size+=1
    
    def insertAt(self,index,elem):
        #verificar error indice

        if index>=self._size or index<0:
            print("error de indice")
            return
        elif self.isEmpty():
            self.addFirst(elem)
        elif index==self._size-1:
            self.addLast(elem)
        elif index==0:
            self.addFirst(elem)
        else:
            node=Node(elem)
            current=self._head
            current_index=1
            #en vez del contador podriamos  usar un for
            while current and current_index!=index:
                current=current.next
                current_index+=1
            
            current.next.prev=node
            node.next=current.next
            current.next=node
            node.prev=current
            self._size+=1
    
    def removeFirst(self):
        if self.isEmpty():
            print("lista vacia")
            return
        
        if self._head.next:
            self._head=self._head.next
            self._head.prev=None
        
    def __str__(self) -> str:
        text='['
        current=self._head
        while current:
            text+=str(current.elem)
            text+=','
            current=current.next
        return text[:-1]+']'
    
    
a=DList()
a.insertAt(0,"a")