
class SNode:
  def __init__(self, e, next=None):
    self.elem = e
    self.next = next

"""Now, we can implement the class for a singly linked list. Our class only uses a refererence, head, for storing the first node, respectively. Moreover, it includes an atributte, named size, which stores the number of elements in the list."""

class SList:
  """This is the implementation of a singly linked list. We only use 
  a reference to the first node, named head"""
  def __init__(self):
    """This constructor creates an empty list"""
    self.head=None
    self.size=0
    
  def addFirst(self,e):
    """Add a new element, e, at the beginning of the list"""
    #create the new node
    newNode=SNode(e)
    #the new node must point to the current head
    newNode.next=self.head
    #update the reference of head to point the new node
    self.head=newNode
    #increase the size of the list  
    self.size=self.size+1
    
  def addLast(self,e):
    """This functions adds e to the end of the list"""
    if self.isEmpty():
      self.addFirst(e)
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
      
  def isEmpty(self):
    """"It returns True if the list is empty, and False eoc"""
    return self.head is None

  def __len__(self):
    """It returns the size of the list"""
    return self.size

  def removeFirst(self):
    """Removes the first element of the list"""
    result=None
    if self.head is None:
      print('Error: list is empty!')
    else:  
      #gets the first element, which we will return later
      result=self.head.elem
      #updates head to point to the new head (the next node)
      self.head=self.head.next
      self.size=self.size-1
    
    return result
    
  def removeLast(self):
    """Removes and returns the last element of the list"""
    result=None
    if self.head is None:
      print('Error: list is empty!')
    else:
      #we need to reach the penultimate node
      previous=None
      current=self.head
      while current.next is not None:
          previous=current
          current=current.next

      if previous is None:
        #the size of the list is 1
        result=self.removeFirst()
      else: 
        #here, current is the penultimate node, while current is the last node.
        #gest the element at the last node
        result=current.elem
        #now, previous with next must point to None
        previous.next=None
        self.size=self.size-1
    
    return result

  
  def __str__(self):
    """Returns a string with the elements of the list"""
    temp=self.head
    result=''
    while temp is not None:
      result=result+','+str(temp.elem)
      temp=temp.next
    if len(result)>0:
      result=result[1:]
    return result
    
    
  def getAt(self,index):
    """Returns the element at the index position in the list"""
    
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
    #we return its element
    return current.elem
      
      
  def index(self,e):
    """It returns the first position of e into the list. If the element 
    does no exist, then it returns -1"""
    
    index=-1
    
    found=False
    
    current=self.head
    #we traverse the nodes while found is not True. 
    while current is not None and found==False:
      if current.elem==e:
        found=True   #the loop condition becomes False
      current=current.next
      index=index+1
    
    #Warning: if e does not exist,  
    #index is the number of nodes in the list    
    if found:
      return index
    else:
      return -1
    
    
  def insertAt(self,index,e):
    """This methods inserts a new node containing the element e at the index
    position in the list"""
    
    #first, we must check that index is a right position. Note that index=size
    #is a right position for the insertAt method. 
    if index<0 or index>self.size:
      print(index, 'Error: index out of range')
      return 
   
  
    if index==0:
      self.addFirst(e)
    #elif index==self.size:
    #  self.addLast(e)
    else:
      #we need to reach the previous node (the node at the index-1 position)
      i=0
      previous=self.head
      while i<index-1:
        previous=previous.next
        i=i+1

      #now, previous is the node with index-1
      #create the new node
      newNode=SNode(e)
      #newnode must point to the node after previous (which is previous.next)
      newNode.next = previous.next
      #previous must point with its next reference to the new node
      previous.next = newNode
      self.size += 1

      
  def removeAt(self,index):
    """This methods removes the node at the index position in the list"""
    
    #We must check that index is a right position in the list
    #Remember that the indexes in a list can range from 0 to size-1
    if index<0 or index>=self.size:
      print(index,'Error: index out of range')
      return None
       
    if index==0:
      return self.removeFirst()
    elif index==self.size-1:
      return self.removeLast()
    else:
      #we must to reach the node before the node at the index position
      i=0
      previous=self.head
      while i<index-1:
        previous=previous.next
        i=i+1
      
      #previous is the node at index -1 position
      
      result=previous.next.elem
      previous.next = previous.next.next
      self.size=self.size-1
      return result
        
def check_brackets(sentence:str)->bool:
    """dovolvera True si los parentesis son correctos false si son incorrectos"""
    openers=SList()
    for char in sentence:
        if char=='(':
            openers.addFirst(char)
        elif char==')':
            if openers.isEmpty():
                return False
            else:
                openers.removeFirst()
    
    if openers.isEmpty():
        return True
    else:
        return False
            

print(check_brackets("((()())())"))
