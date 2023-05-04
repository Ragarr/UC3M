"""Escribir una función que determine cuántos días hay un mes en particular. La función recibirá
dos parámetros: el mes como un número entero entre 1 y 12, y el año como un número entero
de cuatro dígitos. Tener en cuenta la existencia de años bisiestos. Crear un programa que lea un
mes y un año a partir del teclado y muestre por pantalla el número de días en ese mes. """


def calcularDias(mes: int, año: int) -> int:
    """ la funcion devuelve -1 si no se han introducido datos correctos"""
    if mes < 1 or mes > 12:
        return -1
    if año < 0:
        return -1
    if año % 4 != 0:  # no divisible entre 4
        bisiesto = False
    elif año % 4 == 0 and año % 100 != 0:
        bisiesto = True
    elif año % 4 == 0 and año % 100 == 0 and año % 400 != 0:
        bisiesto = False
    elif año % 4 == 0 and año % 100 == 0 and año % 400 == 0:
        bisiesto = True
    if mes == 1:
        return 31
    elif mes == 2:
        if bisiesto:
            return 29
        else:
            return 28
    elif mes == 3:
        return 31
    elif mes== 4:
        return 30
    elif mes==5:
        return 31
    elif mes==6:
        return 30
    elif mes == 7:
        return 31
    elif mes == 8:
        return 31
    elif mes == 9:
        return 30
    elif mes == 10:
        return 31
    elif mes == 11:
        return 30
    elif mes == 12:
        return 31


print("introduce un mes 1-12 y un año")
mes=int(input("mes: "))
año=int(input("año: "))

print("el mes {} de el año {} tiene {} dias".format(mes,año,calcularDias(mes,año)))
