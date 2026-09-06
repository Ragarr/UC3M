"""Ejercicio 5. Generar una función que permita escribir de forma correcta las mayúsculas en un texto dado. El
primer carácter de la cadena debe escribirse en mayúscula, así como el primer carácter, no
blanco, después de un ".", "!" ó "?". Por ejemplo, si la función se proporciona con la cadena "¿a
qué hora tengo que estar allí? ¿cuál es la dirección? ", entonces debería
devolver la cadena "¿A qué hora tengo que estar allí? ¿Cuál es la
dirección?". Incluir un programa que lea una cadena del usuario, convierta a mayúsculas las
letras adecuadas utilizando la función y muestre el resultado por pantalla."""


def formatearTexto(texto: str) -> str:
    puntuacion = tuple(".!?")
    texto = list(texto)
    texto[0] = texto[0].upper()

    for i in range(len(texto)):
        char = texto[i]
        texto.append(" ")
        if char in puntuacion and texto[i+1].isalpha():
            texto[i+1] = texto[i+1].upper()
        elif char in puntuacion and not texto[i+1].isalpha():
            for j in range(len(texto)-i):
                if texto[i+j].isalpha():
                    texto[i+j] = texto[i+j].upper()
                    break
    texto = ''.join(str(e) for e in texto)
    texto.strip()
    return texto


print(formatearTexto("¿a qué hora tengo que estar allí? ¿cuál es la dirección?"))
