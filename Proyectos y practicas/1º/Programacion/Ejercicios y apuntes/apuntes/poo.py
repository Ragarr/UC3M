# abstracción, encapsulamiento, herencia y polimorfismo

class persona():
    # esto se llama el constructor-> matrix 1
    def __init__(self, nombre=None, apellido=None, edad=None, altura=None) -> None:
        # self hace referencia a la region de memoria donde esta guardada el objeto de tipo persona
        # es unica en cada variable en este caso para cada persona
        # a la funcion le pasas parametros para que se asignene en el momento de la construccion
        # se le pueden pasar parametros por defecto

        self.nombre = nombre
        self.apellidos = apellido
        self.edad = edad
        self.altura = altura
        self.vida = 100

    def morir(self):
        self.vida = 0

    def __str__(self) -> str:
        return self.nombre + " " + self.apellidos + " mide " + str(self.altura) 

    def estado(self):
        print(self.nombre, self.apellidos, "tiene",
              self.edad, "años y mide", self.altura)


dani = persona("dani", "sin apellido", 39, 175)
dani.estado()
beto = persona()
beto.estado()
print(dani)
print(dani.__str__())


"""
las clases tienen estructura y comportamiento:
    la estructura son los atributos
    el comportamiento son las **funciones -que se llaman metodos al estar dentro de las clase-
los objetos 

"""
"""
los conceptos se definen los objetos se crean:
la clase es un concepto(un concepto esta en el imaginario y una clase en un ordenedor)
    un concepto es la idea universal y necesaria que tenemos todos de algo 
    un concepto metido en un ordenador es una clase 

a partir de muchos objetos creo el concepto 
"""
"""
p1=persona()
p2=persona()
p3=p1
p3 y p1 son DOS variables con la misma region de memoria

"""
