Una red bayesiana es una estructura de datos para la representación de conocimiento incierto. 
- Representa la dependencia entre variables y especifica de manera concisa la distribución de probabilidad conjunta.
- Es una representación gráfica en la que cada nodo de la red representa una variable aleatoria.  Un arco del nodo X al nodo Y significa que la variable X tiene una influencia sobre Y.
- Cada nodo X tiene una tabla de probabilidad condicional que cuantifica el efecto que los padres de X tienen sobre X. 
- Es un grafo dirigido acíclico (GDA).
# Probabilidad condicional
![[Pasted image 20230412191357.png]]
| x   | $P(Y \vert X)$ | $P(\neg Y \vert X)$ | 
| --- | -------------- | ------------------- |
| V   | 0.7            | 0.3                 |
| f   | 0.01           | 0.99                |
-  $P(Y \vert X) + P(\neg Y \vert X) = 1$ 
- $P(Y \vert \neg X) + P(\neg Y \vert \neg X) = 1$ 
- $P(Y)= P(Y \vert X)P(X) + P(Y \vert X)P(\neg X)$
- $P(\neg Y)= P(\neg Y \vert X)P(X) + P(\neg Y \vert \neg X)P(\neg X)$
# Causalidad y correlación
La causalidad se refiere a una relación directa entre una causa y su efecto, mientras que la correlación se refiere a una relación estadística entre dos variables que pueden estar relacionadas, pero no necesariamente por una causa y efecto directos. La correlación no implica causalidad ya que puede haber otros factores en juego.
# Independencia condicional
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
1. Independencia a priori de los nodos que no tienen ningún antepasado común
2. Independencia condicional de los nodos hermanos con respecto a su padre
3. Independencia condicional entre un nodo y los antepasados de sus padres
4. Dependencias condicionales por descendientes comunes instanciados
## Grafos conexos
Entre cualquier par de nodos hay al menos un camino (una ruta no dirigida).
- Grafo simplemente conexo o **poliárbol**: entre cualquier par de nodos hay un único camino.
- Grafo múltiplemente conexo: contiene bucles o ciclos
- Árbol: poliárbol en el que cada nodo tiene un solo padre, menos el nodo raíz que no tiene

## D-Separación
Un conjunto de nodos E d-separa dos conjuntos de nodos X y Y si cualquier trayectoria no-dirigida de un nodo en X a un nodo en Y es bloqueada en función de E.
![[Pasted image 20230412194003.png]]
Si la ruta no-dirigida (independiente de la dirección de las flechas) de un nodo X a un nodo Y está d-separada por E, entonces X y Y son condicionalmente independientes dada E
Ejemplo: Encendido separa batería de arranque, por lo tanto, arranque y batería son condicionalmente independientes de Encendido.

Si A y B son d-separadas, entonces cambios en la probabilidad de A no tienen efecto en la probabilidad de B
Si A y B son d-separadas dada la evidencia e, entonces A y B son condicionalmente independientes dado e
Ejemplo:
![[Pasted image 20230412194303.png]]
F está d-separada del resto de las variables no instanciadas A, E y G

Una RB es representación correcta del dominio si cada nodo es cond. Independiente respecto de antepasados de sus padres

# Construcción de Redes Bayesianas
1. Escoger conjunto de variables
2. Definir un orden parcial para el conjunto de variables; primero los nodos causales y luego los nodos efecto
3. Mientras queden variables
	1. Escoger siguiente variable Xi y añadir nodo a la RB
	2. Asigne Padres($X_{i}$) a un conjunto mínimo de nodos presente en la red, de manera que sea satisfecha la propiedad de independencia condicional
	3. Elaborar la tabla de probabilidad condicional de $X_{i}$
Este método garantiza la obtención de redes acíclicas Evita la redundancia en la definición de probabilidades Evita que se violen los axiomas de probabilidad

# Inferencia en RB
- **Inferencia** o **propagación de probabilidades**: efectos de la evidencia propagados por la red para saber probabilidades a posteriori
- **Propagación**: dar valores a ciertas variables (evidencia), y obtener la probabilidad posterior de las demás variables
## Tipos de inferencia
- **Modelo diagnóstico:** efectos (síntomas) → causas (diagnóstico)
- **Modelo causal**: Causas → efecto
- **Inferencias intercausales**: entre las causas de un efecto común
- **Inferencias mixtas**: combinación de las anteriores

# Tipos de árboles
![[Pasted image 20230412195013.png]]
