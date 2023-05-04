import pyxel
from clases.bloques.bloque import bloque
import random
import constants as c
from clases.objetos.champi import champi
from clases.objetos.flor import flor
from clases.objetos.moneda import moneda


class interrogacion(bloque):
    def __init__(self, coord: list, monedas = False) -> None:
        """este bloque es tanto el de la interrogacion como el bloque liso dependiendo en si esta activo o no"""
        self.__tiene_monedas = monedas #Nos permite diferenciar los bloques de interrogación de monedas de los que contienen power ups. 
        super().__init__(coord, c.sprite_interrogacion,c.ancho_interrogacion,c.alto_interrogacion)
        # De base spwanea la seta, ya que es la más habitual
        # 1champi 2flor u 1monedas
        self.monedas = random.randint(1,6)
        self.__contenido = True #Booleano que nos perimte saber si contiene algo  el bloque
        self.__frame_golpe= 0 #Nos permite poder medir la invunerabilidad del bloque para que no se recogan monedas instantaneamente
    @property 
    def contenido(self):
        return self.__contenido

    @contenido.setter
    def contenido(self,new_contenido):
        self.__contenido = new_contenido

    @property 
    def tiene_monedas(self):
        return self.__tiene_monedas

    @tiene_monedas.setter
    def tiene_monedas(self,new_tiene_monedas):
        self.__contenido = new_tiene_monedas


    def golpear(self, objetos:list, player):
        """Dará un objeto seta si es pequeño o si es grande dará una flor y se convertirta en un bloque plano"""
        self.v_y=-0.3
        if self.__tiene_monedas: 
            if  self.__frame_golpe+c.fps/3<=pyxel.frame_count:
                self.__frame_golpe=pyxel.frame_count 
                if self.monedas >= 1:
                    self.monedas -= 1 # resta una moneda al contenido del bloque
                    objetos.append(moneda([self.coord[0],self.coord[1]-15]))
                    player.dinero += 1
                else:
                    self.sprite = c.sprite_interrogacion_golpeado
        else: #Si golpeas el bloque pequeño te dará un champi, en caso de que seas grande una flor   
            if self.contenido and player.grande:
                objetos.append(flor([self.coord[0],self.coord_iniciales[1]-c.alto_flor-8]))#Crea una flor encima del bloque
                self.contenido = False
            elif self.contenido:
                objetos.append(champi([self.coord[0],self.coord_iniciales[1]-c.alto_champi/2]))#Crea la seta al inicio de su animación
                self.contenido = False
            else:
                pass
                
            self.sprite = c.sprite_interrogacion_golpeado  # reemplazar el sprite de interrogacion por el liso
