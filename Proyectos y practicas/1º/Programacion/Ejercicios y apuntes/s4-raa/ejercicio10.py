# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 14:24:58 2021

@author: Raúl Aguilar -@defalcovgl-
"""

"""
De un operario se conoce su sueldo y los años de antigüedad. Se pide confeccionar un programa
que lea los datos de entrada y muestre el sueldo a pagar:
    ●Si el sueldo es mayor o igual a 1000 mostrar el sueldo en pantalla sin cambios.
    ●Si el sueldo es inferior a 1000, el sueldo final dependerá de la antigüedad en la empresa
    (solamente preguntar por la antigüedad si el sueldo es menor que 1000):
        o Si es igual o superior a 10 años, otorgarle un aumento del 20 %.
        o Si su antigüedad es menor a 10 años, otorgarle un aumento del 5 %.
"""


def calc_sueldo(sueldo):
    if sueldo >= 1000:
        print("su sueldo sera de ", sueldo, "€")
    else:
        working = True
        while working:
            try:
                antiguedad = int(input("introduzca su adntiguedad en años: "))
                working = False
            except ValueError:
                print("por favor asegurese de que ha escrito su antiguedad como un numero entero")
        if antiguedad < 10:
            sueldo *= 1.05
        else:
            sueldo *= 1.2
        print("su sueldo sera de ", sueldo, "€")


def solicitar_sueldo():
    working = True
    while working:
        try:
            sueldo = int(input("introduzca su sueldo: "))
            working = False  # finaliza la fase uno y sale del bucle
            return sueldo
        except ValueError:
            print("por favor asegurese de que ha escrito su sueldo como un numero entero")


calc_sueldo(solicitar_sueldo())
