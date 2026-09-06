# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 14:06:48 2021

@author: Raúl Aguilar -@defalcovgl-
"""

v1 = "aserejé"
v2 = "jadejé"
v3 = v1 + v2

print(v3)
# se concadenan las dos tal cual sin nada entre medias

try:
    v3 = v1 - v2
    print(v3)
except TypeError:
    print("el operador - no soporta el tipo string")
