# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 11:21:49 2021

@author: Raúl Aguilar -@defalcovgl-
"""

"""
Hacer un programa que pida al usuario dos números enteros y muestre el
resultado de dividir el primero por el segundo. Si el segundo es cero, en lugar
de dividir deberá imprimir “No se puede dividir por cero usando enteros”
"""


def main():
    fase1 = True  # es el activador de la primera fase que creara las variables
    while fase1:
        try:
            i1 = int(input("introduce el numerador: "))
            i2 = int(input("introduce el denominador: "))
            fase1 = False  # finaliza la fase uno y sale del bucle
        except ValueError:
            print("por favor asegurese de que sus valores son enteros")
    fase2 = True
    while fase2:
        try:
            print(i1, "/", i2, "es: ", i1 / i2)
            fase2 = False
        except ZeroDivisionError:
            print("No se puede dividir por cero usando enteros")
            print("Vuelva a introducir sus enteros")
            main()


"""
He decidido que la funcion no sea recursiva de forma infinita por que no creear
un bucle mas y no tener que preguntar al usuario cuando quiere salir, por lo
tanto solo se ejecuta una vez, pero se podria hacer completamente recursiva.
"""

main()
