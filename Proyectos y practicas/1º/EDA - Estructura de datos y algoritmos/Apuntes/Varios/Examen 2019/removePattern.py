# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from ej1 import SList

class SListWithRemovePattern(SList):
    
    def removePattern(self):
        if self.isEmpty():
            print('The list is empty')
            return 0
        
        count=0
        prev=self.head
        x=prev.element
        nodeIt=prev.next

        while nodeIt:
            if nodeIt.element==2*x:
                x=nodeIt.element
                prev.next=nodeIt.next
                self.size-=1
                count+=1
            else:
                x=nodeIt.element
                prev=nodeIt
                
            nodeIt=nodeIt.next
                
        return count

           
def test():
    """This method helps us to assess the above methods"""
    
    
    l=[1,2,4,8,16,3,6,5,4,9,18,36]
    list1=SListWithRemovePattern()
    for x in l:
        list1.addLast(x)
        
    print("original list: ", list1.toString())

    list1.removePattern()
    print("original list: ", list1.toString())
    

test()
