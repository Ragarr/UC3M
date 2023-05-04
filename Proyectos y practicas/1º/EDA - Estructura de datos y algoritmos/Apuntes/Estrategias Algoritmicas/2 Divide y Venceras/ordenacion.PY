

##listas normales
def mergesort(l: list):
    if len(l) == 1:
        return l

    primera = l[:len(l)//2]
    segunda = l[len(l)//2:]
    primera =mergesort(primera)
    segunda =mergesort(segunda)
    return merge(primera, segunda)


def merge(l1, l2):
    i = 0
    j = 0
    aux=[]
    while i < len(l1) and j < len(l2):
        if l1[i]<l2[j]:
            aux.append(l1[i])
            i+=1
        elif l1[i]>l2[j]:
            aux.append(l2[j])
            j+=1
        else:
            aux.append(l2[j])
            aux.append(l1[i])
            i+=1
            j+=1
    while i < len(l1):
        aux.append(l1[i])
        i += 1
    while j < len(l2):
        aux.append(l2[j])
        j += 1   

    return aux

'''def DLIST_mergesort(l:DList):
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

def DLIST_merge(l1:DList,l2:DList):
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
    return out'''


# mi quicksort
def my_quicksort(l):
    if len(l) <= 1:
        return l
    else:
        pivote = l[0]
        menores = [x for x in l[1:] if x < pivote]
        mayores = [x for x in l[1:] if x >= pivote]
        return quicksort(menores) + [pivote] + quicksort(mayores)

# quicksort de isidro
def quicksort(A: list):
    if A != None and len(A) > 1:
        _quicksort(A, 0, len(A)-1)

def _quicksort(A: list, left: int, right:int):
    medio = (left + right) // 2
    pivote = A[medio]
    i = left 
    j = right
    while i<= j:
        while A[i] < pivote:
            i += 1
        while A[j] > pivote:
            j -= 1

        if i <= j:
            A[i], A[j] = A[j] , A[i]
            i += 1
            j -= 1

    if left < j:
        _quicksort(A, left, j)
    if right > i:
        _quicksort(A, i, right)



from dlist import DList,DNode

class DLIST_QUICKSORT(DList):
    def __init__(self):
        super().__init__()
    
    def quicksort(self):
        return self._quicksort(0,self._size-1)
    
    def _quicksort(self,left,right):
        medio=(left+right)//2
        pivot=self._head
        for _ in range(medio):
            pivot=pivot.next
        pivot=pivot.elem       
        a=self._head
        for _ in range(left):
            a=a.next
        
        b=self._tail
        for _ in range(self._size-right-1):
            b=b.prev
        # algoritmo perse
        i=left
        j=right
        while i<=j:
            print("i:{}, a:{} \nj:{}, b:{} \npivot:{} \n".format(i,a.elem,j,b.elem,pivot))
            if a.elem<pivot:
                a=a.next
                i+=1
            elif b.elem>pivot:
                b=b.prev
                j-=1
            elif i<=j:
                a.elem,b.elem=b.elem,a.elem
                i+=1
                j-=1
                a=a.next
                b=b.prev
        if left<j:
            self._quicksort(left,j)
        if right>i:
            self._quicksort(i,right)
        
        return
                


'''L = DLIST_QUICKSORT()
lista = [5, 4, 3, 2, 3, 0, 14]
for i in lista:
    L.addFirst(i)

print(L)


L.quicksort()

print(L)'''
l=[12,1,5,8,2,4,7,21,74]
mergesort(l)
print(mergesort(l))