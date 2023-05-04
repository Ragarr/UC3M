# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 13:31:57 2021

@author: Raúl Aguilar -@defalcovgl-
"""

"""Hacer un programa que lea un solo carácter por teclado y diga si es un número o no. Imprimir por
pantalla Es un número o No es un número, según el caso."""


def askchar():
    while True:
        char = input("introduzca un unico caracter: ")
        if len(char) == 1:
            return char

        else:
            print("introduce un unico caracter")


def identify_char(char):
    if char.isalpha():
        print("es una letra")
    elif char.isdigit():
        print("es un numero")
    else:
        print("no es ni un numero ni una letra")


identify_char(askchar())
