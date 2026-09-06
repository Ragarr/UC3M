from clases import SList, SNode

class SList2(SList):
    def __init__(self):
        super().__init__()
    
    def moveLastToFront(self,k:int):
        if k>len(self):
            return
        current=self.head
        for _ in range(len(self)-1-k):
            current=current.next
        current.next,self.head=None,current
        

        