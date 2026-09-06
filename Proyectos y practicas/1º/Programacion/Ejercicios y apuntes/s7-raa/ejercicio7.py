import random

maria = {"nombre": "María",
         "ejerciciosSemanales": [],
         "pruebasSemanales": []}

pedro = {"nombre": "Pedro",
         "ejerciciosSemanales": [],
         "pruebasSemanales": []}
miguel = {"nombre": "Miguel",
          "ejerciciosSemanales": [],
          "pruebasSemanales": []}
sum_clase = 0
media_clase = 0
for i in range(10):
    maria["ejerciciosSemanales"].append(random.randint(0, 10))
    pedro["ejerciciosSemanales"].append(random.randint(0, 10))
    miguel["ejerciciosSemanales"].append(random.randint(0, 10))
    maria["pruebasSemanales"].append(random.randint(0, 10))
    pedro["pruebasSemanales"].append(random.randint(0, 10))
    miguel["pruebasSemanales"].append(random.randint(0, 10))
maria["examen"] = random.randint(0, 10)
pedro["examen"] = random.randint(0, 10)
miguel["examen"] = random.randint(0, 10)

alumnos = [maria, pedro, miguel]
for alumno in alumnos:
    media_ej = 0
    media_pr = 0
    max_ej = 0
    min_ej = 10
    max_pr = 0
    min_pr = 10
    sumatorio_ej = int(0)
    sumatorio_pr = int(0)
    for k in alumno.keys():
        if k == "ejerciciosSemanales":  # calucla la media de los ejercicios semanales
            for ejercicio in alumno[k]:
                sumatorio_ej += ejercicio
                if ejercicio > max_ej:
                    max_ej = ejercicio
                if ejercicio < min_ej:
                    min_ej = ejercicio
            media_ej = sumatorio_ej / len(alumno[k])

        elif k == "pruebasSemanales":
            for prueba in alumno[k]:
                sumatorio_pr += prueba
                if prueba > max_pr:
                    max_pr = prueba
                if prueba < min_pr:
                    min_pr = prueba
            media_pr = sumatorio_pr / len(alumno[k])
    alumno["stats"] = [(media_ej + media_pr) / 2, max_ej if max_ej > max_pr else max_pr,
                       min_ej if min_ej < min_pr else min_pr]
    alumno["nota"] = media_ej * 0.1 + media_pr * 0.3 + alumno["examen"] * 0.6
    if alumno["nota"] >= 9:
        alumno["notaLiteral"] = "Sobresaliente"
    elif alumno["nota"] >= 7:
        alumno["notaLiteral"] = "Notable"
    elif alumno["nota"] >= 6:
        alumno["notaLiteral"] = "Bien"
    elif alumno["nota"] >= 5:
        alumno["notaLiteral"] = "Aprobado"
    else:
        alumno["notaLiteral"] = "suspenso"
    print(
        "{al}: media de ejercicios semanales: {ej}, media de pruebas semanales {pr}, nota del examen: {ex}, nota final: {nota}, {nlit}".format(
            al=alumno["nombre"], ej=media_ej, pr=media_pr, ex=alumno["examen"], nota=alumno["nota"],
            nlit=alumno["notaLiteral"]))
    sum_clase += alumno["nota"]

print("la media de la clase es: {media}".format(media=sum_clase/len(alumnos)))
