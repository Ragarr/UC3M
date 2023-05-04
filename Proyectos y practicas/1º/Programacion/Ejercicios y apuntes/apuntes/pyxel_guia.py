"""instalas pip en anaconda promp:
    pip install pyxel -U
    pyxel kitao
    el fichero 03 tiene documentacion 
    el fichero 5 tiene info de los colores

    """

"""
pyxel.init(alto,ancho,caption=titulo de la ventana)
pyxel.image(0).load(0,0,"assets/pyxel_logo_38_16")
#carga una imagen en el banco de imagenes 0 de (cada banco tiene 256x256 pixeles), hay 3 bancos 
.load(pos x donde se carga el sprite, pos y donde se carga el sprite)
pyxel.btnp(pyxel.KEY_Q)
true si se presiona la Q
false si no

pyxel.cls(0) limpia la pantalla con el color 0 (negro)

los colores de implementan como una lista de tuplas: [(R,G,B),(R;G;B),... 15]
pyxel.text(x,y,"..."texto,color=1-15)
pyxel.frame_count # zzdevuelve el frame en el que estas 

pyxel.blt(x,y,nºbanco,x_i,y_i,x_f,y_f)  #x,y donde empieza lo que va a pintar
                                        #nº de banco donde esta almacenada la imagen
                                        #x,y cordenada inicial de la imagen en el banco
                                        #x,y cordenada final del banco
pyxel.load("assets/jummpgame.pyxeres") carga todo el fichero
pyxres que contiene todos los recursos(imagenes y sonidos)
el parametro es la ubicacion del arcivo
playm(cancion:0,is_loop) reproduce musica


en el update se calculan las colisiones
el juego consiste en un while:
    update()
    draw()

enummerate(iterable):
    devuelve una tuplas con pares de indice valor -deconstruye la tupla-
    se usa normalmente asi:
    
    for index, value in enumerate(iterable):
con un *iterable lo divides en su elemento, ej:
def funcion(a,b,c,d,e,f):
    pass
lista=(1,2,3,4,5,6)
funcion(*lista)# esto da a=1,b=2...

.play(musica,canal) # reproduce una cancion


















"""
