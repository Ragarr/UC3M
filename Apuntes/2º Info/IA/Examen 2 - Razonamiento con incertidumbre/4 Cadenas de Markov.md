# Procesos Estocásticos
Un proceso estocástico es un conjunto de variables aleatorias que depende de un parámetro o de un argumento, en nuestro caso dependen del tiempo.
Un proceso estocástico es una familia de variables aleatorias definida sobre un espacio de probabilidad.
Tendremos que X es una función de dos argumentos. Fijando $\omega=\omega_{0}$, obtenemos una función determinista (no aleatoria):
$\{X_{t}:\Omega\to \mathcal{R}, t \in T  \}$
$\omega\to W_{t}(\omega)=X(\omega,t)$
Asimismo fijando  $t=t_{0}$ obtenemos una de las variables aleatorias de la familia

El espacio de estados S de un proceso estocástico es el conjunto de todos los posibles valores que puede tomar dicho proceso.
$S=\{ X_{t}(\omega)\mid t \in T \land \omega \in \Omega \}$
## Ejemplo
Lanzamos una moneda al aire 6 veces. El jugador gana 1 € cada vez que sale cara (C), y pierde 1 € cada vez que sale cruz (F).
- $X_{i}$ = estado de cuentas del jugador después de la i-ésima jugada.
- La familia de variables aleatorias $\{ X_{1},X_{2},\dots,X_{6} \}$ constituye un proceso estocástico
- $\Omega = \{ CCCCCC, CCCCCF, \dots \}$
- $card(\Omega)=2^6=64$
- $P(\omega)=\frac{1}{64} \forall \omega \in \Omega$
- T= {1,2,3,4,5,6}
- S={-6,-5,…,-1,0,1,…,5,6}
- $X_{1}(\Omega)=\{ -1,1 \}$
- $X_{2}(\Omega)=\{ -2,0,2 \}$
- $X_{3}(\Omega)=\{ -3,-1,1 ,3 \}$
Podemos hallar la probabilidad de que el proceso tome uno de estos valores:
la probabilidad de todos los caminos que te llevan a ese estado
- $P[X_{3}(\Omega)=1]=P[CFC]+P[CCF]+P[FFC] = 3 \cdot \frac{1}{2} \cdot \frac{1}{2}\cdot \frac{1}{2}=\frac{3}{8}$

## Tipos de procesos estocásticos
- Cadena: Ejemplo anterior 
- Sucesión de variables aleatorias continuas: cantidad de lluvia caída cada mes 
- Proceso puntual: Número de clientes esperando en la cola de un supermercado 
- Proceso continuo: velocidad del viento
# Cadena de Markov
Una cadena de Markov es un tipo especial de proceso estocástico discreto en el que la probabilidad de que ocurra un evento depende solamente del evento inmediatamente anterior.
Las cadenas de Markov son espacios de estados S discretos y conjuntos de instantes de tiempo T también discretos, T=$\{ t_{0}, t_{1} , t_{2} ,\dots\}$
Sólo trabajaremos con CM homogéneas en el tiempo, que son aquellas en las que donde $q_{ij}$ se llama probabilidad de transición en una etapa desde el estado i hasta el estado j.
 $q_{ij}$ son las probabilidades de transitar del estado i al estado j.
Los $q_{ij}$ se agrupan en la denominada matriz de transición de la CM:

$$Q=\begin{bmatrix}
q_{00} & q_{01} & q_{02} & \dots \\
q_{10} & q_{11} & q_{12} & \dots \\
q_{20} & q_{21} & q_{22} & \dots \\
\vdots & \vdots & \vdots & \ddots \\
q_{n0} & q_{n1} & q_{n2} & \dots
\end{bmatrix}
=(q_{ij})_{i,j\in S}
$$
Propiedad: las filas han de sumar 1.

## Diagrama de transición de estados
El diagrama de transición de estados (DTE) de una CM es un grafo dirigido cuyos nodos son los estados de la CM y cuyos arcos se etiquetan con la probabilidad de transición entre los estados que unen. Si dicha probabilidad es nula, no se pone arco.
![[Pasted image 20230416182008.png]]
## Ejemplo
Sea una línea telefónica de estados ocupado=1 y desocupado=0. Si en el instante t está ocupada, en el instante t+1 estará ocupada con probabilidad 0,7 y desocupada con probabilidad 0,3. Si en el instante t está desocupada, en el t+1 estará ocupada con probabilidad 0,1 y desocupada con probabilidad 0,9.
$$Q=\begin{bmatrix}
0,9 & 0,1 \\
0,3 & 0,7
\end{bmatrix}$$
![[Pasted image 20230416182039.png]]
# Modelos ocultos de Markov
En el Modelo de Markov, el estado en el que nos encontramos es conocido. Pero cómo podemos manejar una situación en la que recibimos una observación del sistema pero no sabemos en qué estado está el sistema y tenemos que inferirlo.
Si cada estado de un modelo de Markov emite una observación con una cierta incertidumbre ¿Podemos saber en qué estado se encuentra el sistema al recibir la observación?
## Ejemplo
Un alumno estudia día tras día en su estudio sin ventanas, y quiere saber si llueve o no. Hay una sola persona a la que ve entrar cada día, su compañero de piso, y puede ver si lleva o no un paraguas. Variables aleatorias:  L: Llueve. (Estado oculto)  P: La persona lleva un paraguas. (Observación) Para representarlo, podemos construir la siguiente Red Bayesiana:
![[Pasted image 20230416184424.png]]
## Inferencia en HMM
La inferencia en un Modelo Oculto de Markov (HMM) se refiere a la capacidad de hacer predicciones y estimaciones basadas en la información disponible. 
Esto incluye el **filtrado** o **monitoreo**, que es la distribución de probabilidad del estado actual dada la evidencia previa; la predicción de estados futuros dada la evidencia previa; el suavizado para estimar los estados pasados dada la evidencia actual; y la explicación más probable, que es la secuencia de estados que maximiza una secuencia de observables. 
También se puede realizar la estimación de los parámetros del HMM para minimizar una secuencia de observables de una secuencia de estados.

En el ejemplo anterior:
Si trajo paraguas los dos primeros días seguidos, ¿cuál es la probabilidad de que el segundo esté lloviendo?
| $Llueve_{t-1}$ | $P\left( \frac{Llueve_{t}}{Llueve_{t-1}} \right)$ |
| -------------- | ------------------------------------------------- |
| V              | 0,7                                               |
| F              | 0,3                                                  |

| $Llueve_{t}$ | $P\left( \frac{Paraguas}{Llueve_{t}} \right)$ |
| -------------- | ------------------------------------------------- |
| V              | 0,9                                               |
| F              | 0,2                                                  |
Filtrado:
Si trajo paraguas los dos primeros días seguidos, ¿cuál es la probabilidad de que el segundo esté lloviendo? Siendo la probabilidad a priori de lluvia el 50%.
- $P(L0/P0)=0,9*0.5*1/P(P(P0)=0.82$
- $P(¬L0/P0) =0.18$
- $P(L1/P0,P1)= \frac{0.9*(0.7*1.82*0.3*0.18)*1}{P(P0,P1)}= 0.88$
## Resumen de HMM
En lugar de observar los estados de la cadena de Markov, observamos otros elementos, bajo ciertas probabilidades:
### Elementos de una cadena de Markov oculta.
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
### Tres problemas
Llamemos λ al conjunto de parámetros del modelo de Markov oculto, y a una realización de la cadena de Markov oculta.
- Problema 1. Calcular P ( O / λ )
- Problema 2. Encontrar la secuencia de estados que mejor se corresponda con la secuencia observada O, bajo el modelo λ .
- Problema 3. Estimar los parámetros del modelo. Lo haremos buscando λ que haga máxima P ( O / λ ) .

## Primer Problema
Si supiéramos cuál ha sido la sucesión de estados, entonces la probabilidad de una sucesión de estados es la multiplicación de las probabilidades de cada estado (partiendo del inicial hasta llegar al deseado).
![[Pasted image 20230416190424.png]]
### Procedimiento atras hacia alante (induccion)
Definimos las funciones adelante así:
![[Pasted image 20230416190457.png]]
Las funciones adelante se pueden calcular por inducción así:
1. Paso inicial ![[Pasted image 20230416190520.png]]
2. Inducción ![[Pasted image 20230416190534.png]]
3. Paso final ![[Pasted image 20230416190545.png]]

## Segundo problema ALGORITMO DE VITERBI
Buscamos la cadena de estados que mejor se corresponda con la secuencia observada (problema 2). Formalizamos esto en el objetivo siguiente:
.....



## Resolver un ejercicio de HMM
Para resolver un HMM hay que realizar los siguientes pasos: 
1. Modelar el HMM: un HMM se define mediante el estado oculto del problema (𝑂𝑇) y su observación (𝐴𝑇). 
2. Modelar la representación de la red bayesiana: dibujar la red bayesiana del problema. 
3. Definir las distribuciones de probabilidad que afectan al problema y colocarlas en la red bayesiana. 
4. Definir la tarea de inferencia a resolver
