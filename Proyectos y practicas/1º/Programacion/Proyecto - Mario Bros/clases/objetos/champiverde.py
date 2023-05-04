from clases.objetos.objeto import objeto
import constants as c
from clases.bloques.escalera import escalera
from clases.bloques.tuberia import tuberia



class champi_verde(objeto):

    def __init__(self, coord: list) -> None:
        super().__init__(coord,c.sprite_champi_verde, 15, 15)
        self.v_y = 0
        self.v_x = 1.2


    def actualizar(self, bloques):
        self.sufrir_gravedad()
        self.colisionar_bloques(bloques)
        self.actualizar_posicion()

    def colisionar_bloques(self, bloques: list):
        for bloque in bloques:
            # animación de la seta subiendo, estática en el sitio hasta que llegue a la parte de arriba quedándose quieto en las x
            if self.colisionando(bloque) and self.coord_iniciales[1]-c.alto_champi/2 + 1 < self.coord[1] and not self.coord[1] > self.coord_iniciales[1] and self.coord[0] == self.coord_iniciales[0]  :
                self.v_y = -0.1
                self.v_x = 0

            elif self.colisionando(bloque):  # comprueba si hay colision
                #salto de la seta justo cuando sale de un objeto de interrogación
                if self.colisionando(bloque) and self.coord_iniciales[1]-c.alto_champi/2 < self.coord[1] and not self.coord[1] > self.coord_iniciales[1]:
                    self.v_x = 1.2
                    self.coord[1] -= 10
                    self.v_y = -3

                # comprueba si la colision es por encima
                elif ((abs(bloque.coord[1]-(self.coord[1]+self.alto))) <= self.alto):
                    self.v_y = 0
                    #choque lateral con los bloques y cambio de sentido solo con los bloques no movibles y tuberias yas que otros tipos podrían dar pie a errores y estos son los únicos a la altura del suelo
                    if not isinstance(bloque, escalera) and not isinstance(bloque, tuberia) and self.coord[1] > self.coord_iniciales[1] :
                        self.coord[1] = bloque.coord[1] - self.alto
                    # Salto de la estrella
                    self.v_y = c.v_gravedad
            if ( (isinstance(bloque,escalera) or isinstance(bloque,tuberia)) and bloque.coord[0]+bloque.ancho < self.coord[0] 
                and bloque.coord[0]+bloque.ancho +2 > self.coord[0] and self.coord[1] > bloque.coord[1]):
                    self.v_x = -self.v_x
            if ( (isinstance(bloque,escalera) or isinstance(bloque,tuberia)) and self.coord[0]+self.ancho < bloque.coord[0] 
                and self.coord[0]+self.ancho + 2> bloque.coord[0] and self.coord[1] > bloque.coord[1]):
                     self.v_x = -self.v_x

    def colisionar_jugador(self):
        self.morir()