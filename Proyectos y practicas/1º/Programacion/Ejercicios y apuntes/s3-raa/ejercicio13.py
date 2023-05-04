# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 23:12:59 2021

@author: Raúl Aguilar -@defalcovgl-
"""

import sys


f1 = float(99999999999999999999999999999999999999999.99999999999999999999999999999999999999999999999999)
f2 = float(88888888888888888888888888888888888888888.88888888888888888888888888888888888888888888888888)
f3 = f1 * f2
print("el resutltado del producto es:", f3)


try:
    f4 = f3 ** 99
    print("el resutltado de la potencia es:", f4)
except OverflowError:
    print("el resultado es demasiado grande ya que el flaot mas grande que "
          "soporta su sistema es", sys.float_info.max, "y el resultado de la"
          "potencia es mas grande que esto")


"""
no se si en todos los sistemas es igual, en mi sistema el maximo es
1.7976931348623157e+308 por lo tanto falla
"""
