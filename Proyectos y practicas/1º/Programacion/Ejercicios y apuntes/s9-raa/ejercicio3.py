"""Ejercicio 3. Crear una función que genere un número aleatorio entre un mínimo y un máximo recibidos
como parámetros. Tendrá un tercer parámetro que indicará si el número debe ser entero,
flotante o complejo.
"""
import random


def randomizarNumero(min: int, max: int, tipo: str):
    """devolvera un valor aleatoreo en el intervalo dado de tipo 'int','float' o 'complex'"""
    if tipo == "int":
        numeroAleatorio = random.randint(min, max)
    elif tipo == "float":
        numeroAleatorio = random.randint(min, max-1) + random.random()
    elif tipo == "complex":
        numeroAleatorio = complex(random.randint(min, max), random.randint(min,max))
    return numeroAleatorio



print(randomizarNumero(1, 10, "complex"))
