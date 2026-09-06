"""
                        input   output
                        causa   efecto
una funcion trnsforma cosas a->b
                             ^-funcion
-def- sirve para definir una funcion
los nombres de funciones van en infinitivo al ser acciones
(a:int,b:int):->int tipas los datos de la funcion los que recive y los que devuelve
>                           <-esta parte se llama signatura
def sumar(a:int,b:int)->int:
    return a+b        ^- la flecha es unicamente informativa
resulltado=sumar(2,3)
print(resultado)
si no se especifica el return se devuele None
return None
    =
return
    =


tambien puedes devolver varios valores como una tupla
return a+b,a,b
    devuelve la tupla: (a+b,a,b)

la tupla se puede asignar a una variable:
a=(1,2)
o se puede deconstruir:
a,b=(1,2) #a=1 b=2
"""

#dia 2


"""
una funcion con varios parametros opcionales funciona asi:

def range(stop, star=0, step=1)

si al llamar una funcion l hago asi se asigna b al parametro a y a al parametro b

def operar(a,b):
    return a*a+b

operar(b=1,a=7) # devolvera 107
operar(1,7) # devolvera 8

una funcion se declara asi y el comentario sale en un popup
def operar(a: int, b:int)->int:
    '''comentario de la funcion'''
"""