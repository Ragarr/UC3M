"""Defina un programa que le permite simular el comportamiento de un cajero automático."""
import os
import random as rnd
import time

import numpy as np


def cls():  # para limpiar la consola
    os.system('cls' if os.name == 'nt' else 'clear')


pin = np.random.choice(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], size=4, replace=True).tolist()
pin = "".join(pin)
saldo = rnd.randint(50, 5000)


def askpin():  # pregunta los numeros al usuario
    asking = True
    while asking:
        try:
            pin = str(input("introduce tu pin: "))
            asking = False
        except ValueError:
            print("por favor asegurese de que ha escrito un pin valido (0000): ")
        return pin


def retiradaEfectivo(saldo_disponible):
    cls()
    asking = True
    while asking:
        try:
            dinero_a_retirar = int(input("introduce el dinero a retirar:"))
            asking = False
        except ValueError:
            print("por favor asegurese de que ha un numero valido: ")

    if dinero_a_retirar > saldo_disponible:
        print("saldo insuficiente, su saldo es de: ", saldo_disponible)
        time.sleep(2)
        return saldo_disponible
    else:
        print("dinero entregado, nuevo saldo: ", saldo_disponible - dinero_a_retirar)
        saldo_disponible -= dinero_a_retirar
        time.sleep(2)
        return saldo_disponible


def ingresoEfectivo(saldo_disponible):
    cls()
    ingreso = int(input(
        "introduzca el dinero: "))  # esto puede dar error al ser una entrada por teclado pero en un cajero nunca sucederia
    print("dinero ingresado, nuevo saldo: ", saldo_disponible + ingreso)
    time.sleep(2)
    return saldo_disponible + ingreso


def menu_operaciones():
    global saldo
    while True:
        cls()
        print("Bienvenido")
        print("------------------------")
        print("1- Ingreso efectivo")
        print("2- Retirada efectivo")
        print("3- Salir")
        op = input("Indique la operación a realizar:")
        if op == "1":
            saldo = ingresoEfectivo(saldo)

        elif op == "2":
            saldo = retiradaEfectivo(saldo)
        elif op == "3":
            cls()
            print("Muchas gracias por operar con nosotros")
            print("Saldo disponible: ", saldo)
            time.sleep(2)
            cls()
            return
        else:
            print("introduzca una operacion valida (1/2/3)")


def menu_inicio():
    global pin
    for intento in range(3):
        pinintroducido = askpin()
        if pinintroducido == pin:
            menu_operaciones()
        else:
            print("numero de intentos disponibles: ", 2 - intento)
    return


print(pin)
menu_inicio()
