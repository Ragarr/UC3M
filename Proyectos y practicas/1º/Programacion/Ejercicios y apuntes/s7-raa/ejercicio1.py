import random

matriz = list()
n = 3  # listas y columnas de la matriz cuadrada contando el 0
texto = ""

# crea la matriz nxn con cosas aleatoreas
while len(matriz) <= n:
    matriz.append([])
for i in matriz:
    while len(matriz[matriz.index(i)]) < n:
        matriz[matriz.index(i)].append(random.randint(1, 10))
# crea un ultimo vector
for fila in range(len(matriz[n])):
    matriz[n][fila] = 0
    for columna in range(n):
        matriz[n][fila] += matriz[columna][fila]


for fila in range(len(matriz[n])):
    for columna in range(n):
        texto += " {} +".format(matriz[columna][fila])  # uso la traspuesta ya que la suma es un ultimo vector y no el
                                                        # ultimo componente de los vectores

    texto= texto[: -2]
    print(texto+" = ", matriz[n][fila])
    texto=""

print(texto)
