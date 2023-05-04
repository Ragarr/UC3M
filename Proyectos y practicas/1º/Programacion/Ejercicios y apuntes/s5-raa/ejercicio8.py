import random

def tirar_dados():
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    return dado1, dado2


def preguntar():
    pregunta = input("¿Desea seguir tirando? Sí|No").upper()
    if pregunta == "SI":
        return True
    elif pregunta == "NO":
        return False
    else:
        print("por favor conteste unicamente si o no")
        return None


PARTIDA_MAX = 3
partida = 0
puntuaciones = [0, 0]
jugadores = [1, 2]
excedido = False
for partida in range(PARTIDA_MAX):
    for jugador in jugadores:
        if excedido:
            jugando = False

        else:
            jugando = True
        while jugando:
            excedido = False
            print("PARTIDA", partida + 1, "- JUGADOR", jugador)
            dados = tirar_dados()
            puntuaciones[jugador - 1] += sum(dados)
            print("Ha obtenido en los dados", dados[0], ",", dados[1])
            print("Su puntuación acumulada es", puntuaciones[jugador - 1])
            if puntuaciones[jugador - 1] > 21:
                print("***********GANA EL JUGADOR", jugadores[-jugador], "***********")
                jugando = False
                excedido = True
                puntuaciones[0] = 0
                puntuaciones[1] = 0

            else:
                jugando=preguntar()
                while jugando==None:
                    jugando=preguntar()

    if puntuaciones[0] < puntuaciones[1]:
        print("***********GANA EL JUGADOR 2***********")
    elif puntuaciones[0] > puntuaciones[1]:
        print("***********GANA EL JUGADOR 1***********")
    elif puntuaciones[0] == puntuaciones[1] and not excedido:
        print("***********EMPATE***********")
    else:
        excedido=False
    puntuaciones[0] = 0
    puntuaciones[1] = 0




















