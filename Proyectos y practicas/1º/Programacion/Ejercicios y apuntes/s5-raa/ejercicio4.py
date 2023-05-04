"""Como sabréis, para leer un número por teclado en Python hay que usar input y luego
convertir la cadena leída a entero o flotante. De esta forma podremos operar con el número
leído. Pero si recibimos algo que no sea un número el programa fallará. Una forma de resolver
este problema es usar la función isdigit() del tipo str, que devuelve True si la cadena es un
número (por ejemplo '342432'.isdigit() devuelve True). Esto funciona para los enteros,
pero no para los flotantes puesto que el punto decimal no se considera un dígito
('343.32'.isdigit() devuelve False). Crear un programa que pide un número por
teclado y continúa pidiéndolo hasta que lo que recibe es un número. Una vez recibido debe
imprimir su cuadrado. El programa debe funcionar tanto para enteros como para flotantes."""


# Creo que lo apropiado es no usar try except en este programa

def asknumber():
    num = input("introduce un numero para calcular su cuadrado: ")
    return num


def conv(number):
    separadores = [",", ".", "'"]
    separadoresNoValidos = [",", "'"]
    caracteresCumplen = []
    comas = 0
    while True:
        for i in number:
            if i.isdigit() or i == "-" or i in separadores:
                if i in separadores:
                    comas += 1
                    if i in separadoresNoValidos:
                        number = number.replace(i, ".")

                caracteresCumplen.append(True)

            else:
                caracteresCumplen.append(False)
        if all(caracteresCumplen) and comas <= 1:
            converted_number = float(number)
        else:
            print("numero no valido")
            conv(asknumber())
        return converted_number


print(conv(asknumber()) ** 2)

