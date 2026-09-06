"""Crear tres funciones para: (a) pedir al usuario un número positivo en el rango (1, 10), (b)
generar una lista aleatoria de ese número de elementos, y (c) encontrar el mínimo de esa lista.
Crear un programa que use las funciones anteriores."""

from math import inf


def pedirNumero():
    preguntando=True
    while preguntando:
        num=input("introduzca un numero positivo entre 1 y 10")
        if num.isnumeric():
            num=int(num)
            if num <=10 and num>=1:
                return num

def crearListaAleatoria(longitud:int)->list:
    import random
    lista=list()
    for i in range(longitud):
        lista.append(random.random())
    return lista

def encontrarMinimo(lista:list):
    buscando =True
    min=0
    for n in lista:
        min+=n
    for item in lista:
        if item<min:
            min=item
    return min
        
num=pedirNumero()
lista=crearListaAleatoria(num)
minimo=encontrarMinimo(lista)