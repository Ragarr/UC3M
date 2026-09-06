"""Realizar un programa que juegue a piedra, papel y tijera, con las siguientes especificaciones:
 Habrá un jugador que jugará contra la máquina.
 El número de partidas a realizar será una constante en el programa. El juego se repetirá
todas las veces que indique dicha constante.
 Se solicitará al jugador que introduzca su jugada PIEDRA, PAPEL o TIJERA, mediante el
siguiente mensaje:
¿PIEDRA, PAPEL O TIJERA?
 El programa sacará aleatoriamente su jugada (piedra, papel o tijera). El programa indicará
quién ha ganado según las siguientes reglas:
o La piedra aplasta la tijera (Gana la piedra.)
o La tijera corta el papel (Gana la tijera.)
o El papel envuelve la piedra (Gana el papel.)
o En caso de empate se señalará EMPATE"""
import random

PARTIDA_MAX = 3
JUGADAS_POSIBLES = ["PIEDRA", "PAPEL", "TIJERA"]
partida = 0
print("*****Se realizan",PARTIDA_MAX,"partidas*****")
while partida < PARTIDA_MAX:
    jugada_maquina = random.choice(JUGADAS_POSIBLES)
    jugada_jugador = input("¿PIEDRA, PAPEL O TIJERA?").upper()
    print("el programa saca ", jugada_maquina.lower())
    partida+=1
    if jugada_jugador == jugada_maquina:
        print("*****EMPATE*****")
    elif jugada_jugador == "PIEDRA" and jugada_maquina == "PAPEL":
        print("*****GANA MAQUINA*****")
    elif jugada_jugador == "PIEDRA" and jugada_maquina == "TIJERA":
        print("*****GANA USUARIO*****")
    elif jugada_jugador=="PAPEL" and jugada_maquina == "PIEDRA":
        print("*****GANA USUARIO*****")
    elif jugada_jugador=="PAPEL" and jugada_maquina=="TIJERA":
        print("*****GANA MAQUINA*****")
    elif jugada_jugador=="TIJERA" and jugada_maquina=="PAPEL":
        print("*****GANA USUARIO*****")
    elif jugada_jugador=="TIJERA" and jugada_maquina=="PIEDRA":
        print("*****GANA MAQUINA*****")
    else:
        print("asegurese de haber introducido una eleccion valida")
        partida-=1
