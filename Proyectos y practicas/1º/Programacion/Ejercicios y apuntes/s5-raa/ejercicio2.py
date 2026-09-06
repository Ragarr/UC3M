"""pedir al usuario 2 números enteros A y B tales que A + 5 < B. Se debe seguir pidiendo hasta que
el usuario introduzca los números correctos. A continuación se deben generar aleatoriamente e
imprimir 5 números enteros en el intervalo [A,B], de tal forma que se alternen pares e impares.
No es necesario que los números sean distintos, sólo la alternancia par-impar.
Ejemplo: para el intervalo [3,9] una posible secuencia válida es 6, 7, 6, 3, 4
"""
import random


def asknums():  # pregunta los numeros al usuario
    while True:
        try:
            a = int(input("introduce A: "))
            b = int(input("introduce B: "))
            asking = False
        except ValueError:
            print("por favor asegurese de que ha escrito dos numeros enteros")
        if a + 5 < b:
            return a, b


def randomizedlist(a, b):
    pre = 1
    lst = []
    for i in range(5):
        num = random.randint(a, b)
        while num % 2 == pre % 2:
            num = random.randint(a, b)
        lst.append(num)
        pre = num

    return lst


numbers = asknums()
print(randomizedlist(numbers[0], numbers[1]))
