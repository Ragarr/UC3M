"""Escribe un programa que cree una tupla con los nombres de los meses del año. El programa
pedirá al usuario un número. Si el número está entre 1 y la longitud de la tupla, mostrará el
correspondiente mes del año. En otro caso mostrará un mensaje de error y pedirá otro
número. El programa estará funcionando hasta que el usuario introduzca 0."""


def asknum():
    try:
        num = int(input("introduce un numero entero"))
        return num
    except:
        print("asegurate de haber introducido un numero")
        asknum()



MESES=("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septriembre", "octubre", "noviembre",
"diciembre")
working=True
while working:
    num=asknum()
    if num-1 in range(len(MESES)):
            print(MESES[num-1])
            working=False
    else:
        print("error")

