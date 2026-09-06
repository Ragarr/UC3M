9# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 13:19:27 2021

@author: Raúl Aguilar -@defalcovgl-
"""

f1 = 12345678901234567.0
f2 = 12345 678901234568.0

print(f1 - f2)


# el resultado es 0.0 ya que estamos trabajando con valores float (decimales)

i1 = int(f1)
i2 = int(f2)

print(i1 - i2)

# el resultado es 0 ya que estamos trabajando con valores int (enteros)


print(0.3 - 0.2)
fewgf

"""
El resultado es 0.09999999999999998 y no 0.1 debido a que nosotros hacemos
cálculos usando base 10, mientras que la maquina hace cálculos
usando base 2.
0.3 y 0.2 no se pueden representar con precisión en binario sin importar
cuántos dígitos significativos uses, por ello existe margen de error en
ciertos calculos.
"""
