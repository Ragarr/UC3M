import random

notas=[]
nota_min=10
nota_max=0

for i in range(5):
    notas.append(random.randint(1,10))


for juez, nota in enumerate(notas):
    print("el juez", juez+1,"da al gimnasta",nota,"punto" if nota==1 else "puntos")


for nota in notas:
    if nota<nota_min:
        nota_min=nota
    if nota>nota_max:
        nota_max=nota
print("La menor puntuación obtenida es",nota_min,"y la mayor puntuación es",nota_max)