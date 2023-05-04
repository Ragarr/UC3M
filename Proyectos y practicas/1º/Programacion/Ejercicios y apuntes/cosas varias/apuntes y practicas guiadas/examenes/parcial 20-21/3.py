import random

numeros = list()
aciertos = list()
N_JUGADORES = 20
N_TIRADAS = 100
for _ in range(N_JUGADORES):
    numeros.append(random.randint(1, 10))
    aciertos.append(0)

for _ in range(N_TIRADAS):
    num = random.randint(1, 10)
    for i in range(len(numeros)):
        if num == numeros[i]:
            aciertos[i] += 1
nmax = 0
ganador = 0
for i in range(len(aciertos)):
    if aciertos[i] > nmax:
        nmax = aciertos[i]
        ganador = i
print(len(numeros),numeros)
print(len(aciertos), aciertos)
print("ha ganado el jugador ", ganador)
