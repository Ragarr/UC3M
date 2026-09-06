saldo_cuentas = {}
balance_global = 0

def crear_cuenta(n):
    saldo_cuentas[n] = 0

def ingresar_dinero(n, m):
    saldo_cuentas[n] += m
    global balance_global
    balance_global += m

def traspasar_dinero(n, m, x):
    saldo_cuentas[n] -= x
    saldo_cuentas[m] += x
    global balance_global

def retirar_dinero(n, m):
    saldo_cuentas[n] -= m
    global balance_global
    balance_global -= m

def consultar_saldo(n):
    return saldo_cuentas[n]

# Abrir el archivo de comandos
with open("/home/defalco/Practicas_SSOO/Practica 3/ssoo_p3_multihilo_2023/file.txt", "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Separar los elementos de la línea en una lista
        elementos = linea.split()

        # Realizar el comando correspondiente según el primer elemento de la lista
        if elementos[0] == "CREAR":
            crear_cuenta(int(elementos[1]))
        elif elementos[0] == "INGRESAR":
            ingresar_dinero(int(elementos[1]), int(elementos[2]))
        elif elementos[0] == "TRASPASAR":
            traspasar_dinero(int(elementos[1]), int(elementos[2]), int(elementos[3]))
        elif elementos[0] == "RETIRAR":
            retirar_dinero(int(elementos[1]), int(elementos[2]))
        elif elementos[0] == "SALDO":
            print("Saldo de la cuenta {}: {}".format(elementos[1], consultar_saldo(int(elementos[1]))))

# Imprimir el balance global al finalizar
print("Balance global: {}".format(balance_global))
