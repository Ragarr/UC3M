"""Crear una numeros de 100 números enteros aleatorios entre el 1 y el 1000 e imprimirla. A
continuación eliminar todos los números pares de la numeros y volverla a imprimir."""
import random

numeros = []
for i in range(100):
    numeros.append(random.randint(1, 1000))
print(numeros)


print([x for x in numeros if x % 2 != 0]) # usando comprension de listas creo una lista con unicamente los impares
pares=[]
for item in numeros:
    if item % 2==0:
        pares.append(item)

for item in pares: #sin usar comprension de listas
    numeros.remove(item)

print(numeros)
