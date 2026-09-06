from dlist import DList,DNode

def mergesort(l:DList):
    m=len(l)//2
    left=DList()
    right=DList()
    current=l._head
    for _ in range(m):
        left.addLast(current.elem)
        current=current.next
    while current:
        right.addLast(current.elem)
        current=current.next
    if len(left)>1:
        left = mergesort(left)
    if len(right)>1:
        right = mergesort(right)
    
    return merge(left,right)

def merge(l1:DList,l2:DList):
    merging=True
    out=DList()
    c1=l1._head
    c2=l2._head
    while merging:
        if c1 and c2:
            if c1.elem<c2.elem:
                out.addLast(c1.elem)
                c1=c1.next
            elif c1.elem>=c2.elem:
                out.addLast(c2.elem)
                c2=c2.next
        elif c1:
            out.addLast(c1.elem)
            c1=c1.next
        elif c2:
            out.addLast(c2.elem)
            c2=c2.next
        else:
            merging=False  
    return out
        
        


l=[0,8,6,1,234,564,2314,45,232,4,6,3,21,23,56]
Dl=DList()
for i in l:
    Dl.addLast(i)
print(Dl)
print(mergesort(Dl))