"""Escribe un programa que haga lo siguiente:
1. Pregunta al usuario por el tamaño de la lista a crear que debe ser mayor que 0. En
caso contrario continuará preguntando por el tamaño hasta obtener uno correcto.
2. Rellena la lista aleatoriamente con números flotantes entre 1 y 49
3. Crea una variable llamada ‘total’
4. Suma la parte entera de todos los elementos de la lista y almacena el valor en la
variable ‘total’
5. Muestra por pantalla la lista y el valor de ‘total’ """
import random

tamaño_lista = 0
while tamaño_lista <= 0:
    tamaño_lista = int(input("introduce el tamaño de la lista como un entero"))
lista = list(range(tamaño_lista))
for i in lista:
    lista[i]=random.randint(1,49)
total=sum(lista)
print(lista)
print(total)