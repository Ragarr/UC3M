import constants as c
from clases.npcs.npc import npc
import pyxel
from clases.bloques.tuberia import tuberia
from clases.bloques.escalera import escalera


class bill_bala(npc):
    def __init__(self, coord: list, izquierda = True) -> None:
        if izquierda:
            bsprite = c.sprite_bala
            sentido_v_x = -3 
        else:
            bsprite = c.sprite_bala_i
            sentido_v_x = 3 
        # Esto hay que modificarlo cuando tengamos los sprites
        super().__init__(coord=coord, sprite = bsprite, ancho=c.ancho_bala, alto=c.alto_bala)
        self.v_x = sentido_v_x
        self.es_caparazon = True
        

    def colisionar_jugador(self, jugador):
        self.morir(jugador)
        
    def morir(self,jugador):
        self.esta_vivo = False
    
    def colisionar_bloques(self, bloques: list):
        for bloque in bloques:
            # animación de la seta subiendo, estática en el sitio hasta que llegue a la parte de arriba quedándose quieto en las x
            if self.colisionando(bloque):  # comprueba si hay colision
                self.v_y = 0
            if ( (isinstance(bloque,escalera) or isinstance(bloque,tuberia)) and bloque.coord[0]+bloque.ancho < self.coord[0] 
                and bloque.coord[0]+bloque.ancho +3 > self.coord[0] and self.coord[1] > bloque.coord[1]+5):
                    self.esta_vivo = False
            if ( (isinstance(bloque,escalera) or isinstance(bloque,tuberia)) and self.coord[0]+self.ancho < bloque.coord[0] 
                and self.coord[0]+self.ancho + 3> bloque.coord[0] and self.coord[1] > bloque.coord[1]+5):
                    self.esta_vivo = False

    def actualizar_estado(self, bloques: list, npcs: list, objetos: list, jugador):
        if pyxel.width < self.coord[0]:
            pass
        else:
            self.colisionar_bloques(bloques)
            self.colisionar_npcs(npcs, jugador)
            self.actualizar_posicion()
        