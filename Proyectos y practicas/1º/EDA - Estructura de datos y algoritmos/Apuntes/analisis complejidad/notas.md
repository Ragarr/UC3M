# un alogritmo 
es un conjunto de pasos que tiene que resolver un problema 
- debe de ser correcto
- debe ser eficiente

# el rendimiento
se mide en dos parametros, la complejidad temporal(velocidad) y la espacial(memoria)
hay dos formas de analizar el algoritmo:

- analisis empirico
- analisis teorico

## analisis empirico
- escrbir el programa
- medir instrucciones para medir el tiempo
- ejecutar para distintos tamaños
- importar a un excel y ver un grafico de dispersion

problemas del analisis empririco:
- hay que implementar los algoritmos
- mismo entorno para comparar TODOS los algoritmos.
- los resultados pueden no ser representativos para todas las entradas.
## analisis teorico
- usa pseudocodigo
- no importa el entorno
- basado en la funcion T(n) que permite representar el tiempo de ejecucion en fucnion del tamaño de la entrada (unidad de tiempo inventada, generalmente nanosegundos)
- considera todas las posibles entradas.

operaciones primitivas damos c=1 (nanosegundo) de coste temporal, ej:
- x=2
- indexar un elemento vector[i]
- etc.
ejemplo:

```
def swap(a,b):
    t=a c=1
    a=b c=1
    b=t c=1
```
T(n)=1+1+1=3.

necesita 3 nanosegundo.

si tenemos un bucle tenemos que contar las instrucciones del bucle y multiplicarlo por el numero de iteraciones 
Tloop(n)=T(B)*nº iteraciones
```
r=0             c=1
for i in range(1,n+1):
    r+=i        c=1
return r        c=1
```
T(n)=n+2 ns

bucles anidados:
```
for i=1 to n:                   |
    for j=1 to n:               |todo esto *n
        print(i*j)     c=1*n    |

```
T(n)=n^2

sin embargo:
```
while current:
    for i in range(n):
        current=current.next
    insertAt("asdf",i)
```
esto tiene complejidad T(n)=n ya que el while solo evalua.

cuando hay if:
```
if o=0:
    x=0
else:
    for i in range(10):
        x+=1
```
tiene complejidad T(n)=max(T1(s), T2(n))=max(1,n+1)=n+1

cuando las complejidades es muy proxima se comparan los valores cuando el tamaño tiende a infinito(en polinomios ignoramos los grados menores y los coeficientes)
```
T(n)=3n^3               ---> n^3
T(n)=3n^3+2n^2          ---> n^3
```
hay    que buscar a que grupo se asemeja:
```
1<log n < n < nlog n < n^2  < n^3 < ... < 2^n < n!
```
notacion:
```
O(1)
O(logn)
O(n)
O(nlogn)
O(n^2)
O(n^c)
O(c^n)
O(n!)
```

