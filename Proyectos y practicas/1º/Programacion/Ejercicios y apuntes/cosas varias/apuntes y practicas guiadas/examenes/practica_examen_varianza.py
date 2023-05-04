import random

N = 10
x=list(range(N))
# la media
suma = 0
for i in x :
    suma += i
media = suma / N
# la varianza
suma = 0
for x_i in x:
    suma += ((x_i - media) ** 2)
varianza = suma / N

desv_tipica= varianza**(0.5)
print(media, varianza,desv_tipica)

