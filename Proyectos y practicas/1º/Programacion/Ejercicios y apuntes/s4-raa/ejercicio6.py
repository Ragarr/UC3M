# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 12:54:41 2021

@author: Raúl Aguilar -@defalcovgl-
"""

"""
Hacer un programa que pida por teclado una edad e imprima el precio de una entrada de cine
según la edad. El precio normal son 9 euros, para menores de 5 años hay un 60% de descuento,
para menores de 26 un 20% y para mayores de 65 un 40%.
"""


def calcprecio(edad):  # calcula el descuento a aplicar en funcion de la edad del usuario

    precio_base = 9
    mayores65 = 0.6
    menores5 = 0.4
    menores26 = 0.8
    if edad < 5:
        precio = precio_base * menores5
        print("aplicado descuento para menores de 5")
    elif edad < 26:
        precio = precio_base * menores26
        print("aplicado descuento para menores de 26")
    elif edad > 65:
        precio = precio_base * mayores65
        print("aplicado descuento para mayores de 65")
    else:
        precio = precio_base
        print("no se puede aplicar ningin descuento")
    return precio


def askage():  # pregunta la edad al usuario
    working = True
    while working:
        try:
            edad = int(input("introduzca su edad: "))
            working = False  # finaliza la fase uno y sale del bucle
            return edad
        except ValueError:
            print("por favor asegurese de que ha escrito su edad como un numero entero")


print("su precio final es", calcprecio(askage()))
