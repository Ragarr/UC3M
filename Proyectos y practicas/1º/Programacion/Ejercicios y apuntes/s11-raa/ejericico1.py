"""Crear una clase Estudiante que represente a un estudiante de primer año. Sus atributos son:
nombre, apellido, nota programación, nota álgebra, nota cálculo, nota física,
nota técnicas y nota humanidades. 
Crear un método init que reciba valores para cada uno
de los atributos y compruebe que los rangos de los valores de las notas introducidas es el
adecuado (si son incorrectos la nota se inicializa con un 0). Escribir un programa que cree un
objeto de este tipo, solicite al usuario los valores de los campos por teclado e imprima por
pantalla la información del estudiante. """


class estudiante():
    def __init__(self, nombre, apellidos, n_progra, n_alegebra, n_calculo, n_fisica, n_tecnicas, n_humanidades) -> None:
        self.nombre = nombre
        self.apellidos = apellidos
        self.nota_progra = n_progra if n_progra >= 0 and n_progra <= 10 else 0
        self.nota_algebra = n_alegebra if n_alegebra >= 0 and n_alegebra <= 10 else 0
        self.nota_calculo = n_calculo if n_calculo >= 0 and n_calculo <= 10 else 0
        self.nota_fisica = n_fisica if n_fisica >= 0 and n_fisica <= 10 else 0
        self.nota_tecnicas = n_tecnicas if n_tecnicas >= 0 and n_tecnicas <= 10 else 0
        self.nota_humanidades = n_humanidades if n_humanidades >= 0 and n_humanidades <= 10 else 0

    def __str__(self) -> str:
        return "{} {} ha obtenido un {} en progra, un {} en algebra, un {} en calculo, un {} en fisica, un {} en tecnicas y un {} en humanidades".format(
            self.nombre, self.apellidos, self.nota_progra,  self.nota_algebra, self.nota_calculo, self.nota_fisica, self.nota_tecnicas, self.nota_humanidades)

nombre = input("introduzca el nombre")
apellidos = input("introduzca los apellidos")
n_progra = int(input("introduzca la nota de programación"))
n_alegebra = int(input("introduzca la nota de algebra"))
n_calculo = int(input("introduzca la nota de calculo"))
n_fisica = int(input("introduzca la nota de fisica"))
n_tecnicas = int(input("introduzca la nota de tecnicas"))
n_humanidades = int(input("introduzca la nota de humanidades"))
carla = estudiante(nombre, apellidos, n_progra, n_alegebra,
                   n_calculo, n_fisica, n_tecnicas, n_humanidades)

print(carla)
