import random
import time

# prueba del primer metodo
lista = []
inicio = time.time()

for i in range(100000):
    lista.append(random.randint(1, 100))

final = time.time()
print("el primero ha tardado:", final - inicio)

# probamos el segundo metodo
lista = [0] * 100000
inicio = time.time()

for i in lista:
    lista[len(lista) - 1] += random.randint(1, 100)

final = time.time()

print("el segundo ha tardado", final - inicio)

# probamos el tercer metodo
lista = [0] * 100000
inicio = time.time()

for i in lista:
    lista[len(lista) - 1] = lista[len(lista) - 1] + random.randint(1, 100)

final = time.time()

print("el tercero ha tardado", final - inicio)

"""output:
el primero ha tardado: 0.062056541442871094
el segundo ha tardado 0.07006335258483887
el segundo ha tardado 0.08207464218139648
apenas hay diferencia pero la hay"""