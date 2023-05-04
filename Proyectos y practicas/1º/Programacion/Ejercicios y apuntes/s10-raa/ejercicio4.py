"""Defina una función que devuelva una tupla imitando el comportamiento de la función
range(start, stop, step), devolviendo una tupla con valores comprendidos entre
start y stop con step pasos entre uno y otro. Configurar los valores por defecto de los
parámetros para que se pueda ejecutar también myrange(start,stop) y myrange(stop).
Se debe comprobar que los rangos son correctos y tienen el tipo correcto (int) en caso
contrario devolver una tupla vacía."""


def myrange(stop: int, start: int = 0, step: float = 1):
    """devuelve una tupla del intervalo dado en step saltos"""
    i=start
    output=[]
    if step==0 or type(stop)!=int or type(start)!=int:
        return ()
    while i<stop:
        output.append(i)
        i+=step
    return tuple(output)

print(myrange(4,-5,3))



