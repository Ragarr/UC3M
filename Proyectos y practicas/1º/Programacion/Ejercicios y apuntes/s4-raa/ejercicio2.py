# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 11:14:20 2021

@author: Raúl Aguilar -@defalcovgl-
"""

a, b, c, d = 5, 3, 20, 20
c -= ((a + 1) / b - 3 + a % b)
d -= ((a + 1) / (b + 3 - 4 * a) % b)
print("c:", c)
print("d:", d)

"""
el valor de c sera el mismo menos (a + 1) / ((b - 3) + (a % b))
el valor de d es el mismo menos (a + 1) / (((b + 3) - (4 * a)) % b)

es lo mismo que escribir lo siguiente:
    c = c - ((a + 1) / b - 3 + a % b)
    d = d - ((a + 1) / (b + 3 - 4 * a) % b)
"""
