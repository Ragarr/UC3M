meses = {"Enero": 31, "Febrero": 28, "Marzo": 31, "Abril": 30, "Mayo": 31, "Junio": 30, "Julio": 31, "Agosto": 31,
         "Septiembre": 30, "Octubre": 31, "Noviembre": 30, "Diciembre": 31}
fecha_con_claves = {"dia": None, "mes": None, "año": None, "bisiesto": None}

for k in fecha_con_claves:
    if k != "bisiesto":
        fecha_con_claves[k] = input("introduce el {}: ".format(k))

for k in fecha_con_claves:
    if k == "mes":
        if fecha_con_claves["mes"].isnumeric():
            fecha_con_claves["mes"] = int(fecha_con_claves["mes"])
        if fecha_con_claves["mes"] == 1:
            fecha_con_claves["mes"] = "Enero"
        elif fecha_con_claves["mes"] == 2:
            fecha_con_claves["mes"] = "Febrero"
        elif fecha_con_claves["mes"] == 3:
            fecha_con_claves["mes"] = "Marzo"
        elif fecha_con_claves["mes"] == 4:
            fecha_con_claves["mes"] = "Abril"
        elif fecha_con_claves["mes"] == 5:
            fecha_con_claves["mes"] = "Mayo"
        elif fecha_con_claves["mes"] == 6:
            fecha_con_claves["mes"] = "Junio"
        elif fecha_con_claves["mes"] == 7:
            fecha_con_claves["mes"] = "Julio"
        elif fecha_con_claves["mes"] == 8:
            fecha_con_claves["mes"] = "Agosto"
        elif fecha_con_claves["mes"] == 9:
            fecha_con_claves["mes"] = "Septiembre"
        elif fecha_con_claves["mes"] == 10:
            fecha_con_claves["mes"] = "Octubre"
        elif fecha_con_claves["mes"] == 11:
            fecha_con_claves["mes"] = "Noviembre"
        elif fecha_con_claves["mes"] == 12:
            fecha_con_claves["mes"] = "Diciembre"
    if k == "dia":
        fecha_con_claves[k] = int(fecha_con_claves[k])
    if k == "año":
        fecha_con_claves[k] = int(fecha_con_claves[k])

año = fecha_con_claves["año"]
if año % 4 == 0:
    if año % 100 == 0:
        if año % 400 == 0:
            fecha_con_claves["bisiesto"] = True
        else:
            fecha_con_claves["bisiesto"] = False
    else:
        fecha_con_claves["bisiesto"] = True
else:
    fecha_con_claves["bisiesto"] = False

checking = True
while checking:
    if fecha_con_claves["dia"] > meses[fecha_con_claves["mes"]]:
        if fecha_con_claves["mes"] == "Febrero" and fecha_con_claves["bisiesto"]:
            checking = False
        else:
            print("introduzca una fecha valida")
            for k in fecha_con_claves:
                if k != "bisiesto":
                    fecha_con_claves[k] = input("introduce el {}: ".format(k))
    else:
        checking = False
print("{dia} de {mes} de {año}, {bis}".format(dia=fecha_con_claves["dia"], mes=fecha_con_claves["mes"],
                                              año=fecha_con_claves["año"], bis="año bisiesto." if fecha_con_claves["bisiesto"] else "año no bisiesto."))
