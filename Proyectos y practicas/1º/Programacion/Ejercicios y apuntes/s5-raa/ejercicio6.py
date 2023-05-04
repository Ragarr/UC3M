"""Realizar un programa que lea de teclado la nota de un examen de cada uno de los alumnos de
una clase y calcule la media, la nota más alta, la más baja y el número de alumnos presentados
al examen. La entrada de datos se acaba cuando se lee una nota negativa."""


def introducir_notas():
    notas = []
    while True:
        try:
            nota = int(input("introduce la nota del alumno: "))
            if nota < 0:
                return notas
            else:
                notas.append(nota)
        except:
            print("asegurate de que has introducido un vlaor entero")


notas = introducir_notas()
print("la media es: ", sum(notas)/len(notas))
print("la nota mas alta es: ", max(notas))
print("la nota mas baja es: ", min(notas))
print("se han presentado: ", len(notas) + 1, "alumnos")
