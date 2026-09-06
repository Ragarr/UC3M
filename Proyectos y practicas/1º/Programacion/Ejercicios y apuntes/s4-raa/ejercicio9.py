# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 14:17:43 2021

@author: Raúl Aguilar -@defalcovgl-
"""

"""Escribir un programa que pida ingresar la coordenada de un punto en el plano, es decir dos
valores enteros x e y. Posteriormente imprimir en pantalla en que cuadrante se ubica dicho
punto. (1º Cuadrante si x > 0 Y y > 0 , 2º Cuadrante: si x < 0 Y y > 0, etc.). Si alguno de ellos es
cero imprimirá Cero no es un valor válido y terminará."""


def buscar_cuadrante(x, y):
    if x > 0 and y > 0:
        print("1º cuadrante")
    elif x < 0 and y > 0:
        print("2º cuadrante")
    elif x < 0 and y < 0:
        print("3º cuadrante")
    elif x > 0 and y < 0:
        print("4º cuadrante")
    else:
        print("Cero no es un valor válido")
        return


asking = True
while asking:
    x = input("introduzca la cordenada X: ")
    y = input("introduzca la cordenada Y: ")
    if x.startswith("-") and x[1:].isdigit() or x.isdigit():
        x = float(x)
    else:
        print("valor x no valido")
    if y.startswith("-") and y[1:].isdigit() or y.isdigit():
        y = float(y)
    else:
        print("valor y no valido")
    if isinstance(x, float) and isinstance(y, float):
        asking = False

buscar_cuadrante(x, y)
