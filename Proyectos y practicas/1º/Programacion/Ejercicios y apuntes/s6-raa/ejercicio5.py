"""Escribe un programa que adivine el número que el usuario ha pensado (Entre 1 y 100). En cada
intento el programa generará un número aleatorio y deberá controlar que no se repite. Deberá
ser posible detectar si el usuario está mintiendo (si ha intentado decir todos los números y el
usuario dice que no es ninguno de ellos). El programa contará además el número de intentos
que ha necesitado para adivinarlo."""
import random

inicio = 0
fin = 100
intentos = 0
adivinando = True
numeros_usados = []
print("piensa un numero del", inicio, "al", fin)
while adivinando:
    if intentos == 100:
        print("bro has hecho trampas, no es gracioso, :c")
        adivinando = False
    num = random.randint(inicio, fin)
    while num in numeros_usados:
        num = random.randint(inicio, fin)
    print("¿es el numero", num, "el numero en el que has pensado?")
    # respuesta = True if input("S/N").upper() == "S" else False
    if True if input("S/N").upper() == "S" else False:
        print("he adivinado el numero en", intentos + 1, "intentos")
        adivinando = False
    else:
        intentos += 1
        numeros_usados.append(num)
    if intentos == fin:
        print("bro has hecho trampas, no es gracioso, :c")
        adivinando=False
