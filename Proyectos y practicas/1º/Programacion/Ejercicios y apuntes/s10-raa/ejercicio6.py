"""Crear nuevas versiones de las funciones del ejercicio anterior que realizan cambios en la lista
(append, insert, etc.) para que se realicen sobre la lista original en lugar de devolver una lista
con los cambios."""

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
    list1 = list1+[x]
    return list1


def find(list1, x):
    for i in list1:
        if i == x:
            return True
    return False


def insert(list1, x, index):
    list1[index] = x
    return list1


def remove(list1, x):
    i = 0
    while i < len(list1):
        if list1[i] == x:
            del(list1[i])
            return list1
        i += 1
    return -1


def removeAll(list1, x):
    i = 0
    while i < len(list1):
        if list1[i] == x:
            del(list1[i])
        else:
            i += 1
    return list1


def clear(list1):
    while len(list1) != 0:
        del(list1[0])
    return list1


def pop(list1):
    output = list1[len(list1)-1]
    del(list1[len(list1)-1])
    return output


lista = [1, 2, 2, 3, 4, True, "abc"]
print(lista)
clear(lista)
print(lista)
