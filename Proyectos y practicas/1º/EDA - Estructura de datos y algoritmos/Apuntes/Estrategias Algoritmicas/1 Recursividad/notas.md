# Recursion
los arboles y los grafos usan recursión
toda recursion necesita eun caso base, un sitio donde la solucion esta ya definida
```
def suma(n):
    if n ==0:
        return 0 # este es el caso base
    
    return n+suma(n-1)
print(suma(12))
```
la recursion debe aproximarse hacia el caso base
## tipos de recursion
### recursion lineal
una llamada recusiva puede producir como maximo una nueva llamada recursiva
### recursion binaria 
una llamada recursiva puede generar dos llamadas recursivas
ej: sucesion de fibonacci 

suma de una lista de numeros usando recursion
### multiple recursion
una llamada recursiova puede generar tres o mas llamadas recursivas
