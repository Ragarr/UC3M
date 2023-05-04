""" Defina un programa que contenga el conjunto de funciones siguientes sin usar los métodos de
lista vistos en la clase de teoría. Debe realizar las comprobaciones. En las funciones que hacen
cambios en la lista no se debe modificar la lista original sino devolver una nueva lista con los
cambios."""


def count(list1, x):
    coincidencias = 0
    for i in list1:
        if i == x:
            coincidencias += 1
    return coincidencias


def index(list1, x):
    for i in range(len(list1)):
        if list1[i] == x:
            return i
    return None


def append(list1, x):
    lista = list1.copy()+[x]
    return lista


def find(list1, x):
    for i in list1:
        if i == x:
            return True
    return False


def insert(list1, x, index):
    lista = list1.copy()
    lista[index] = x
    return lista


def remove(list1, x):
    i = 0
    lista=list1.copy()
    while i < len(list1):
        if list1[i] == x:
            del(lista[i])
            return lista
        i += 1
    return -1


def removeAll(list1, x):
    i = 0
    lista=list1.copy()
    while i < len(lista):
        if list1[i] == x:
            del(lista[i])
        else:
            i += 1
    return lista


def clear(list1):
    lista =list1.copy()
    while len(lista) != 0:
        del(lista[0])
    return lista


def pop(list1):
    lista=list1.copy()
    output = lista[len(lista)-1]
    del(lista[len(lista)-1])
    return output


lista = [1, 2, 2, 3, 4, True, "abc"]
print(lista)
clear(lista)
print(lista)
