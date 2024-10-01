Describiendo el camino: el Álgebra Relacional 
- Es un lenguaje formal de manipulación para diseñar [[3 Dinamica del SQL, DML|consultas]]. 
- Fue definida por Codd (1971) para los modelos relacionales. Inicialmente definió 5 operaciones básicas y 3 derivadas.
- Su estudio sirve para ilustrar las operaciones básicas requeridas en cualquier LMD y como estándar para comparar lenguajes relacionales (mide su potencia operacional) 
- Los operandos en cualquier operación algebraica-relacional son relaciones, y el resultado es siempre una relación. 
- Los operadores pueden clasRificarse siguiendo varios criterios: primitivos y derivados; unarios, binarios, y binarios compatibles; básicos, extendidos, y otros operadores

# Operadores Unarios (I)

## Selección
Escogemos las tuplas que cumplan una condición
Notación: $\operatorname{\sigma}_{\text{predicado}}(Relacion)$
![[Pasted image 20230312154618.png]]
## Proyección
Subconjunto del esquema relación
Notación:  $\operatorname{\pi}_{\text{atr1,atr2,...}}(Relacion)$
![[Pasted image 20230312154806.png]]

## Renombrado
Asigna el resultado de una expresión a un símbolo (relación temporal, cuya existencia está limitada a la duración de la [[3 Dinamica del SQL, DML|consulta]])*.
Notación: $\operatorname{\rho}_{\text{simbolo}}(Expresion)$ o tambien $S \equiv Expresion$
![[Pasted image 20230312155135.png]]
1. A:= Seleccion de los libros cuyo autor es Dumas 
2. Q:= columna titulo (proyeccion) de A
ó
1. A $\equiv$ Seleccion de los libros cuyo autor es Dumas
2. Q $\equiv$ Columa titulo de A

# Operadores Binarios Compatibles
Para poder aplicar los operadores de conjuntos Unión, Intersección y Diferencia, las relaciones deben ser compatibles.

Dos relaciones son compatibles si tienen el mismo número de atributos y el atributo i-ésimo del primer operando está definido sobre el mismo dominio que el atributo i-ésimo del segundo operando.

En general, el esquema de relación de dos relaciones no coincide pero puede aplicarse la operación de proyección para igualar estos esquemas
![[Pasted image 20230312155541.png]]
## Union
Todas las tuplas de ambas relaciones (compatibles), eliminándose todas las tuplas repetidas.
![[Pasted image 20230312155629.png]]

# Combinaciones
## Intersección
Todas las tuplas que estén en ambas (compatibles)
![[Pasted image 20230312155721.png]]

## Diferencia
tuplas que aparecen en la primera y no en la otra (compatibles)
![[Pasted image 20230312155743.png]]

## Producto cartesiano
Tuplas de ambas en todas las combinaciones
![[Pasted image 20230312155821.png]]

## Combinación (simple join or inner join):
Tuplas del producto cartesiano que cumplen una expresión condicional genérica. La condición lleva operadores de comparación (=, >, <...)
![[Pasted image 20230312155938.png]]

## Combinación Natural (equijoin):
Caso particular del operador combinación donde la comparación es de igualdad.
Notación: * o |X| (algo asi)
![[Pasted image 20230312160253.png]]

## Operadores Primarios y Operadores Derivados 
- Algunos operadores del álgebra relacional pueden ser sustituidos por una secuencia de otras operaciones algebraicas. 
- Aquellos se dirá que son operadores derivados. 
- Por otro lado, operadores primitivos son los que no pueden ser obtenidos por ninguna secuencia de otros operadores primitivos![[Pasted image 20230312160420.png]]

# Otros
## Agrupación
Formación de grupos según un conjunto de atributos al cual se le aplica una función de agregación.
Notacion:
- $\operatorname{\pi}_{\text{proyeccion}},\operatorname{\sigma}_{\text{seleccion}}, Ģ_{\text{criterio}}(relacion)$
-  también se admite GROUP BY en vez de Ģ
![[Pasted image 20230312160735.png]]
Funciones de agrupación: Count(), Sum(), Avg(), Min(), Max()

## División
El cociente lo forman todas las tuplas que concatenadas con cada tupla del divisor estén contenidas en el dividendo.
$a \div b \equiv {\pi}_{\text{esq(A)-esq(B)}}A-{\pi}_{\text{esq(A)-esq(B)}}(({\pi}_{\text{esq(A)-esq(B)}}AxB)-A)$
![[Pasted image 20230312161205.png]]
## Semi-Combinacion (right or left semijoin)
igual que cualquier combinación, pero sólo se toman las columnas del operando izquierdo (|\*) o derecho (\*|).
![[Pasted image 20230312161516.png]]
## Anti-Combinacion (antijoin)
igual que la semi combinación, pero las tuplas que se incluyen son las que no cumplen la condición definida.![[Pasted image 20230312161645.png]]

## Combinacion externa (Outer join)
Extensión de la combinación, que incluye las tuplas que no encajan de la relación izquierda/derecha/ambas. Las columnas que no aplican, adoptan el valor nulo (NULL ó $\sigma$ ).
![[Pasted image 20230312161843.png]]

## Conjuntos ordenados
onjunto ordenado (lista) es el resultado de aplicar un orden ($ORDER.BY_\text{orden}$ ó ┬orden) sobre una relación. Si orden omite la especificación de orden (sólo explicita atributos) se sobreentiende el orden ≤ sobre números y el orden lexicográfico sobre caracteres.

Si se opera una lista ordenada se obtiene una relación (sin orden).

Sobre una lista ordenada se pueden aplicar funciones de selección y funciones analíticas de agregación (first, last, rank(value), ...)
![[Pasted image 20230312162459.png]]

## Asignación
se utiliza para definir operaciones de actualización sobre la base de datos. La notación del operador es $\leftarrow$
![[Pasted image 20230312162603.png]]
