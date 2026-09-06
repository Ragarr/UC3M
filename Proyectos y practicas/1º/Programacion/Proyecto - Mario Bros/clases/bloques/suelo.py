from clases.bloques.bloque import bloque
import pyxel
import constants as c
class suelo(bloque):
    def __init__(self, coord: list) -> None:
        # El suelo lo generamos con un método en game, en esencia cada uno es un bloque simple, irrompible y que se encuentra a la altura del suelo. 
        super().__init__(coord, c.sprite_suelo, pyxel.width, pyxel.height/3)
