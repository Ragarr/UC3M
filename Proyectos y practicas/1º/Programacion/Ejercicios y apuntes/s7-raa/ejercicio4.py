import random

# creacion del  inventario_tableros
inventario_tableros = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(len(inventario_tableros)):
    inventario_tableros[i] = random.randint(0, 10)

# impresion del numero de inventario_tableros
print("Almacenados:    tamaño1 tamaño2 tamaño3 tamaño4 tamaño5 tamaño6 tamaño7 tamaño8 tamaño9 tamaño10")
print("                ", end="")
for i in range(len(inventario_tableros)):
    print("{}".format(inventario_tableros[i]), end="       " if len(str(inventario_tableros[i])) < 2 else "      ")
    # el condicional para que no se desacompase si hay un 10 que ocupa mas que los demas
print("")
clientes = int(input("Introduce el número de clientes: "))
while clientes < 1:
    print("debe haber almenos un cliente")
    clientes = int(input("Introduce el número de clientes: "))

# creacion de una matriz conn una fila=cliente col=tipo de tablero
matriz_clientes = list()
for i in range(clientes):
    matriz_clientes.append([])
    for j in range(10):
        matriz_clientes[i].append(None)

# rellenar la matriz alñeatorieamente
for i in range(len(matriz_clientes)):
    vector_cliente = matriz_clientes[i]
    for j in range(len(vector_cliente)):
        matriz_clientes[i][j] = random.randint(0, 4)

# impresion de pedidios originales
print("Pedidos originales")
for i in range(len(matriz_clientes)):
    vector_cliente=matriz_clientes[i]
    print("Cliente {n_cliente}:      ".format(n_cliente=i), end="")
    for j in range(len(vector_cliente)):
        print("{}".format(matriz_clientes[i][j]), end="       " if len(str(matriz_clientes[i][j])) < 2 else "      ")
    print("")

# creacion de la matriz de pedidos pendientes (vacia) de las mismas dimensiones que la matriz clientes
matriz_pendientes = list()
for i in range(clientes):
    matriz_pendientes.append([])
    for j in range(10):
        matriz_pendientes[i].append(None)

for i in range(len(matriz_clientes)):
    vector_cliente = matriz_clientes[i]
    for j in range(len(vector_cliente)):
        tableros = matriz_clientes[i][j]
        diferencia = tableros - inventario_tableros[j]
        if diferencia > 0:
            matriz_pendientes[i][j] = diferencia
            inventario_tableros[j] = 0
        else:
            matriz_pendientes[i][j] = 0
            inventario_tableros[j] = inventario_tableros[j] - tableros

# impresion de pedidios pendientes
print("Pedidos pendientes")
for i in range(len(matriz_pendientes)):
    vector_cliente=matriz_pendientes[i]
    print("Cliente {n_cliente}:      ".format(n_cliente=i), end="")
    for j in range(len(vector_cliente)):
        print("{}".format(matriz_pendientes[i][j]), end="       " if len(str(matriz_pendientes[i][j])) < 2 else "      ")
    print("")