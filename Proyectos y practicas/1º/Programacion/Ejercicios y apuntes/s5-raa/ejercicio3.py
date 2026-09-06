"""Escribir un programa que genere e imprima los N números perfectos menores de un cierto
número introducido por teclado. Un número es perfecto si es igual a la suma de todos sus
divisores positivos sin incluir el propio número. Ejemplo:
Indica el límite superior para generar números perfectos y pulsa
Enter:
10000
El número 6 es perfecto
El número 28 es perfecto
El número 496 es perfecto
El número 8128 es perfecto
"""


def askn():  # solicita el numero
    asking = True
    while asking:
        try:
            n = int(input("Indica el límite superior para generar números perfectos y pulsa Enter: "))
            asking = False
        except ValueError:
            print("asegurate de haber introducido un numero entero")
    return n


def esPerfecto(n):  # devuelve true o false si el numero es perfecto o no
    divisores = []
    for i in range(n + 1):  # sumo  uno aqui y a i luego para no dividir por 0
        i += 1
        if n % i == 0:
            divisores.append(n / i)
    if sum(divisores) - n == n:
        return True
    else:
        return False


listaPerfectos = []
for i in range(askn()):
    if i == 0:
        continue
    if i % 10000 == 0:
        print("se ha comprobado hasta el nº ", i)
        for i in listaPerfectos:
            print("El número", i, " es perfecto")
    if esPerfecto(i):
        print("El número", i, " es perfecto")
        # listaPerfectos.append(i)

# for i in listaPerfectos:
#    print("El número", i, " es perfecto")


"""es un programa muy poco eficiente, no se si sera capaz de calcular el 5º en un tiempo razonable"""
