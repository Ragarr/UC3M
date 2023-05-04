from re import search


def suma(n):
    if n ==0:
        return 0
    
    return n+suma(n-1)
#print(suma(12))

def factorial(n):
    if n==1:
        return 1
    return n*factorial(n-1)
#print(factorial(4))
def mult(a,b):
    if b==0:
        return 0
    return a+mult(a,b-1)


#print(mult(4,4))
def fibonacci(n):
    if n <=1:
        return n
    return fibonacci(n-1)+fibonacci(n-2)

#print(fibonacci(5))

def palin(w):
    if len(w)==1 or len(w)==2:
        return True
    if w[0]!=w[-1]:
        return False
    return palin(w[1:-1])
#print(palin("anaana"))
w="murcielago"
c1="r"
c2="d"
def areAdj(w,c1,c2):
    if w[0]==c1:
        if w[1]==c2:
            return True
        else:
            return False
    return areAdj(w[1:],c1,c2)

#print(areAdj(w,c1,c2))
def invert(l:list):
    if len(l)==0:
        return l
    return [l[-1]]+invert(l[:-1])
#print(invert([1,2,3,4,5,6,7,8,9]))


def order(l:list):
    if len(l)<=1:
        return l
    min=l[0]
    for i in l:
        if i< min:
            min=i
    l.remove(min)
    return [min] + order(l)

def searchB(l,x):
    if len(l)<=1:
        return l[0]==x
    return searchB(l[:len(l)//2],x) or searchB(l[len(l)//2:],x)
print(searchB([1,2,3,4,5,6],12))
print(order([1,3,5,7,3,2,5,7,3,6,8,0,5]))