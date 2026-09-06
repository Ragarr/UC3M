

m1 = list()
m2 = list()
dimensiones_m1 = {"m": 0, "n": 0}
dimensiones_m2 = {"m": 0, "n": 0}

dimensiones_m1["m"] = int(input("introduce el numero de filas de la matriz A:"))
dimensiones_m1["n"] = int(input("introduce el numero de columnas de la matriz A:"))
 # creacioon de la primera matriz
while len(m1)< dimensiones_m1["m"]:
    m1.append([])
for i in range(len(m1)):
    vector=m1[i]
    j = 0
    while len(vector)<dimensiones_m1["n"]:
        texto = "Introduce el número de la posición {m}, {n}: ".format(m=i, n=j)
        j += 1
        print(texto, end="")
        m1[i].append(int(input()))

#impresion de la matriz 1
print("La matriz A es:")
for i in range(len(m1)):
    vector= m1[i]
    for j in range(len(vector)):
        print(m1[i][j], end=" ")
    print("\n")


dimensiones_m2["m"] = int(input("introduce el numero de filas de la matriz B:"))
dimensiones_m2["n"] = int(input("introduce el numero de columnas de la matriz B:"))
#creacion de la segunda matriz
while len(m2)< dimensiones_m2["m"]:
    m2.append([])
for i in range(len(m2)):
    vector=m2[i]
    j = 0
    while len(vector)<dimensiones_m2["n"]:
        texto = "Introduce el número de la posición {m}, {n}: ".format(m=i, n=j)
        j += 1
        print(texto, end="")
        m2[i].append(int(input()))
#impresion de la matriz 2
print("La matriz B es:")
for i in range(len(m2)):
    vector= m2[i]
    for j in range(len(vector)):
        print(m2[i][j], end=" ")
    print("\n")


# creacion de listas con los elementos de cada matriz
elementos_m1 = list()
for i in range(len(m1)):
    vector= m1[i]
    for j in range(len(vector)):
        elementos_m1.append(m1[i][j])
        
elementos_m2 = list()
for i in range(len(m2)):
    vector= m2[i]
    for j in range(len(vector)):
        elementos_m2.append(m2[i][j])
# comprobacion de si un elemento esta en ambas matrices mediante las listas antes creadas
for i1 in range(len(elementos_m1)):
    item1= elementos_m1[i1]
    for i2 in range(len(elementos_m2)):
        item2= elementos_m2[i2]
        if item1==item2:
            print("el elemento {} esta contenido en ambas listas".format(item2))