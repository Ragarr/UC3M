if __name__ == "__main__":
    print("este archivo no es el principal y no esta pensado para ser ejecutado")
    quit()
import pyxel
from clases.bloques.suelo import suelo
import constants as c
from clases.objetos.fireball import fireball
from clases.bloques.tuberia import tuberia
from clases.bloques.escalera import escalera
class npc():
    def __init__(self, coord: list, sprite: list,ancho,alto) -> None:
        """
        Cooord es una lista de 2 elementos que contiene la posicón de donde se pinta el sprite
        Sprite es una lista de 6 elementos 
        que contiene en este orden los siguienes valores n este orden:
        -el numero de banco del sprite
        -la pos x donde se inicia el sprite
        -la pos y donde se inicia el sprite
        -la pos x final del sprite
        -la pos y final del sprite
        -color de chroma
        """
        self.__coord = coord
        self.__sprite = sprite
        self.__esta_vivo = True # El npc está vivo 
        self.__v_x = -c.v_npc  # La v_x habrá que modificarla según probemos
        self.__v_y = 0
        self.__ancho=ancho
        self.__alto=alto
        self.__es_caparazon= False
        
    @property
    def ancho(self):
        return self.__ancho
    @property
    def alto(self):
        return self.__alto
    @alto.setter
    def alto(self,new):
        if not isinstance(new, int):
            raise ValueError('la altura  debe ser un entero')
        if new<1:
            raise ValueError('la altura  debe ser mayor que 1')
        self.__alto=new
    @property
    def es_caparazon(self):
        return self.__es_caparazon
    @es_caparazon.setter
    def es_caparazon(self,new):
        if not isinstance(new, bool):
            raise ValueError('El valor de caparazon debe ser un booleano')
        self.__es_caparazon=new
    @property
    def sprite(self):
        return self.__sprite

    @sprite.setter
    def sprite(self, new_sprite: list):
        if not isinstance(new_sprite, list):
            raise ValueError("el sprite deben ser una lista")
        if len(new_sprite) != 6:
            raise ValueError("la lista sprite debe tener exactamente 6 elementos")
        self.__sprite = new_sprite
    @property
    def coord(self):
        return self.__coord
    @coord.setter
    def coord(self, new_coord):
        if len(new_coord)!= 2:
            raise ValueError('La lista coord tiene que tener exactamente 2 elementos')
        self.__coord = new_coord
    @property
    def esta_vivo(self):
       return self.__esta_vivo
    @esta_vivo.setter
    def esta_vivo(self, new_esta_vivo:bool):
        if not isinstance(new_esta_vivo, bool):
            raise ValueError('El valor de estar vivo debe ser un booleano')
        self.__esta_vivo= new_esta_vivo
    @property
    def v_x(self):
        return self.__v_x
    @v_x.setter
    def v_x(self,new_v_x):
        if  not isinstance(new_v_x, (int, float)):
            raise ValueError('El valor de la velocidad es int o float')
        self.__v_x= new_v_x
    @property
    def v_y(self):
        return self.__v_y
    @v_y.setter
    def v_y(self,new_v_y):
        if  not isinstance(new_v_y, (int, float)):
            raise ValueError('El valor de la velocidad es int o float')
        self.__v_y=new_v_y

    def sufrir_gravedad(self,jugador):
        if (self.coord[1] < pyxel.height):
            self.__v_y += c.v_gravedad
        else:
            self.morir(jugador)
    
    def colisionar_bloques(self, bloques: list):
        for bloque in bloques:
            # animación de la seta subiendo, estática en el sitio hasta que llegue a la parte de arriba quedándose quieto en las x
            if self.colisionando(bloque):  # comprueba si hay colision
                self.v_y = 0
            if ( (isinstance(bloque,escalera) or isinstance(bloque,tuberia)) and bloque.coord[0]+bloque.ancho < self.coord[0] 
                and bloque.coord[0]+bloque.ancho +3 > self.coord[0] and self.coord[1] > bloque.coord[1]+5):
                    self.v_x = -self.v_x
            if ( (isinstance(bloque,escalera) or isinstance(bloque,tuberia)) and self.coord[0]+self.ancho < bloque.coord[0] 
                and self.coord[0]+self.ancho + 3> bloque.coord[0] and self.coord[1] > bloque.coord[1]+5):
                     self.v_x = -self.v_x


    
    def colisionar_npcs(self, npcs,jugador):
        for npc in npcs:
            if self.colisionando(npc):
                if npc.__es_caparazon:
                    self.morir(jugador)
                else:
                    self.__v_x = -self.__v_x


    def actualizar_posicion(self):
       self.coord[0] += self.v_x
       self.coord[1] += self.v_y


    def colisionando(self, entity):
        if (abs(entity.coord[0]-self.coord[0]) < self.ancho
                and abs(entity.coord[1]-self.coord[1]) < self.alto):
            # comprueba si hay colision
            return True
        else:
            return False
    
    def colisionar_con_objeto(self,objetos:list,jugador):
        for objeto in objetos:
            if self.colisionando(objeto) and isinstance(objeto,fireball):
                jugador.score+=c.punt_goomba # ambas son iguales
                self.morir(jugador)
                objeto.morir()
