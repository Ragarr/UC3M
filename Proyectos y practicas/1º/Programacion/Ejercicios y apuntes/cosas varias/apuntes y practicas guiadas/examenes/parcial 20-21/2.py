alimentos = list()
while True:
    print("introduzca un comando")
    print("Add, Remove, Find, List, Stock")
    comando = str(input()).upper()
    if comando == "ADD":
        alimentos.append(str(input("que alimento desea añadir")))
        print("se ha añadido el elementos")
    elif comando == "REMOVE":
        eliminar = str(input("que desea eliminar"))9
        enStock = False
        i = 0
        while i < len(alimentos) and not enStock:
            if eliminar == alimentos[i]:
                enStock = True
                pos_eliminar = i
        if enStock:
            del (alimentos[pos_eliminar])
            print("se ha eliminado un", eliminar)
        else:
            print("no se ha encontrado el alimento a eliminar")
    elif comando == "FIND":
        encontrar = str(input("de que alimento quiere revisar la existencia"))
        enStock = False
        for i in range(len(alimentos)):
            if encontrar == alimentos[i]:
                enStock = True
        if enStock:
            print("el alimento existe en la nevera")
        else:
            print("el alimento no existe en la nevera")
    elif comando == "LIST":
        texto = ""
        for i in set(alimentos):
            texto += "{}, ".format(i)
        texto = texto[:-1]
        print(texto)
    elif comando=="STOCK":
        contabilizar=str(input("alimento a contabilizar"))
        contador=0
        for alimento in alimentos:
            if contabilizar==alimento:
                contador+=1
        print("hay {n} {el}s".format(n=contador,el=contabilizar))
    else:
        print("comando no reconocido")