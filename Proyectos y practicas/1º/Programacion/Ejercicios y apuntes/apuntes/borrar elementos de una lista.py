lista=[2,4,None,7,8,9,9,0,None,None]
muertos = 0
for a in range(len(lista)):
    if lista[a] == None:
        lista.append(None)
        del (lista[a])
        muertos += 1

print(lista[:-muertos])