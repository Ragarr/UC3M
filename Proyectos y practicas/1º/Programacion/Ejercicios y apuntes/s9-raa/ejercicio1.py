"""Ejercicio 1. Crear una función que genere una contraseña de forma aleatoria. La contraseña generada por la
función deberá tener las siguientes características:
a. Longitud aleatoria entre 8 y 12 caracteres.
b. Contener al menos un carácter mayúscula, un número y un símbolo, pudiendo contener más
de uno de los anteriores (no será válida una función que siempre genere contraseñas con
solamente uno de los caracteres anteriores)"""
import random


def GenerarContraseña() -> str:
    abc_minus = tuple("abcdefghijklmnñopqrstuvwxyz")
    abc_mayus = tuple("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
    nums = tuple("1234567890")
    simbolos = tuple("<>-_.,:;!ªº@#·~$%€&¬()='?¿¡+*]^`[¨´}{ç")
    longitud = random.randint(8, 12)
    n_sim = random.randint(1, longitud-4)
    n_num = random.randint(1, longitud-n_sim)
    n_may = random.randint(1, longitud-n_num)
    contraseña = str()
    # numero de mayusculas, minusculas etc escritas
    n_sim_ap, n_num_ap, n_may_ap, n_min_ap = 0, 0, 0, 0

    contraseña = str()
    while len(contraseña) < longitud:
        k = random.random()
        if k < 0.33 and n_sim_ap < n_sim:
            contraseña += simbolos[random.randint(0, len(simbolos)-1)]
            n_sim_ap += 1
        elif k < 0.66 and n_num_ap < n_num:
            contraseña += nums[random.randint(0, len(nums)-1)]
            n_num_ap += 1
        elif n_may_ap < n_may:
            contraseña += abc_mayus[random.randint(0, len(abc_mayus)-1)]
            n_may_ap += 1
        else:
            contraseña += abc_minus[random.randint(0, len(abc_minus)-1)]

    return contraseña


def ValidarContraseña(contraseña: str) -> bool:
    simbolos = tuple("<>-_.,:;!ªº@#·~$%€&¬()='?¿¡+*]^`[¨´}{ç")
    if len(contraseña) < 8 or len(contraseña) > 12:
        return False
    if not any(c in contraseña for c in simbolos):
        return False
    if not any(c.isdigit() for c in contraseña):
        return False
    if not any(c.isupper() for c in contraseña):
        return False
    return True


contraseña = GenerarContraseña()
valida = ValidarContraseña(contraseña)
