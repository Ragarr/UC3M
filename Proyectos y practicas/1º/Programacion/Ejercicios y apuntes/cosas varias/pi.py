# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 14:56:00 2021

@author: Raúl Aguilar -@defalcovgl-
"""

import math
pi=0
n=1
sol=0
while True:
    i=1/(n**2)
    sol=sol+i
    pi=(math.sqrt(sol*6))
    n=n+1
    if n%10000==0:
        print("pi es: ", pi,"en la sum nº: ", n)