"""Crear una función que reciba como parámetros una lista y un elemento y devuelva una tupla
con las posiciones que ese elemento ocupa en la lista. Si no está en la lista devolverá la tupla
vacía. 
Crear otra función que, usando la primera, reciba como parámetros dos listas y un
elemento y devuelva si alguna de las apariciones del elemento coincide en la misma posición
en las dos listas."""
def indiceElem(lista:list,elem)->tuple:
    """devolvera una tupla con las posiciones de la lista en las que aparece el elemento dado
    no puede devolver tuplas de un solo elemento"""
    posiciones = list()
    for i in range(len(lista)):
        item=lista[i]
        if item==elem and type(elem)==type(item):
            posiciones.append(i)
    posiciones = tuple(posiciones)
    return posiciones

def coincideIndice(lista1:list,lista2:list, elem)->bool:
    """devuelve el indice de dos elementos que coincidan con mismo indice y valor en dos listas diferentes"""
    posl1=indiceElem(lista1,elem)
    posl2=indiceElem(lista2,elem)
    for i in posl1:
        for j in posl2:
            if i==j:
                return i
    return -1

lista1=[1,2,23,3,4,5,67,7,78,2,213,4354,56,546,7,8,8,0,123,4]
lista2=[4,2,6,5,67,8,6,4,24,56,3,78,8,3,21,12,54,5]

print(coincideIndice(lista1,lista2,2))

