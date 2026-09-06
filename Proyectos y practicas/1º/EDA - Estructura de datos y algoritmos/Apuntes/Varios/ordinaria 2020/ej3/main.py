def getIndices(A:list,x:int):
    l=[]
    getIndex(A,x,0,l)
    return l

def getIndex(A:list,x:int,cut_index,l:list):
    if len(A) == 1 and A[0]==x:
        l.append(cut_index)
    elif len(A)<=1:
        return
    else:
        getIndex(A[:len(A)//2],x,cut_index,l)
        getIndex(A[len(A)//2:],x,cut_index+(len(A)//2),l)