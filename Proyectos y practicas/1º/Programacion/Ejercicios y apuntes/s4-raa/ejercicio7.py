# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 13:10:12 2021

@author: Raúl Aguilar -@defalcovgl-
"""

"""Crear un programa que reciba por teclado un número de segundos, lo convierta en su
equivalente en horas y lo imprima. Por ejemplo 3.680 segundos son 1 hora, 1 minuto y 20
segundos y debe imprimir 01:01:20 (atención a los ceros de delante)"""


def asksecs():  # pregunta lo segundos al usuario
    working = True
    while working:
        try:
            secs = int(input("los segundos a convertir: "))
            working = False  # finaliza la fase uno y sale del bucle
            return secs
        except ValueError:
            print("por favor asegurese de que ha escrito los segundos como un numero entero")


def convert_secs(secs):
    horas_C = secs // 3600
    horas_R = secs % 3600
    mins_C = horas_R // 60
    mins_R = horas_R % 60
    return {"horas": horas_C, "minutos": mins_C, "segundos": mins_R}


def mostrar_resultado(
        resultado):  # se podria hacer con .format() pero no me acuerdo de como se usaba y creo que asi esta bien
    if resultado["horas"] < 10:
        if resultado["minutos"] < 10:
            if resultado["segundos"] < 10:
                print("0", end="")
                print(resultado["horas"], end=":")
                print("0", end="")
                print(resultado["minutos"], end=":")
                print("0", end="")
                print(resultado["segundos"])
            else:
                print("0", end="")
                print(resultado["horas"], end=":")
                print("0", end="")
                print(resultado["minutos"], end=":")
                print(resultado["segundos"])
        else:
            print("0", end="")
            print(resultado["horas"], end=":")
            print(resultado["minutos"], end=":")
            print(resultado["segundos"])
    else:
        print(resultado["horas"], end=":")
        print(resultado["minutos"], end=":")
        print(resultado["segundos"])


mostrar_resultado(convert_secs(asksecs()))
