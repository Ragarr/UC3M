"""Crea una lista inicializando sus elementos en la declaración. Asigna a uno de sus elementos otro
de ellos (ej. a[5] = a[3]). Muestra por pantalla ambos elementos. A continuación añade una
instrucción para cambiar el valor del segundo elemento y muestra por pantalla ambos de
nuevo. ¿Ha cambiado también el primero? ¿Por qué? ¿Qué sucede si se cambia el valor del
primero (a[5])?
"""


lista = ["a","b"]

print(lista)
lista[0]=lista[1]
lista[1]="nuevo valor"
print(lista[0], lista[1])
"""el valor del primero no cambia de nuevo a no ser que le des la instruccion de hacerlo"""
lista[1]=lista[0]
print(lista[0],lista[1])
"""ahora los dos valen lo mismo"""
