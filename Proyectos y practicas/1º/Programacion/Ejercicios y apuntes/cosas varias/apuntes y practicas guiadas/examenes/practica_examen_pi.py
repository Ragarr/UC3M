import random

dentro = 0
fuera = 0
numPuntos = 1000
for _ in range(numPuntos):
    x = random.random()
    y = random.random()
    if (x ** 2) + (y ** 2) <= 1:
        dentro += 1
pi = 4 * (dentro / numPuntos)
print(pi)
