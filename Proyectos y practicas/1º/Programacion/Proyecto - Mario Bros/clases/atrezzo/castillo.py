from clases.atrezzo.atrezzo import atrezzo
from clases.atrezzo.atrezzo import atrezzo 
import constants as c
class castillo(atrezzo):
    
    def __init__(self,coord ) -> None:
     #Las tuberías tienen colisiones laterales en los dos extremos por ello no varían    
        
        super().__init__(coord, c.sprite_castillo)