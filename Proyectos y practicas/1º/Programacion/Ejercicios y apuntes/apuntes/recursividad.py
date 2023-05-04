# """una funicon recursia es una funcion que se llama a si misma"""


"""
def funcion():
    funcion()
    #feedback-retroalimentacion 
funcion()
""" #esto peta por un error de recursividad

def factorial(n:int):
    if n<1:
        return 1
    else:
        print(n)
        return n*factorial(n-1)
print(factorial(4))