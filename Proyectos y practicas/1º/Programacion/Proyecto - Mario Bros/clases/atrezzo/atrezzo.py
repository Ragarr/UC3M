if __name__ == "__main__":
    print("este archivo no es el principal y no esta pensado para ser ejecutado")
    quit()
import constants as c
class atrezzo():
    def __init__(self,coord, sprite:list) -> None:
        """coord es una lista que contiene dos elementos, posicion x & posicion y, sprite es una lista que contiene los siguiente en este orden:
        -banco
        -x inicio
        -y inicio
        -ancho
        -alto
        -color de croma
        """
        self.__coord=coord
        self.__sprite=sprite
    @property 
    def sprite(self):
        return self.__sprite
    @property # el getter
    def coord(self):
            return self.__coord

    @coord.setter # el setter
    def coord(self,coord:list):
        if not isinstance(coord,list):
            raise ValueError("las coordenadas deben ser una lista")
        if len(coord) !=2:
            raise ValueError("la lista de coordenadas debe tener exactamente dos elementos")
        if not isinstance(coord[0], (int,float)) or not isinstance(coord[1], (int,float)):
            raise ValueError("las coordenadas deben ser enteros o floats")
        self.__coord=coord









