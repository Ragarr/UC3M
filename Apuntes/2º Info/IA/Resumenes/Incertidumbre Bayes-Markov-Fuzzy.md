# Incertidumbre
En un sistema con incertidumbre, las conclusiones ocurren con cierta probabilidad, no determinista como hasta ahora.
La incertidumbre puede venir de los hechos, si son **incompletos, inciertos o erroneos**.
## Palabras relacionadas con la incertidumbre (dicc. de términos)
- **Imprecisión**
	se refiere a información o enunciados que admiten más de una interpretación posible. Por ejemplo, decir que un sistema tiene una temperatura alta puede interpretarse de muchas maneras.
- **Vaguedad** 
	se refiere a conceptos cuya frontera del conjunto de valores que especifica no está bien definida, como en el ejemplo “Juan es joven”.
- **Incompletitud** 
	se refiere a información que no permite inferir la verdad o falsedad de un enunciado. Por ejemplo, si no sé si llevo paraguas, no sé si me voy a mojar aunque llueva.
- **Incertidumbre** 
	se refiere a enunciados cuya validez (verdadero o falso) no puede determinarse con seguridad.

# Razonamiento Bayesiano
## Teorema de Bayes:
$P(A | B) = \frac{P(B | A)\cdot P(A)}{P(B)}$
Donde:
-   $P(A | B)$ es la probabilidad de que ocurra el evento A habiendo ocurrido el evento B.
-   $P(B |A)$ es la probabilidad de que ocurra el evento B habiendo ocurrido el evento A.
-   $P(A)$ es la probabilidad de que ocurra el evento A.
-   $P(B)$ es la probabilidad de que ocurra el evento B.
## Regla de Bayes
- $P(A,B)=P(A|B)·P(B) =P(B|A)·P(A)$
- $P(A|B)·P(B)=P(B|A)·P(A)$
### Regla de LaPlace
$$P(A)=\frac{\text{n casos favorables a A}}{\text{n casos posibles}}=\frac{n_{A}}{n}$$
### Conjuntos
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
### Ejemplo sucesos
**Lanzar un dado y observar el número resultante:**
- Suceso elemental: Sale un 2 `{2}`
- Suceso compuesto: Sale un número par `{2,4,6}`
**Encender un foco hasta que se funda. Medir el tiempo:**
  - Suceso: el foco dura más de 100 horas `{t | t > 100}

### Variables aleatorias
Si `M` es una variable aleatoria que representa el resultado de lanzar una moneda con valores posibles cara y cruz, podemos hacer proposiciones como `M = cara` y `M = cruz`, y podemos hablar de probabilidades como `P(M = cara)` y `P(M = cruz)`, que representan la probabilidad de obtener cara y cruz respectivamente.

### Probabilidad.
- **Probabilidad conjunta**: La probabilidad conjunta es una medida estadística que indica la probabilidad de que dos sucesos ocurran al mismo tiempo. (interseccion de que las variables aleatorias tomen x valor)
	- $P(x_{i},y_{j},z_{k})\equiv P(X=x_{i}\cap Y=y_{i}\cap Z=z_{i})$
- **Probabilidad marginal**: La probabilidad marginal es la probabilidad de un subconjunto de valores del conjunto sin necesidad de conocer los valores de las otras variables.
	- $P(x_{i})=\sum_{\forall j,k}P(x_{i},y_{j}.z_{k}))$
**Ejemplo**:
Probabilidades Conjuntas:
|              | Dolor dental (D) | $\neg$Dolor Dental |
| ------------ | ---------------- | ------------------ |
| Caries (C)   | 0.04             | 0.06               |
| $\neg$Caries | 0.01             | 0.89               |
Probabilidades Marginales:
- $P(C)=P(C,D)+P(C,\neg D)=0.06+0.04=0.1$
- $P(D)=P(C,D)+P(\neg C,D)=0.04+0.01=0.05$
- Nota: son la suma de fila o columna correspondiente de las probabilidades conjuntas
#### Probabilidad condicionada
$P(A|B)=\frac{P(A\cap B)}{P(B)}$
Si A y B son mutuamente excluyentes: 
- P(A,B) =0 
- P(A | B) = 0 = P(B | A).
Si $A\subset B$ entonces P(B | A) = 1

# Redes bayesianas
## Causalidad y correlación
La causalidad se refiere a una relación directa entre una causa y su efecto, mientras que la correlación se refiere a una relación estadística entre dos variables que pueden estar relacionadas, pero no necesariamente por una causa y efecto directos. La correlación no implica causalidad ya que puede haber otros factores en juego.
## Independencia condicional
La independencia condicional describe cómo dos eventos pueden ser independientes entre sí cuando se tiene en cuenta un tercer evento. Esto significa que la ocurrencia de un evento no afecta la probabilidad del otro evento dado que el tercer evento ha ocurrido. Ejemplo:
```
Imagina que tienes dos eventos: 
	A) Llueve afuera
	B) El césped está mojado. 
En general, estos dos eventos están relacionados: 
	> si llueve afuera (A), es más probable que el césped esté mojado(B). 
Sin embargo, ahora considera un tercer evento: 
	C) El rociador de agua está encendido. 
Si sabes que el rociador de agua está encendido ©, entonces la probabilidad de que el césped esté mojado (B) no depende de si está lloviendo afuera o no (A). En otras palabras, dado que el rociador de agua está encendido ©, los eventos “llueve afuera” (A) y “el césped está mojado” (B) son condicionalmente independientes.
```
Propiedades:
1. **Independencia** a priori de los nodos que no tienen **ningún antepasado común**
2. **Independencia condicional** de los nodos **hermanos con respecto a su padre**
3. **Independencia condicional** entre un nodo y los **antepasados de sus padres**
4. **Dependencias condicionales** por **descendientes comunes instanciados**
## Como pintar y leer el arbolito
![[Pasted image 20230412191357.png]]
### Ejemplo
![[Pasted image 20230523132139.png]]
![[Pasted image 20230523132430.png]]
![[Pasted image 20230523132442.png]]
![[Pasted image 20230523132458.png]]

## Grafos conexos
Entre cualquier par de nodos hay al menos un camino (una ruta no dirigida).
- Grafo simplemente conexo o **poliárbol**: entre cualquier par de nodos hay un único camino.
- **Grafo múltiplemente conexo**: contiene bucles o ciclos
- **Árbol**: poliárbol en el que cada nodo tiene un solo padre, menos el nodo raíz que no tiene
### Tipos de árboles
![[Pasted image 20230412195013.png]]

### Ejemplo poliarbol
![[Pasted image 20230412194003.png]]

### D-separación
Un conjunto de nodos E D-separa dos conjuntos de nodos X y Y si cualquier trayectoria no-dirigida de un nodo en X a un nodo en Y es bloqueada en función de E.

**En el ejemplo anterior**: Encendido separa batería de arranque, por lo tanto, arranque y batería son condicionalmente independientes de Encendido.

## Construir una red de Bayes
1. Escoger conjunto de variables
2. Definir un orden parcial para el conjunto de variables; primero los nodos causales y luego los nodos efecto
3. Mientras queden variables
	1. Escoger siguiente variable Xi y añadir nodo a la RB
	2. Asigne Padres($X_{i}$) a un conjunto mínimo de nodos presente en la red, de manera que sea satisfecha la propiedad de independencia condicional
	3. Elaborar la tabla de probabilidad condicional de $X_{i}$
Este método garantiza la obtención de redes acíclicas Evita la redundancia en la definición de probabilidades Evita que se violen los axiomas de probabilidad

## Inferencia en RB
- **Inferencia** o **propagación de probabilidades**: efectos de la evidencia propagados por la red para saber probabilidades a posteriori
- **Propagación**: dar valores a ciertas variables (evidencia), y obtener la probabilidad posterior de las demás variables

### Tipos de inferencia
- **Modelo diagnóstico:** efectos (síntomas) → causas (diagnóstico)
- **Modelo causal**: Causas → efecto
- **Inferencias intercausales**: entre las causas de un efecto común
- **Inferencias mixtas**: combinación de las anteriores

# Márkov
En lugar de observar los estados de la cadena de Markov, observamos otros elementos, bajo ciertas probabilidades:
## Elementos de una cadena de Markov oculta.
- Espacio de estados: $E=\{ E_{1},E_{2},\dots,E_{s} \}$
- Matriz de transicion: $$Q=\begin{bmatrix}
q_{00} & q_{01} & q_{02} & \dots \\
q_{10} & q_{11} & q_{12} & \dots \\
q_{20} & q_{21} & q_{22} & \dots \\
\vdots & \vdots & \vdots & \ddots \\
q_{n0} & q_{n1} & q_{n2} & \dots
\end{bmatrix}
=(q_{ij})_{i,j\in S}
$$
- Alfabeto de símbolos observables: $A=\{ a_{1},\dots,a_{m} \}$
- Probabilidades de emision: $B=b_{i}(a)$
- Distribución inicial: $p^{(0)}=\{ p^{(0)}_{1}, p^{(0)}_{2},\dots,p^{(0)}_{s} \}$

## Tres problemas
Llamemos λ al conjunto de parámetros del modelo de Markov oculto, y a una realización de la cadena de Markov oculta.
- Problema 1. Calcular P ( O / λ )
- Problema 2. Encontrar la secuencia de estados que mejor se corresponda con la secuencia observada O, bajo el modelo λ .
- Problema 3. Estimar los parámetros del modelo. Lo haremos buscando λ que haga máxima P ( O / λ ) .

### Primer Problema
Si supiéramos cuál ha sido la sucesión de estados, entonces la probabilidad de una sucesión de estados es la multiplicación de las probabilidades de cada estado (partiendo del inicial hasta llegar al deseado).
### Segundo problema
Buscamos la cadena de estados que mejor se corresponda con la secuencia observada
### Tercer problema
Estimación de los parámetros del modelo, aquellos que minimizan una secuencia de observables de una secuencia de estado.

## Resolver un ejercicio de HMM
Para resolver un HMM hay que realizar los siguientes pasos: 
1. Modelar el HMM: un HMM se define mediante el estado oculto del problema (𝑂𝑇) y su observación (𝐴𝑇). 
2. Modelar la representación de la red bayesiana: dibujar la red bayesiana del problema. 
3. Definir las distribuciones de probabilidad que afectan al problema y colocarlas en la red bayesiana. 
4. Definir la tarea de inferencia a resolver

# Lógica Fuzzy
A diferencia de la lógica clásica, que utiliza valores binarios (verdadero o falso) para representar el estado de una variable, la **lógica difusa permite la representación** de la información mediante **valores que van de 0 a 1**, lo que refleja la posibilidad de que una afirmación sea **parcialmente verdadera** o **parcialmente falsa**.

En la lógica difusa, los términos lingüísticos y los conceptos vagos se pueden representar de manera más realista. Por ejemplo, en lugar de decir que una persona es alta o baja, se pueden utilizar términos como "alta", "media" o "baja" para describir su estatura. Estos términos se asignan a conjuntos difusos, que son intervalos de valores dentro de un dominio determinado. La membresía de un valor a un conjunto difuso se determina mediante una función de pertenencia, que asigna un grado de pertenencia entre 0 y 1.

## Conjuntos borrosos
Un conjunto borroso representa el grado de verdad o posibilidad de que un concepto sea verdadero.
### Ejemplo 
**Joven:**
![[Pasted image 20230523155349.png]]
**Mediana edad**:
![[Pasted image 20230523155513.png]]

## Operadores borrosos
- Unión $A\cup B$
	- $\mu_{A\cup B}(x)=\lor(\mu_{A}(x),\mu_{B}(x)\forall x \in X)$
	- $\lor$ es el operador 'O'
- Intersección $A\cap B$
	- $\mu_{A\cap B}(x)=\land(\mu_{A}(x),\mu_{B}(x)\forall x \in X)$
	- $\land$ es el operador 'Y'
**Ejemplo Union**
![[Pasted image 20230523160019.png]]
**Ejemplo interesccion**
![[Pasted image 20230523160103.png]]

## Inferencia en FUZZY

### Con entradas numericas.
Se aplican las reglas con maximos (si la regla tiene un or) o minimos si la regla tiene un and, ejemplo
![[Pasted image 20230523164737.png]]
el resultado es el maximo de la pertenencia a delicious y excellent, que da a que se corte la pertnenencia a generous en el mismo punto de pertenencia a delicious.

**Cuando varias reglas aplican a la vez**
![[Pasted image 20230523164952.png]]
hay que tener en cuenta que service good y service poor se superponen por lo que pertenece en parte a ambos, asi que ambas reglas producen una salida, luego se hace la agregacion de todas las salidas y calculas su centro de gravedad, mediante integrales:
![[Pasted image 20230523165318.png]]
O a ojo xd.

El punto donde se sitúe el centro de gravedad es el resultado esperado.
En el ejemplo, el centro este en 16.7 por lo que la propina esperada es del 16.7%.
![[Pasted image 20230523165417.png]]

### Con entradas lingüísticas

Se hace más o menos igual, con el porcentaje de pertenencia a cada conjunto
y valor de pertenencia a cada conjunto final es el resultado.
