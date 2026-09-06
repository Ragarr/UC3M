import pyxel
from clases.bloques.bloque import bloque
import constants as c
from clases.objetos.champiverde import champi_verde



class bloque_invisible(bloque):
    def __init__(self, coord: list, monedas = False) -> None:
        """este bloque es tanto el de la interrogacion como el bloque liso dependiendo en si esta activo o no""" 
        super().__init__(coord, c.sprite_invisible,c.ancho_ladrillo,c.alto_ladrillo)
        # Contiene la seta verde que da al jugador un vida extra
        self.__contenido = True #Booleano que nos perimte saber si contiene algo  el bloque
 
    @property 
    def contenido(self):
        return self.__contenido

    @contenido.setter
    def contenido(self,new_contenido):
        self.__contenido = new_contenido

    def golpear(self, objetos:list, player):
        """Dará una seta verde y se convertirá en un bloque golpeado"""
        self.v_y=-0.3
        if self.contenido: 
            self.sprite = c.sprite_interrogacion_golpeado
            objetos.append(champi_verde([self.coord[0],self.coord_iniciales[1]-c.alto_champi/2]))#Crea la seta al inicio de su animación
            self.contenido = False
        else:
            pass