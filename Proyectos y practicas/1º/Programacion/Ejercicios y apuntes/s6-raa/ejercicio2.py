"""Crea una lista de longitud mayor que 20 e inicializa aleatoriamente sus valores. Crea una
segunda lista y hazla igual a la primera(a = b). Cambia el valor de un elemento de la primera
lista. ¿Cambia también el correspondiente de la segunda lista? ¿Por qué? Crea otras dos listas
y repite el paso previo pero en vez de utilizar el operador de asignación (=) copia los elementos
de la primera lista en la segunda uno a uno. ¿Hay alguna diferencia?
"""

import random
lista=list(range(30))
lista2=lista
print(lista)
print(lista2)
lista[0]="nuevo valor"
print(lista)
print(lista2)
"""se comportan igual ya que es una 'copia superficial'"""
lista3=[]
for i in lista:
    lista3.append(i)
lista[1]="otro nuevo valor"
print(lista)
print(lista3)
"""se comportan de manera independiente ya que son una 'copia profunda'"""
