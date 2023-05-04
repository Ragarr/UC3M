"""Crear una clase Dado, con campos nombre y tiradas, para simular una partida de juego de
dados. Crear un método init que recibe el nombre del jugador y un entero n que representa el
número de tiradas (debe ser mayor que cero). Asignará el nombre al campo correspondiente y
creará una lista de n posiciones rellena con números entre el 1 y el 6. Se simulará una partida de
dados, preguntando a cada jugador su nombre y el número de tiradas del juego. El ganador será
el que tenga el mayor número de dados iguales. En caso de empate ganará el jugador cuyos
dados sumen más."""
import random
class Dado():
    def __init__(self,nombre:str,tiradas:int) -> None:
        self.nombre=nombre
        if tiradas >0:
            self.tiradas=tiradas
        else:
            raise ValueError(" las tiradas deben ser mayores que 0")
    def tirarDado():
        return random.randint(1,6)
    

jugadores=list()
tiradas=int(input("introduzca el numero de tiradas del juego"))
puntuaciones=list()
for i in range(6):
    nombre="introduzca el nombre del jugador {}".format(i+1)
    nombre=str(input(nombre))
    jugadores.append(Dado(nombre,tiradas))
for i in range(tiradas):
    for j in range



