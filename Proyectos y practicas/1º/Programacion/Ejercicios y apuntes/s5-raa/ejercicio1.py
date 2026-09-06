"""Genere un número aleatorio entre 1 y 20 y, sin mostrarlo por pantalla, trate de averiguar su
valor. A medida que introduzca valores el programa debe indicarle si el número introducido es
mayor o menor que el buscado y el número de intentos."""

import random

num = random.randint(1, 20)
finding = True
tries = 0
while finding:
    tries += 1
    guess = int(input("introduce un valor del 1 al 20: "))
    if guess < num:
        print("el numero a adivinar es mayor que el introducido")
    elif guess > num:
        print("el numero a adivinar es menor que el introducido")
    else:
        print("has adivinado el nuemero al ", tries, "º intento, congrats")
        break
