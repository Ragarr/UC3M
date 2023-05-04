from clases.objetos.objeto import objeto
import constants as c



class flor(objeto):
    def __init__(self, coord: list) -> None:
        super().__init__(coord,c.sprite_flor,15,15)
        self.v_y = -1   

    def actualizar(self, player):
        if self.coord[1] <= self.coord_iniciales[1]+8:
            self.v_y += 0.1
        else:
            self.v_y = 0
        self.actualizar_posicion()
    
    def colisionar_bloques(self, bloques: list):
        for bloque in bloques:
            # animación de la seta subiendo, estática en el sitio hasta que llegue a la parte de arriba quedándose quieto en las x
            if self.colisionando(bloque) and self.coord_iniciales[1]-c.alto_champi/2 + 1 < self.coord[1]:
                self.v_y = -0.1
                self.v_x = 0

    def colisionar_jugador(self):
        self.morir()
 
