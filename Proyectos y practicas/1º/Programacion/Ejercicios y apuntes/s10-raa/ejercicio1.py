"""Definir una función que devuelva una lista a partir de la combinación dos listas pasadas como
argumento, eliminando los duplicados: combine(list1, list2)."""

list1 = [1, 2, 3, 4, 5, 6]
list2 = [4, 5, 6, 7, 8, 9, 9, 9, 9]


def juntarListas(lista1: list, lista2: list) -> list:
    lista = lista1+lista2
    lista=set(lista)
    lista=list(lista)
    return lista

juntarListas(list1, list2)
