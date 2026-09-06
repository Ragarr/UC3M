frecuencia_ingles = {"E": 0.126, "T": 0.0937, "A": 0.0824, "O": 0.077, "N": 0.068}
frecuencia_espanol = {"E": 0.1368, "T": 0.0535, "A": 0.1253, "O": 0.0868, "N": 0.0798}
apariciones_texto = {"E": 0, "T": 0, "A": 0, "O": 0, "N": 0}
frecuencia_texto = {"E": 0, "T": 0, "A": 0, "O": 0, "N": 0}
diferencia_ingles = 0
diferencia_español = 0
texto = input("introduce el texto")
texto = texto.upper()
letras = 0
for char in texto:
    if char.isalpha():
        letras += 1
        if char == "E":
            apariciones_texto["E"] += 1
        if char == "T":
            apariciones_texto["T"] += 1
        if char == "A":
            apariciones_texto["A"] += 1
        if char == "O":
            apariciones_texto["O"] += 1
        if char == "N":
            apariciones_texto["N"] += 1

for k in apariciones_texto.keys():
    frecuencia_texto[k] = apariciones_texto[k] / letras

for k in frecuencia_texto.keys():
    diferencia_ingles += abs(frecuencia_ingles[k] - frecuencia_texto[k])
    diferencia_español += abs(frecuencia_espanol[k] - frecuencia_texto[k])
if diferencia_ingles < diferencia_español:
    print("el texto es ingles")
else:
    print("el texto es español")
print(frecuencia_texto, diferencia_español, diferencia_ingles)
