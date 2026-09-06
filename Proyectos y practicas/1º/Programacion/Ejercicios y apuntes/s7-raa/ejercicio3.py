import random

MAX = 30
MIN = 1
matriz = [[None, None, None],
          [None, None, None],
          [None, None, None]]
matriz_ordenada = list()
elementos_matriz = list()
elementos_ordenados = list()

# creacion de la matriz sin que ningun elemento se repita
for i in range(len(matriz)):
    vector = matriz[i]
    for j in range(len(vector)):
        matriz[i][j] = random.randint(MIN, MAX)
        while matriz[i][j] in elementos_matriz:
            matriz[i][j] = random.randint(MIN, MAX)
        elementos_matriz.append(matriz[i][j])

# ordena la lista de elemetos
while len(elementos_matriz) > 0:
    minimo = elementos_matriz[0]
    for indice in range(len(elementos_matriz)):
        elemento = elementos_matriz[indice]
        if elemento < minimo:
            minimo = elemento
    elementos_ordenados.append(minimo)
    del (elementos_matriz[elementos_matriz.index(minimo)])


ordenando = True
# coloca los elementos de la lista ordenada en una matriz
while ordenando:
    vector = []
    for elemento in elementos_ordenados:
        if len(vector) < 3:
            vector.append(elemento)

    matriz_ordenada.append(vector)
    for i in vector:
        elementos_ordenados.remove(i)

    if len(matriz_ordenada) == 3:
        ordenando = False


for i in matriz_ordenada:
    print("{}".format(i))
