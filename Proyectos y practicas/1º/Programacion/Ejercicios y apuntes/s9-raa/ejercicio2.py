"""Ejercicio 2. Crear las siguientes funciones:
a. crearListaNumeros: Crea una lista de 10 elementos aleatorios todos pares y retorna la
lista creada.
b. calcularPropiedades: Calcula el máximo, mínimo y la media de los valores de una lista
recibida como parámetro y los devuelve."""
import random


def crearListaNumeros():
    lista = list()
    for i in range(10):
        num = random.randint(0, 20000)
        if num % 2 == 0:
            lista.append(num)
        else:
            num += 1
            lista.append(num)
    return lista


print(crearListaNumeros())
