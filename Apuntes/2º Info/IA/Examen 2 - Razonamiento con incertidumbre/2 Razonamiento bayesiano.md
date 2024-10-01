## Mates que hay detrás

### Teorema de Bayes:
$P(A | B) = \frac{P(B | A)\cdot P(A)}{P(B)}$
Donde:
-   $P(A | B)$ es la probabilidad de que ocurra el evento A habiendo ocurrido el evento B.
-   $P(B |A)$ es la probabilidad de que ocurra el evento B habiendo ocurrido el evento A.
-   $P(A)$ es la probabilidad de que ocurra el evento A.
-   $P(B)$ es la probabilidad de que ocurra el evento B.
### Regla de Bayes
- $P(A,B)=P(A|B)·P(B) =P(B|A)·P(A)$
- $P(A|B)·P(B)=P(B|A)·P(A)$
### Probabilidad como frecuencia
Sea $r$ el número de resultados obtenidos mediante un experimento y $r_{A}$ el número de veces que el resultado fue el suceso A. La frecuencia relativa $f_{A}$ de A se define como:
$f_{A}=\frac{r_{A}}{r}$
Y cumple:
- $0\leq f_{A}\leq 1$
- $f_{A}=0 \Leftrightarrow r_{A}=0; f_{A}=1 \Leftrightarrow r_{A} =1$
- si A y B son mutuamente excluyentes, entonces $f_{A\cup B}=f_{A}+f_{B}$
- $r\rightarrow\infty\Rightarrow f_{A}=P(A)$

### Regla de LAPLACE
$P(A)=\frac{\text{n casos favorables a A}}{\text{n casos posibles}}=\frac{n_{A}}{n}$

### Propiedades Útiles
- $P( \neg A)=1-P(A)$
- $P(A\cup B)=P(A)+P(B)- P(A\cap B)$
- $P(A\cup B\cup C)=P(A)+P(B) + P(C)- P(A\cap B)-P(A\cap C)-P(B\cap C)+P(A\cap B\cap C)$

## Definiciones
- **Suceso**: cualquier subconjunto del espacio muestral de un experimento aleatorio.
- **Sucesos elementales o atómicos**: conjunto de resultados posibles de un experimento que verifican:
	- Siempre ocurre alguno de ellos (conjunto exhaustivo, la unión de todos ellos es igual al espacio muestral).
	- Son mutuamente excluyentes (no hay ninguna intersección distinta de $\emptyset$).

	Esto significa que en un experimento aleatorio, siempre ocurrirá uno y solo uno de los sucesos elementales.

- **Suceso compuesto**: construido a partir de la unión de sucesos elementales.

## Ejemplo de sucesos
### Lanzar un dado y observar el número resultante:
- Suceso elemental: Sale un 2 `{2}`
- Suceso compuesto: Sale un número par `{2,4,6}`
### Lanzar una moneda tres veces, ver el total de caras:
- Suceso elemental: el número total de caras es 3 `{CCC}`
- Suceso compuesto: el número total de caras es 2 `{CC+, C+C, +CC}`
### Encender un foco hasta que se funda. Medir el tiempo:
  - Suceso: el foco dura más de 100 horas `{t | t > 100}`

## Variables Aleatorias
Una variable aleatoria es un concepto utilizado cuando tenemos un evento con un conjunto de resultados mutuamente excluyentes. Por ejemplo, si lanzamos una moneda, el resultado es cara o cruz. Si lanzamos un dado, hay seis resultados distintos.
Si `M` es una variable aleatoria que representa el resultado de lanzar una moneda con valores posibles cara y cruz, podemos hacer proposiciones como `M = cara` y `M = cruz`, y podemos hablar de probabilidades como `P(M = cara)` y `P(M = cruz)`, que representan la probabilidad de obtener cara y cruz respectivamente.

## Probabilidad conjunta y marginal
La distribución conjunta contiene todo lo que se necesita saber acerca de un conjunto de VA.  Dado el conjunto de VA $\{X,Y,Z\}$
- Probabilidad conjunta: $P(x_{i},y_{j},z_{k})\equiv P(X=x_{i}\cap Y=y_{i}\cap Z=z_{i})$
	- $\sum_{\forall i,j,k}P(x_{i},y_{j}.z_{k})=1$
- Probabilidad marginal:
	- $P(x_{i})=\sum_{\forall j,k}P(x_{i},y_{j}.z_{k}))$
	- $\sum_{\forall i}P(x_{i})=\sum_{\forall j}P(y_{j})=\sum_{\forall k}P(z_{k})=1$
Ejemplo:
Probabilidades Conjuntas:
|              | Dolor dental (D) | $\neg$Dolor Dental |
| ------------ | ---------------- | ------------------ |
| Caries (C)   | 0.04             | 0.06               |
| $\neg$Caries | 0.01             | 0.89               |
Probabilidades Marginales:
- $P(C)=P(C,D)+P(C,\neg D)=0.06+0.04=0.1$
- $P(D)=P(C,D)+P(\neg C,D)=0.04+0.01=0.05$
- Nota: son la suma de fila o columna correspondiente de las probabilidades conjuntas
## Probabilidad condicionada
Con $P(A | B)$ indicamos que el Espacio muestral de interés se ha “reducido” a aquellos resultados que definen la ocurrencia del suceso B.
Se llama probabilidad de A condicionada a B, representado P(A|B), a la probabilidad de que haya ocurrido A sabiendo que ha ocurrido B.
![[Pasted image 20230406145148.png]]
$P(A|B)=\frac{2}{5}=\frac{2/9}{5/9}=\frac{P(A\cap B)}{P(B)}$
Si A y B son mutuamente excluyentes: 
- P(A,B) =0 
- P(A | B) = 0 = P(B | A).
Si $A\subset B$ entonces P(B | A) = 1

## Lo de los arbolitos
- Los caminos representan intersecciones, y cada arco es una probabilidad condicional 
- Las bifurcaciones representan uniones disjuntas.
![[Pasted image 20230406150122.png]]
## Regla de bayes condicional
$P(A|B,C)=\frac{P(B|A,C)P(A|C)}{P(B|C)}$
