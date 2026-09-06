# divide y venceras
def getIndex(A: list, x: int) -> int:
    """
    Returns the index of the element x in the list A. using recurion and divide and conquer
    """
    if len(A) == 1:
        if A[0] == x:
            return 0
        else:
            return -1
    else:
        mid = len(A) // 2
        left = A[:mid]
        right = A[mid:]
        if x in left:
            return getIndex(left, x)
        elif x in right:
            return getIndex(right, x) + mid
        else:
            return -1

l=[]
for i in range(10):
    l.append(i)

print(l)
print(l.index(4),getIndex(l,4))
