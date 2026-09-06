

if __name__ == "__main__":
    print("este archivo no es el principal y no esta pensado para ser ejecutado")
    quit()

import constants as c
import pyxel
import clases.bloques.bloque

 


class objeto():
    def __init__(self, coord: list, sprite, ancho,alto) -> None:

        self.__coord = coord
        self.__coord_iniciales = coord.copy()
        self.__v_x = 0
        self.__v_y = 0
        self.__existe = True
        self.__ancho=ancho
        self.__alto=alto
        self.__sprite=sprite
    
    @property
    def sprite(self):
        return self.__sprite
    @sprite.setter
    def sprite(self,new):
        if not isinstance(new,(list,tuple)):
            raise ValueError("los sprites deben ser listas o tuplas")
        self.__sprite=new
    @property
    def ancho(self):
        return self.__ancho
    @ancho.setter
    def ancho(self,new):
        self.__ancho=new
    @property
    def alto(self):
        return self.__alto
    @alto.setter
    def alto(self,new):
        self.__alto=new   

    @property
    def v_x(self):
        return self.__v_x
    @v_x.setter
    def v_x(self, new_v_x):
        self.__v_x=new_v_x
    @property
    def coord_iniciales(self):
        return self.__coord_iniciales
    @property
    def existe(self):
        return self.__existe
    @property
    def coord(self):
        return self.__coord
    @coord.setter
    def coord(self, new_coord):
        if len(new_coord) != 2:
            raise ValueError('La lista coord tiene que tener exactamente 2 elementos')
        self.__coord = new_coord
    @property
    def v_x(self):
        return self.__v_x
    @v_x.setter
    def v_x(self,new_v_x):
        if not isinstance(new_v_x,(float,int)):
            raise ValueError('La velocidad debe ser un entero o float')
        self.__v_x=new_v_x
    @property
    def v_y(self):
        return self.__v_y
    @v_y.setter
    def v_y(self,new_v_y):
        if not isinstance(new_v_y, (float, int)):
            raise ValueError('La velocidad debe ser un entero o float')
        self.__v_y = new_v_y
    @property
    def esta_activo(self):
        return self.__esta_activo
    @esta_activo.setter
    def esta_activo(self,esta_activo:bool):
        if not isinstance(esta_activo, bool):
            raise ValueError('el estado de activo debe ser un valor booleano')
        self.__esta_activo=esta_activo
    @property
    def existe(self):
        return self.__existe
    @existe.setter
    def existe (self,new_existe:bool):
        if not isinstance(new_existe, bool):
            raise ValueError('el estado de activo debe ser un valor booleano')
        self.__existe= new_existe
    def morir(self):
        self.__existe = False
    
    def actualizar_posicion(self):
        self.coord[0] += self.v_x
        self.coord[1] += self.v_y
    def colisionando(self,bloque):
        if (abs(bloque.coord[0]-self.coord[0]) < self.ancho
                and abs(bloque.coord[1]-self.coord[1]) < self.alto):  # comprueba si hay colision
            return True
        else:
            return False
    def sufrir_gravedad(self):
        # Influye en los objetos a forma de gravedad para atraerlos al suelo
        if (self.coord[1] < pyxel.height):
            self.__v_y += c.v_gravedad
        else:
            self.morir()
    
