class figura2d():
    def area():
        pass


"""esto es llamar al constructor de la superclase para cuando la subclase hereda atributos de la superclsae
es decir empleado da tecnico y gerente. 
    def __init__(self) -> None:
        super().__init__()
        
        """

class circulo(figura2d):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return 3.14 * (self.radio * self.radio)

class cuadrado(figura2d):
    def __init__(self,lado) -> None:
        self.lado=lado
    def area(self):
        return self.lado*self.la