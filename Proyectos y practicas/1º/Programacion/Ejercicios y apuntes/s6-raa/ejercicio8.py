"""Escribe un programa que le pida al usuario introducir una frase y cree una tupla ignorando los
caracteres repetidos. Los caracteres introducidos en la tupla serán convertidos en mayúsculas.
Finalmente mostrará la tupla por pantalla. Por ejemplo: Si el usuario escribe la frase Hi, how
are you? Imprimirá (’H’, ’I’, ’,’, ’ ’, ’O’, ’W’, ’A’, ’R’, ’E’, ’Y’, ’U’, ’?’)"""

frase = input("introduce una frase").upper()

lista=list(frase)
for c in lista:
    repeticiones=lista.count(c)
    if repeticiones>1:
        del(lista[lista.index(c,lista.index(c)+1)])

tupla=tuple(lista)

print(tupla)