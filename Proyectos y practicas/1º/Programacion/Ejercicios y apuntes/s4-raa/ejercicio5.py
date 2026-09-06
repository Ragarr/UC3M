# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 12:43:30 2021

@author: Raúl Aguilar -@defalcovgl-
"""

"""
Hacer un programa que le pida al usuario por el teclado dos nombres y dos edades e imprima
que fulanito es mayor que menganito. Ej. Si introducimos Pepe 23 y Luisa 18, debe imprimir
Pepe es mayor que Luisa. Si tienen la misma edad, debe imprimir Pepe y Luisa
tienen la misma edad.
"""


def main():
    fase1 = True  # es el activador de la primera fase que creara las variables de nombre y edad
    while fase1:
        try:
            nombre1 = input("introduce el nombre de la primera persona: ")
            edad1 = int(input("introduce su edad: "))
            nombre2 = input("introduce el nombre de la segunda persona: ")
            edad2 = int(input("introduce su edad: "))

            fase1 = False  # finaliza la fase uno y sale del bucle


        except ValueError:
            print("por favor asegurese de haber introducido las edades correctas")

    if edad1 > edad2:
        print(nombre1, "es mayor que", nombre2)
    elif edad2 > edad1:
        print(nombre2, "es mayor que", nombre1)
    else:
        print(nombre1, "y", nombre2, "tienen la misma edad")


main()

# he reciclado bastante codigo del ej anterior
