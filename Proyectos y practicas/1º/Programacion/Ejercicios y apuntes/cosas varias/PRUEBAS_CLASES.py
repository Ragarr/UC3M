class alumno():
    def __init__(self,n,s,m) -> None:
        self.nombre=n
        self.escuela=s
        self.media = m
    def rename(self,nombre):
        self.nombre=nombre
        print("nombre actualizado a", self.nombre)


alumno1=alumno("raul","valmayor",5)
alumno2=alumno("lola","uc3m",7.77)
alumno1.kill
print(alumno1.escuela)


