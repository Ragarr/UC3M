'''from turtle import right


def mayorelem(l: list):
    if len(l) == 1:
        return l[0]
    else:
        primera = mayorelem(l[:len(l)//2])
        segunda = mayorelem(l[len(l)//2:])
        if primera > segunda:
            return primera
        else:
            return segunda


l = [1, 2, 4, 6, 3, 9, 1, 65, 235, 45, 467, 23, 12, 0, 12, 1000]
print(mayorelem(l))'''

l=[1,2,435,2,465,78,782,34,38,73,59,234,68623,487652,873,49]

def mergesort(l:list):
    if len(l) <= 1:
        return l
    else:
        mitad = len(l)//2
        izq = mergesort(l[:mitad])
        der = mergesort(l[mitad:])
        return merge(izq, der)
def merge(izq,der):
    if not izq:
        return der
    if not der:
        return izq
    if izq[0] < der[0]:
        return [izq[0]] + merge(izq[1:],der)
    else:
        return [der[0]] + merge(izq,der[1:])

def quicksort(l):
    if len(l) <= 1:
        return l
    else:
        pivote = l[0]
        menores = [x for x in l[1:] if x < pivote]
        mayores = [x for x in l[1:] if x >= pivote]
        return quicksort(menores) + [pivote] + quicksort(mayores)


def quicksort2(l):
    return _quicksort2(l)

def _quicksort2(l):
    if len(l)<=1:
        return l
    else:
        indice_pivote = len(l)//2
        pivote = l[indice_pivote]
        i=0
        j=len(l)-1
        left=[]
        right=[]
        print(l,pivote)
        while i <= j:
            while l[i]<pivote:
                i+=1
            while l[j]>pivote:
                print('Entra')
                j-=1
            if i <= j:
                print(i, j,end=' ')
                l[i],l[j]=l[j],l[i]
                i+=1
                j-=1
        print('final', l)
        left = _quicksort2(l[:indice_pivote])

        right = _quicksort2(l[indice_pivote+1:]) 
        print('return recursivo:', left + [pivote] + right)
        
        return left + [pivote] + right
print(quicksort2(l))
print(mergesort(l))