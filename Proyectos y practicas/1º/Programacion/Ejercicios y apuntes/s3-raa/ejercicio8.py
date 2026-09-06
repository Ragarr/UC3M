# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 13:53:15 2021

@author: Raúl Aguilar -@defalcovgl-
"""

v1 = 5
v2 = 0

try:
    v3 = v1/v2
    print("se ha dividido exitosamente, resultado: ", v3)
except ZeroDivisionError:
    print("ha ocurrido un error al intentar dividir por 0")

v1 = float(v1)
v2 = float(v2)
try:
    v3 = v1/v2
    print("se ha dividido exitosamente, resultado: ", v3)
except ZeroDivisionError:
    print("ha ocurrido un error al intentar dividir por 0 aunque fueran decimales")
# volvera a ocurrir un error
