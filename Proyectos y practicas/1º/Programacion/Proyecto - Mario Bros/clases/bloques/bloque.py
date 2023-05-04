if __name__ == "__main__":
    print("este archivo no es el principal y no esta pensado para ser ejecutado")
    quit()


class bloque():
    def __init__(self, coord: list, sprite: list, ancho, alto) -> None:
        """coord es una lista de 2 elementos 
        que contiene en este orden los siguienes valores x e y  del origen,
        ancho y alto vienen definidos por el tipo de bloque y sus propiedades
        izquierda y derecha sirve para las colisiones con las tuberias y escaleras, en todos los bloques son falsos, salvo
        para tuberias y escaleras que tienen una diferencia de comportamiento y necesitan los parametros
        """
        self.__coord = coord
        self.__coord_iniciales = self.__coord.copy()
        self.__sprite = sprite
        # aqui hay que añadir el ancho (x) del ladrillo en pixeles para cuando tengamos el archivo con los sprites
        self.__ancho = ancho
        # mas de lo mismo que arriba pero con el largo (y) en pixeles
        self.__alto = alto
        self.__v_y=0
        self.__existe=True

    @property
    def existe(self):
        return self.__existe
   
    @existe.setter #~necesario para cuando el jugador colisiona con el bloque
    def existe(self,new_existe):
        if not isinstance(new_existe,bool):
            raise ValueError("el valor debe ser booleano")
        self.__existe=new_existe

    @property
    def coord(self):
        return self.__coord

    @property
    def v_y(self):
        return self.__v_y
    @v_y.setter
    def v_y(self,v_y:float):
        if not isinstance(v_y, (float,int)):
            raise ValueError("la velocidad debe ser un int o float")
        self.__v_y=v_y
    @property
    def ancho(self):
        return self.__ancho
    @property
    def alto(self):
        return self.__alto
    @property
    def sprite(self):
        return self.__sprite
    
    @sprite.setter # permite que se cambie el sprite de los bloques de interrogacion
    def sprite(self,new_sprite:list):
        if not isinstance(new_sprite, list):
            raise ValueError("el sprite deben ser una lista")
        if len(new_sprite) !=6:
            raise ValueError("la lista sprite debe tener exactamente 6 elementos")
        self.__sprite=new_sprite
  
    @property
    def coord_iniciales(self):
        return self.__coord_iniciales


    def reposicionar(self):
        self.coord[1] = min(self.coord[1]+self.v_y,self.coord_iniciales[1]+2)
        if self.coord[1] < self.coord_iniciales[1]:
            self.v_y+=0.1
        else:
            self.v_y=0
      



