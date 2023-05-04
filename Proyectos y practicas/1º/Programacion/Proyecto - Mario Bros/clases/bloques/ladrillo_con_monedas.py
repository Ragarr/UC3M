import pyxel
from clases.bloques.bloque import bloque
import constants as c
import random
from clases.objetos.moneda import moneda


class ladrillo_con_monedas(bloque):
    def __init__(self, coord: list) -> None:
        """visualmente es igual que los demas ladrillos pero contiene una cantidad aleatorea de monedas"""
        super().__init__(coord, c.sprite_ladrillo, c.ancho_ladrillo, c.alto_ladrillo)
        # numero de monedas que contiene el bloque
        self.monedas = random.randint(1,6)
        self.__frame_golpe= 0 #Nos permite poder medir la invunerabilidad del bloque para que no se recogan monedas instantaneamente
        # controla si el objeto tiene colisiones

    def golpear(self, objetos:list,player = None):
        """dara monedas hasta que no haya, entonces se rompera"""
        self.v_y -= 0.3
        if player.grande:
            if  self.__frame_golpe+c.fps/3<=pyxel.frame_count:
                self.__frame_golpe= pyxel.frame_count 
                if self.monedas < 1:
                    self.romper()
                self.monedas =(self.monedas- 1) # resta una moneda al contenido del bloque
                objetos.append(moneda([self.coord[0],self.coord[1]-15]))
                player.dinero += 1

        
        
    def romper(self):
        self.existe=False
 # para deshabilitar las colisiones con el objeto
