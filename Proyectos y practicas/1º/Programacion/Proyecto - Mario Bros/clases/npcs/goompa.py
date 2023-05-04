import constants as c
from clases.npcs.npc import npc
import pyxel


class goomba(npc):
    def __init__(self, coord: list) -> None:
        super().__init__(coord=coord, sprite=c.sprite_goomba, ancho=c.ancho_goomba, alto=c.alto_goomba)

    def colisionar_jugador(self, jugador):
        self.morir(jugador)

    def morir(self, jugador):
        jugador.score += c.punt_goomba
        self.esta_vivo = False

    def actualizar_estado(self, bloques: list, npcs: list, objetos: list, jugador):
        if pyxel.width+100 < self.coord[0]:
            pass
        else:
            self.sufrir_gravedad(jugador)
            self.colisionar_bloques(bloques)
            self.colisionar_npcs(npcs, jugador)
            self.actualizar_posicion()
            self.colisionar_con_objeto(objetos, jugador)
