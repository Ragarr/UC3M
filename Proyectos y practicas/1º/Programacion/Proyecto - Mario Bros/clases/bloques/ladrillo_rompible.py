from clases.bloques.bloque import bloque
from clases.objetos.estrella import estrella
import constants as c
class ladrillo_rompible(bloque):
    def __init__(self, coord: list, estrella = False) -> None:
        self.Estrella = estrella #Los ladrillos rompibles en ocasiones esconden estrellas,este bool nos sirve para introducir ese parámetro
        """un bloque con textura de ladrillo que cuando es golpeado por el jugador suelta le da una moneda"""
        super().__init__(coord, c.sprite_ladrillo, c.ancho_ladrillo, c.alto_ladrillo)
        
    def golpear(self,bloques=None,player=None):
        """Solo en algunos casos el bloque contendrá una estrella por ello hemos introducido un bool q nos inidica si hay o no una estrella"""
        self.v_y=-0.3
        if self.Estrella:#Si contiene la estrella, después de ser golpado se convertirá en un bloque golpeado
            bloques.append(estrella([self.coord[0],self.coord_iniciales[1]-c.alto_estrella-16]))
            self.Estrella = False
            self.sprite = c.sprite_interrogacion_golpeado
            #el bloque con estrella ya no es rompible en cualquier otro caso se rompe al instante
        elif self.sprite!= c.sprite_interrogacion_golpeado and player.grande:
             self.romper()

    def romper(self):
        self.existe=False
