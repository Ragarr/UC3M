'''Problem 2 - Multidimensional Vector Class
Implementa una clase, Vector, para representar vectores en un espacio
multidimensional. Por ejemplo:
En un espacio de 3 dimensiones, podríamos querer representar un vector con las
siguientes coordenadas: 5, 2, 3 .
En un espacio de 3 dimensiones, podríamos querer representar un vector con las
siguientes coordenadas: 0,1,-1,3,2.
La clase debe contener los siguientes métodos:
● __init__(self,dim): método constructor que crea un vector con todas las
coordenadas igual a 0 y de dimensión m.
● __len__(self): devuelve la dimensión del vector.
● __str__(self): devuelve un string representando el vector. Por ejemplo, si las
coordenadas del vector son: 3,5,0, el método debería devolver la cadena:
"(3,5,0)".
● __getitem__(self,i): devuelve la i ésima coordenada del vector. the ith
coordinate of the vector. Recuerda que la primera coordenada siempre debe
estar representada por el índice 0.
● __setitem__(self,i,newValue): modifica la i ésima coordenada del vector al
nuevo valor newValue.
● __add__(self,other): devuelve un nuevo vector que es la suma del vector
invocante (self) y del parámetro other.
● __eq__(self,other): devuelve True is los dos vectores son iguales, y False en
otro caso.
● dot(self,other): devuelve el producto escalar de dos vectores.
● cosine_distance(self,other): devuelve la distancia del coseno entre los dos
vectores.'''

class Vector:
    def __init__(self, dim) -> None:
        self.items = []
        self.dim = dim
        for _ in range(dim):
            self.items.append(0)

    def __len__(self):
        return len(self.items)

    def __str__(self) -> str:
        return str(self.items).replace("[","(").replace("]",")")

    def __getitem__(self, i):
        return self.items[i]

    def __setitem__(self, i, newValue):
        self.items[i] = newValue

    def __add__(self, other):
        if self.dim != other.dim:
            raise IndexError("Las dimensiones de los vectores son distintas")
        aux = Vector(self.dim)
        for i in range(len(self.items)):
            aux.items[i] = self.items[i]+other.items[i]
        return aux

    def __eq__(self, other):
        return self.items == other.items

    def dot(self, other):
        '''devuelve el producto escalar de dos vectores'''
        producto = 0
        for i in range(len(self)):
            try:
                producto += self.items[i]*self.items[i]
            except:
                print("los vectores no tienen la misma dimension")
        return producto

    def module(self):
        aux = 0
        for i in self.items:
            try:
                aux += i**2
            except:
                pass
        return aux**0.5

    def cosine_distance(self, other):
        return float(self.dot(other)/self.module()*other.module())


a = Vector(3)
b = Vector(3)
for i in range(len(a)):
    a[i] = i
for i in range(len(b)):
    b[i] = i
print(a)
print(a.dot(b))
print(a[1])
print(a+b)
print(a)
print(b)
print(a == b)
a[1] = 5
print(a == b)
print(a.cosine_distance(b))
