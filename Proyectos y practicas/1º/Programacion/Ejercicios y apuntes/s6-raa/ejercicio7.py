""" Escribe un programa que pide como dato un número positivo correspondiente a una cantidad
de dinero y calcula e imprime el mejor desglose de moneda como en un ejercicio de una
semana anterior. Usar una tupla para guardar los distintos billetes y monedas que existen.
"""


working = True
while working:
    try:
        dinero = float(input("euros a convertir: "))
        working = False  # finaliza el bucle
    except ValueError:
        print("por favor asegurese de que ha escrito el dinero como un numero")


EFECTIVO_EXISTENTE=(200,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01)
dinero = int(dinero * 100)
c200 = dinero // (EFECTIVO_EXISTENTE[0]*100)  # c de cociente
r200 = dinero % (EFECTIVO_EXISTENTE[0]*100)  # r de resto
c100 = r200 // (EFECTIVO_EXISTENTE[1]*100)
r100 = r200 % (EFECTIVO_EXISTENTE[1]*100)
c50 = r100 // (EFECTIVO_EXISTENTE[2]*100)
r50 = r100 % (EFECTIVO_EXISTENTE[2]*100)
c20 = r50 // (EFECTIVO_EXISTENTE[3]*100)
r20 = r50 % (EFECTIVO_EXISTENTE[3]*100)
c10 = r20 // (EFECTIVO_EXISTENTE[4]*100)
r10 = r20 % (EFECTIVO_EXISTENTE[4]*100)
c5 = r10 // (EFECTIVO_EXISTENTE[5]*100)
r5 = r10 % (EFECTIVO_EXISTENTE[5]*100)
c2 = r5 // (EFECTIVO_EXISTENTE[6]*100)
r2 = r5 % (EFECTIVO_EXISTENTE[6]*100)
c1 = r2 // (EFECTIVO_EXISTENTE[7]*100)
r1 = r2 % (EFECTIVO_EXISTENTE[7]*100)
c05 = r1 // (EFECTIVO_EXISTENTE[8]*100)
r05 = r1 % (EFECTIVO_EXISTENTE[8]*100)
c02 = r05 // (EFECTIVO_EXISTENTE[9]*100)
r02 = r05 % (EFECTIVO_EXISTENTE[9]*100)
c01 = r02 // (EFECTIVO_EXISTENTE[10]*100)
r01 = r02 % (EFECTIVO_EXISTENTE[10]*100)
c005 = r01 // (EFECTIVO_EXISTENTE[11]*100)
r005 = r01 % (EFECTIVO_EXISTENTE[11]*100)
c002 = r005 // (EFECTIVO_EXISTENTE[12]*100)
r002 = r005 % (EFECTIVO_EXISTENTE[12]*100)
c001 = r002 // (EFECTIVO_EXISTENTE[13]*100)
din_conv = {"200€": c200,
            "100€": c100,
            "50€": c50,
            "20€": c20,
            "10€": c10,
            "5€": c5,
            "2€": c2,
            "1€": c1,
            "0.5€": c05,
            "0.2€": c02,
            "0.1€": c01,
            "0.05€": c005,
            "0.02€": c002,
            "0.01€": c001}

print("{:>10} {}".format("billete", "cantidad"))

for billete, cantidad in din_conv.items():  # billete es la clave del diccionario y cantidad el valor
    if cantidad != 0:
        print("{:>10} {}".format(billete, int(cantidad)))  # imprimira linea a linea los billtes necesarios de cada tipo