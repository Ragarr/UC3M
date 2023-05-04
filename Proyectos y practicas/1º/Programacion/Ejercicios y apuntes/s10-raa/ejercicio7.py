"""La secuencia de Fibonacci f(n) viene determinada por la siguiente fórmula:
si n = 0 f(n) = 0
si n = 1 f(n) = 1
si n > 1 f(n) = f(n - 1) + f(n - 2)
Definir una función que imprima la secuencia de Fibonacci a partir de un número dado.
"""
def fibonacci(n:int):
    if n==0:
        return [0]
    elif n ==1:
        return [1]
    else:
        lst = [0,1]
        for i in range(2,n+1):
            lst.append(lst[i-1]+lst[i-2])
        return lst

#hacerlo tambien de forma recursiva


print(fibonacci(420))
input()