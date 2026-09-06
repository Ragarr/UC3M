import random
# en un examen solo se puede usar append() len() range() y del()

matriz = [[1, 2, 3],
          [2, 3, 5],
          [6, 7, 8]]
# recorrer una matriz elemento a elemento
for i in range(len(matriz)):  # recorre el indice de los vectores filas
    vector = matriz[i]  # el vector asignado al indice i
    print(vector)
    for j in range(len(vector)):  # recorre el indice de los elementos en los vectores filas
        print(matriz[i][j])

for i in range(len(matriz)):  # recorre el indice de los vectores filas
    matriz[i].append(random.randint(1, 10))  # añado una columna de valores aleatoreos
    for j in range(len(matriz)):  # recorre el indice de los elementos en los vectores filas

        print(matriz)
"""
for i in range(len(matriz)):
    vector = matriz[i]
    for j in range(len(vector)):
        matriz[i][j] #  es cada elemento de la matriz
"""
matriz.append(matriz[0])  # añades la primera fila al final PERO SON DEPENDIENTES al ser una copia superficial
matriz[0][0]=10  #  cambia el valor de la primero y consecuentemente la ultima columna al ser DEPENDIENTES

nuevo_vector=list()
for i in matriz[0]: # asi creas una copia profunda de la lista para que NO sean dependientes
    nuevo_vector.append(i)
matriz.append(0)


nuevo_vector=[x for x in matriz[0]]
print(nuevo_vector)
print(matriz[0])