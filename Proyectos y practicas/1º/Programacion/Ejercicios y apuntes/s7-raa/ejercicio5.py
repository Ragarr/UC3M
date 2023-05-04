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
