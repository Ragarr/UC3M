"""Ejercicio 4. Crear una función que permita realizar la conversión de divisas en una oficina de cambio.
Tendrá como constante local una tupla anidada con las tasas de cambio entre las divisas
consideradas (euro, yen, dólar o libra esterlina) que se puede rellenar mirando la información
en internet. Recibirá como parámetro la divisa de origen, la de destino y la cantidad a cambiar.
Devolverá la cantidad equivalente en la divisa de destino."""


def convertirDivisa(origen: str, destino: str, cantidad: int) -> float:
    """ convierte entre euro, yen, dólar o libra esterlina Recibirá como parámetro la divisa de origen,
     la de destino y la cantidad a cambiar. Devolverá la cantidad equivalente en la divisa de destino."""
    RespectoAlDolar = (1.14, 0.0088, 1.34, 1)  # euro, yen, libra,dolar
    if origen == "euro":
        origen = 0
    elif origen == "yen":
        origen = 1
    elif origen == "libra":
        origen = 2
    elif origen == "dolar":
        origen = 3
    if destino == "euro":
        destino = 0
    elif destino == "yen":
        destino = 1
    elif destino == "libra":
        destino = 2
    elif destino == "dolar":
        destino = 3
    return cantidad*RespectoAlDolar[origen]*(1/RespectoAlDolar[destino])


print(convertirDivisa("yen", "dolar", 10000))
