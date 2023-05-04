# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 14:19:17 2021

@author: Raúl Aguilar -@defalcovgl-
"""


txt = "¡Hola don Pepito! \n\t\t ¡Hola don José! \n ¿Pasó usted por mi casa? \n\t\t Por su casa yo pasé. \n ¿Vio usted a mi abuela? \n\t\t A su abuela yo la vi."
splited = txt.split("\n")

t1 = splited[0]
t2 = splited[1]
t3 = splited[2]

print(t1, t2, t3, sep="\n")


# si quisieramos hacerlo sin crear una lista podemos hacerlos asi:


print("\n\n")  # para separar el output de antes con el de ahora

t1 = txt.split("\n")[0]
t2 = txt.split("\n")[1]
t3 = txt.split("\n")[2]

print(t1, t2, t3, sep="\n")
