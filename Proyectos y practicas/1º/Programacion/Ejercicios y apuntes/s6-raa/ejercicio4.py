"""Escribe un programa que cree una lista de 20 números enteros, completándola aleatoriamente
con números entre 1 y 9. Pide al usuario un número (el programa debe comprobar que el
número está entre 1 y 9). Muestra por pantalla si el número está en la lista y todas las
posiciones en las que aparece."""
import random


def asknum():
    try:
        num = int(input("introduce un numero del 1 al 9"))
        askin = False
    except:
        print("asegurate de haber introducido un numero")
        asknum()
    if num > 9 or num < 1:
        print("asegurate de haber introducido un numero entre 1 y 9")
        asknum()
    return num


num = asknum()
lista = []
for i in range(20):
    lista.append(random.randint(1, 9))
if num in lista:
    print("el numero", num, " aparece en la lista")
for indice, valor in enumerate(lista):
    if num == valor:
        print("el numero", num, "aparece en la posicion", indice + 1)
