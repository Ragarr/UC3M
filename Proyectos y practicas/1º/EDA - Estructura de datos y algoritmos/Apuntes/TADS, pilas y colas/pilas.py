"""las pilas son una estructura lineal (organizados seuencialmente -listas-)
    las listas enlazadas aun que son mas aparatosas son mejores para grandes datos
    
las pilas y coals utilizan listas
una pila es una secuencia de elementos al que solo se puede entrar y salir por el principio o el final 
solo puedes modificar el primer o ultimo elemento (sacandolo o metiendo otro)"""
"""el punto de acceso a una  pila se llama cima (last in, first out)"""
"""meter un elemento es push y sacar un elemento es pop y saber cual esta en la cima es top"""
'''funciones utiles:
top()-> ultimo elemento de la pila sin borrarlo, isEmpty()-> saber si esta vacia, len() la longitud de la pila'''

from inspect import stack


class Stack:
    def __init__(self) -> None: # las pilas se crean vacias y se rellenan con push
        self.items=[]
    
    def __str__(self) -> str:
        return str(self.items)
    def __len__(self):
        return len(self.items)
    def isEmpty(self)->bool:
        return len(self)==0
    def push(self,new):
        self.items.append(new)
    def pop(self):
        if not self.isEmpty():
            return self.items.pop()
        else:
            raise IndexError("La pila esta vacia")

    def top(self):
        return self.items[-1]



s=Stack()
for i in range(6):
    s.push(i)
print(s)
s.pop()
print(s)
print(s.top())


def reverse(word):
    s=Stack()
    reversed=""
    for letter in word:
        s.push(letter)
    for i in range(len(s)):
        reversed+=str(s.pop())
    return reversed
print(reverse("hola mundo"))
