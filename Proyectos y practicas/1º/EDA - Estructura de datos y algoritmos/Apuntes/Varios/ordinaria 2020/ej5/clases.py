class SNode:
  def __init__(self, e, next=None):
    self.elem = e
    self.next = next


class SList:
    """This is the implementation of a singly linked list. We only use 
    a reference to the first node, named head"""
    def __init__(self):
        self.head=None
        self.size=0

    def __len__(self):
        return self.size
    
    def add(self,e):
        """This functions adds e to the end of the list"""
        newNode=SNode(e)

        if self.head==None:
            #the new node must point to the current head
            newNode.next=self.head
            #update the reference of head to point the new node
            self.head=newNode
            #increase the size of the list  
        else:
            """Adds a new element, e, at the end of the list"""
            newNode=SNode(e)
            
            #we move throught the list until to reach the last node
            current=self.head
            while current.next is not None:
                current=current.next
            
            #now, current is the last node
            #the last node must point to the new node (which will be the new last node)
            current.next=newNode
        
        self.size=self.size+1

    def __str__(self):
        """Returns a string with the elements of the list"""
        temp=self.head
        result=''
        while temp:
            result=result+','+str(temp.elem)
            temp=temp.next
        if len(result)>0:
            result=result[1:]
        return result
    

