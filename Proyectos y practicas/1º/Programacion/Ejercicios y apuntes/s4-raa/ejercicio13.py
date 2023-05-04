# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 20:59:32 2021

@author: Raúl Aguilar -@defalcovgl-
"""

"""Crear un programa para simular una calculadora. Debe pedir dos números y el operador (+ - *
/ // **) e imprimir el resultado. Si el operador no es válido debe imprimir Operador
incorrecto y terminar."""


def num_input():
    while True:
        try:
            n1 = float(input("introduce el primer numero: "))
            n2 = float(input("introduce el segundo numero: "))
            return n1, n2
        except ValueError:
            print("por favor asegurese de que ha escrito un numero")


def op_input():
    op_list = ["+", "-", "*", "/", "//", "**"]
    while True:
        operador = input("introduce el operador (+ - * / // **): ")
        if operador in op_list:
            return operador
        else:
            print("operador no valido")
            break


def operar(operador, n1, n2):
    if operador == "+":
        print(n1 + n2)
    elif operador == "-":
        print(n1 - n2)
    elif operador == "*":
        print(n1 * n2)
    elif operador == "/":
        print(n1 / n2)
    elif operador == "//":
        print(n1 // n2)
    elif operador == "**":
        print(n1 ** n2)
    else:
        print("has roto el programa, enhorabuena, te sentiras orgulloso, ahora me enfado y me cierro")


num = num_input()  # lo pido en este orden por seguir el enunciado pero yo lo haria al reves
op = op_input()
operar(op, num[0], num[1])
