# -*- coding: utf-8 -*-
6
"""
Created on Sat Oct  2 18:20:29 2021

@author: Raúl Aguilar -@defalcovgl-
"""

"""Realizar un programa que recibe como dato un número positivo correspondiente a una cantidad
de dinero y calcula e imprime el mejor desglose de moneda (mínimo número de unidades
monetarias)."""


def input_dinero():  # pregunta por una cantidad de dinero al usuario
    working = True
    while working:
        try:
            dinero = float(input("euros a convertir: "))
            working = False  # finaliza el bucle
            return dinero
        except ValueError:
            print("por favor asegurese de que ha escrito el dinero como un numero")


def dividir_dinero(dinero):  # el dinero debe introducirse en euros
    # ya no existen los billetes de 500€
    dinero = int(dinero * 100)
    c200 = dinero // 20000  # c de cociente
    r200 = dinero % 20000  # r de resto
    c100 = r200 // 10000
    r100 = r200 % 10000
    c50 = r100 // 5000
    r50 = r100 % 5000
    c20 = r50 // 2000
    r20 = r50 % 2000
    c10 = r20 // 1000
    r10 = r20 % 1000
    c5 = r10 // 500
    r5 = r10 % 500
    c2 = r5 // 200
    r2 = r5 % 200
    c1 = r2 // 100
    r1 = r2 % 100
    c05 = r1 // 50
    r05 = r1 % 50
    c02 = r05 // 20
    r02 = r05 % 20
    c01 = r02 // 10
    r01 = r02 % 10
    c005 = r01 // 5
    r005 = r01 % 5
    c002 = r005 // 2
    r002 = r005 % 2
    c001 = r002 // 1
    din_conv = {"200€": c200,
                "100€": c100,
                "50€": c50,
                "20€": c20,
                "10€": c10,
                "5€": c5,
                "2€": c2,
                "1€": c1,
                "0.5€": c05,
                "0.2€": c02,
                "0.1€": c01,
                "0.05€": c005,
                "0.02€": c002,
                "0.01€": c001}

    return din_conv


dict_dinero_conv = dividir_dinero(input_dinero())  # podria suprimir esta variable pero por legibilidad la dejare

print("{:>10} {}".format("billete", "cantidad"))  # esto es para imprimir como una tabla habria usado un
# dataframe de pandas pero perferia evitar las librerias


for billete, cantidad in dict_dinero_conv.items():  # billete es la clave del diccionario y cantidad el valor
    if cantidad != 0:
        print("{:>10} {}".format(billete, cantidad))  # imprimira linea a linea los billtes necesarios de cada tipo

