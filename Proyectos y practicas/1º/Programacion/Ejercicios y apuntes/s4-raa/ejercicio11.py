# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 18:09:08 2021

@author: Raúl Aguilar -@defalcovgl-
"""

"""Un año es bisiesto si es múltiplo de 4, exceptuando los múltiplos de 100, que sólo son bisiestos
cuando son múltiplos además de 400, por ejemplo el año 1900 no fue bisiesto, pero el año 2000
sí lo fue. Hacer un programa que pida al usuario un año, y diga si es o no bisiesto (se recomienda
usar el diagrama de flujo de la semana 2)."""

año_actual = 2021


def solicitar_año():
    working = True
    while working:
        try:
            año = int(input("introduzca el año: "))
            working = False  # finaliza la fase uno y sale del bucle
            return año
        except ValueError:
            print("por favor asegurese de que ha escrito el año como un numero entero")


def calcular_bisiesto(año, año_actual):
    if año < año_actual:
        if año % 4 == 0:
            if año % 100 == 0:
                if año % 400 == 0:
                    print("el año", año, "fue bisiesto")
                else:
                    print("el año", año, "no fue bisiesto")
            else:
                print("el año", año, "fue bisiesto")
        else:
            print("el año", año, "no fue bisiesto")
    elif año > año_actual:
        if año % 4 == 0:
            if año % 100 == 0:
                if año % 400 == 0:
                    print("el año", año, "sera bisiesto")
                else:
                    print("el año", año, "no sera bisiesto")
            else:
                print("el año", año, "sera bisiesto")
        else:
            print("el año", año, "no sera bisiesto")
    else:
        if año % 4 == 0:
            if año % 100 == 0:
                if año % 400 == 0:
                    print("el año", año, "es bisiesto")
                else:
                    print("el año", año, "no es bisiesto")
            else:
                print("el año", año, "es bisiesto")
        else:
            print("el año", año, "no es bisiesto")


calcular_bisiesto(solicitar_año(), año_actual)
