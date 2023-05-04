# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 12:51:54 2021

@author: Raúl Aguilar -@defalcovgl-
"""
"""
hago un try error para que el programa no falle pero para mostrar lo que
ocurriria si la variable no estuviera definida, falla debido a que la variable
no esta definida
"""

try:
    a
    print(a)
except NameError:  # ejecutara el codigo ya que se produce un error de nombre
    print("NameError, la variable no esta definida")
