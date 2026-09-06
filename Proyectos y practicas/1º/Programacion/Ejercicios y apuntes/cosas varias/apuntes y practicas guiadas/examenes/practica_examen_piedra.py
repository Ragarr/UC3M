import random

PARTIDAS = 3
punt_1 = 0
punt_2 = 0
for partida in range(PARTIDAS):
    mano_1 = random.random()
    mano_2=random.random()
    if mano_1 <= 0.33:
        mano_1 = "PIEDRA"
    elif mano_1 <= 0.66:
        mano_1 = "PAPEL"
    else:
        mano_1 = "TIJERA"
    if mano_2 <= 0.33:
        mano_2 = "PIEDRA"
    elif mano_2 <= 0.66:
        mano_2 = "PAPEL"
    else:
        mano_2 = "TIJERA"