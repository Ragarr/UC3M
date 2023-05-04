from clases.atrezzo.atrezzo import atrezzo
import constants as c

class arbusto(atrezzo):
    def __init__(self, coord:list) -> None:
        """coord: lista tal que[posicion x, posicion y]"""
        super().__init__(coord, c.sprite_arbusto)