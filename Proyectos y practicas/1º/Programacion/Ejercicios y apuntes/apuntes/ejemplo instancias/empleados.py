class empleado():
    def __init__(self, salario) -> None:
        self.salario=salario

class   tecnico(empleado):
    def __init__(self, salario, puesto) -> None:
        super().__init__(salario)
        self.puesto=puesto

dani=tecnico(1000,"profesor")
print(dani.salario,dani.puesto)

"""quiero preguntar respecto a esto:
    
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
        
        """
"""con ddos _ haces un atributo clase funcion etc privado, ej:
    __tecnico=0 es privado
    self.__salario=0 es privado
    solo se podran cambiar mediante un metodo interno
    para obtener desde fuera una variable privada necesitas crear un metodoque lo devuelva
    def getsalario(self):
        return self.__salario
    esto se llaman metodos privados y publicos
    y atributos privados y publicos"""