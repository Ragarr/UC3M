import random

EXTRA_VIDA = 25
atacantes = list()
defensores = list()
defensores_muertos = list()
atacantes_muertos = list()
oleada = 0
for i in range(10000):
    atacantes.append(random.randint(10, 50))
for i in range(3200):
    defensores.append(random.randint(10, 50) + EXTRA_VIDA)

while len(atacantes) > 0 and len(defensores) > 0:
    j = 0  # tendremos que usar un indice diferente para atacantes y defensores para evitar el out of range
    for i in range(len(atacantes)):
        if atacantes[i] > defensores[j]:
            atacantes[i] -= defensores[j] / 3
            defensores[j] = None
        else:
            defensores[j] -= atacantes[i] / 3
            atacantes[i] = None
        j += 1
        if j == len(defensores):  # para que no se salga del rango de defensores
            j = 0
        """muertos=0
        for a in range(len(atacantes))
            if atacantes[a]==None:
                atacantes.append(None)
                del (atacantes[a])
                muertos+=1
        atacantes = atacantes[:-muertos]"""
        c=0
        while c<len(atacantes):
            if atacantes[c]==None:
                del (atacantes[c])


