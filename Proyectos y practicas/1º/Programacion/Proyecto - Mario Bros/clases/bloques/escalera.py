from clases.bloques.bloque import bloque
import constants as c

class escalera(bloque):
    """este bloque SOLO puede usarse para hacer escaleras o a nivel de suelo, si es true hay colision a la 
    derecha de la escalera"""
    def __init__(self, coord: list, alto:int) -> None:
        #El booleano nos perime saber la posición de la hitbox en función de la orientación de la escalera
        #La escalera funciona como un único bloque moldeable en forma de columna que puede tener hasta 5 bloques de altura
        super().__init__(coord,c.escalera(alto), c.ancho_escalera, alto*c.alto_escalera)
        #Los últimos dos parametros son los correspondientes a la hitbox
    