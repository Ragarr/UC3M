from clases.objetos.objeto import objeto
import constants as c
import pyxel
from clases.bloques.escalera import escalera
from clases.bloques.tuberia import tuberia
class estrella(objeto):
    def __init__(self, coord: list) -> None:
        super().__init__(coord,c.sprite_estrella,15,15)
        self.v_y= 1
        self.v_x = 1

    def sufrir_gravedad_estrella(self):
        #Parametro diferenciador del resto de objetos para que la animación de la estrella sea más natural
        if (self.coord[1] < pyxel.height):
            self.v_y += 0.21
        else:
            self.morir()

    def colisionar_bloques(self, bloques: list):
        for bloque in bloques:
            if self.colisionando(bloque):  # comprueba si hay colision
                # comprueba si la colision es por encima
                if ((abs(bloque.coord[1]-(self.coord[1]+self.alto))) <= self.alto):
                    self.v_y = 0
                    #choque lateral con los bloques y cambio de sentido solo con los bloques no movibles y tuberias yas que otros tipos podrían dar pie a errores y estos son los únicos a la altura del suelo
                    self.coord[1] = bloque.coord[1] - self.alto

                    self.coord[1] = self.coord[1]
                    self.v_y = -self.v_y
                  # Salto de la estrella
                    self.v_y = - 3
            if ( (isinstance(bloque,escalera) or isinstance(bloque,tuberia)) and bloque.coord[0]+bloque.ancho < self.coord[0] 
                and bloque.coord[0]+bloque.ancho +2 > self.coord[0] and self.coord[1] > bloque.coord[1]):
                    self.v_x = -self.v_x
            if ( (isinstance(bloque,escalera) or isinstance(bloque,tuberia)) and self.coord[0]+self.ancho < bloque.coord[0] 
                and self.coord[0]+self.ancho + 2> bloque.coord[0] and self.coord[1] > bloque.coord[1]):
                     self.v_x = -self.v_x        


    def colisionar_jugador(self):
        self.morir()


    def actualizar(self, bloques ):
       
        self.sufrir_gravedad_estrella()
        self.colisionar_bloques(bloques)
        self.actualizar_posicion()
        
