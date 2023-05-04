from clases.bloques.bloque import bloque
from clases.npcs.bala import bill_bala
import constants as c
import pyxel
class cañon_lanza_bills(bloque):
    def __init__(self, coord: list, sentido = 0, es_alto = False) -> None:
        """Sentido es una variable númerica que puede ser 0,1 u 2.
        Si es 0 los bala__bill se lanzarán hacia la izquierda, en caso de ser 1 a la la derecha y por último 
        en caso de ser 2 en los dos sentidos"""
        self.__sentido = sentido
        if es_alto:
            sprite = c.sprite_cañon_alto
            alto = 32
        else:
            sprite = c.sprite_cañon_bajo
            alto = 16 
        
        #El cañón tiene dos alturas moldeables
        super().__init__(coord, sprite,c.ancho_cañon,alto)
        
    @property
    def sentido(self):
        return self.__sentido
    @sentido.setter
    def sentido(self,new_sentido:float):
        if not isinstance(new_sentido, (float,int)):
            raise ValueError("la velocidad debe ser un int o float")
        self.__sentido = new_sentido 
 

   

    def lanzar(self, npc:list):
            if self.__sentido == 0:
                npc.append(bill_bala([self.coord[0]-self.ancho,self.coord[1]]))   
            elif self.__sentido == 1:
                npc.append(bill_bala([self.coord[0]+self.ancho,self.coord[1]], False)) 
            if self.__sentido == 2:
                npc.append(bill_bala([self.coord[0]-self.ancho,self.coord[1]])) 
                npc.append(bill_bala([self.coord[0]+self.ancho,self.coord[1]],False))
              
                    
                
              