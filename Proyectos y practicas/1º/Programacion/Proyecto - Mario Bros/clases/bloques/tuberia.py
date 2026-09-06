from clases.bloques.bloque import bloque 
import constants as c
class tuberia(bloque):
    
    def __init__(self, coord: list, alto:int, inicio = False) -> None:
     #Las tuberías tienen colisiones laterales en los dos extremos por ello no varían    
        
        super().__init__(coord, c.tuberia(alto,inicio), c.ancho_tuberia, alto)
        
    