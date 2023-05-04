from clases.objetos.objeto import objeto
import constants as c

class bandera(objeto):
    def __init__(self, coord: list) -> None:
        super().__init__(coord,c.sprite_bandera, 5,200)

    def colisionar_jugador(self):
        self.v_y=1

    def actualizar(self, player):
        self.actualizar_posicion()
