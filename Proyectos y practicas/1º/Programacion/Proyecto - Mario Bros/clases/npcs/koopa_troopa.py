from clases.npcs.npc import npc
import constants as c
import pyxel


class koopa_troopa(npc):
    def __init__ (self, coord: list) -> None:
        super().__init__ (coord=coord, sprite=c.sprite_koopa_troopa,ancho=c.ancho_koopa_troopa, alto=c.alto_koopa_troopa)#Esto hay que modificarlo cuando tengamos los sprites
        self.frame_concha= 0

    def colisionar_jugador(self,jugador):
        if self.es_caparazon and self.v_x == 0:
            '''Si el caparazón está parado y el jugador choca con él lo pondrá en movimiento'''
            self.v_x = c.v_caparazon
        elif self.es_caparazon and self.v_x != 0:
            '''Emplearemos este método exclusivamente cuando el jugador salte encima del caparazón en movimiento'''
            self.v_x = 0
        else:
            '''lo convierte en un caparazon'''
            self.es_caparazon = True
            self.frame_concha=pyxel.frame_count+10*c.fps
            self.v_x = 0
            self.sprite = c.sprite_concha
            self.alto = c.alto_concha
            self.coord[1]-=15
            

    def actualizar_estado(self, bloques: list, npcs: list, objetos:list,jugador):
        if pyxel.width+100<self.coord[0]:
            pass
        else:
            self.sufrir_gravedad(jugador)
            self.colisionar_bloques(bloques)
            self.colisionar_npcs(npcs,jugador)
            self.colisionar_con_objeto(objetos,jugador)
            self.actualizar_posicion()
            if self.frame_concha <=pyxel.frame_count and self.frame_concha != 0:
                self.resurgir()

    def morir(self,jugador):
        self.esta_vivo = False
        jugador.score+=c.punt_koopa_troopa


    def resurgir(self):
        '''El koopa troopa volverá a su estado original pasado un tiempo '''
        if self.v_x<0:
            self.v_x = -c.v_koopa_troopa
        else:
            self.v_x = c.v_koopa_troopa
        self.es_caparazon = False
        self.coord[1]-=10
        self.v_y = 0
        self.sprite = c.sprite_koopa_troopa
        self.frame_concha=0


