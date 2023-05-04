# UN TIPO ABSTRACTO DE DATOS ES UNA CLASE RESUMIDAMENTE
# UNA ESTRUCTURA DE DATOS ES LA IMPLEMENTACION, CCOMO CONSTRUYO, ORGANIZO LA INFORMACION
'''
HAY TIPOS PRIMITIVOS (LOS QUE NOS FACILITA EL LENGUAJE), EJ:
    SIMPLES:
        INTEGRER, FLOAT,BOOL, STRING.
    COMPLEJOS:
        LIST, DICT, TUPLE

Y TIPOS ABSTRACTOS QUE LOS CREAMOS NOSOTROS: CLASES
'''


class complejo:
    def __init__(self,real:float=0,imaginaria:float=0) -> None:
        self.real=real
        self.imaginaria=imaginaria

    def __str__(self) -> str:
        if self.real==0  and self.imaginaria==0:
            return "0"
        elif self.real==0:
            return "{}i".format(self.imaginaria)
        elif self.imaginaria==0:
            return "{}".format(self.real)
        else:
            return "{real}+{im}i".format(real=self.real,im=self.imaginaria)
    
    def __add__(self,otro):
        if type(otro)!=complejo:
            try:
                return complejo(self.real+otro,self.imaginaria)
            except:
                raise TypeError("HAS INTRODUCIDO ALGO QUE NO ES UN NUMMERO PUTO SUBNORMAL")
        else:
            return complejo(self.real+otro.real,self.imaginaria+otro.imaginaria)

    def mod(self):
        return float((self.real**2+self.imaginaria**2)**0.5)

i1=complejo(1,3)
i2=complejo(2,3)
print(i1.mod())