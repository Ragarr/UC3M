"""Crear un nuevo tipo de datos denominado TrianguloRectangulo para representar un
triángulo rectángulo, tendrá dos atributos: base y altura. Crear un método init para recibir
los valores de los campos que compruebe que son correctos. Crear también un programa que
pida la base y la altura de un triángulo rectángulo y que guarde los datos en un objeto triángulo
rectángulo. A continuación, pedir al usuario que pulse 0 para calcular el área del triángulo o 1
para calcular el perímetro. Imprimir por pantalla el resultado de calcular la elección del usuario."""


class TrianguloRectangulo():
    def __init__(self, base, altura) -> None:
        if base.isnumeric():
            self.base = float(base) if float(base) > 0 else 0
        if altura.isnumeric():
            self.altura = float(altura) if float(altura) > 0 else 0

    def area(self):
        return (self.base*self.altura)/2

    def perimetro(self):
        return self.base+self.altura+((self.base**2)+(self.altura**2))**(1/2)


b=int(input("introduce la base"))
h=int(input("introduce la altura"))
triangulo=TrianguloRectangulo(b,h)
ask=int(input("introduce 0 para calcular el area o 1 para calcular el perimetro"))
if ask ==1:
    print(triangulo.area())
elif ask == 1:
    print(triangulo.perimetro())
