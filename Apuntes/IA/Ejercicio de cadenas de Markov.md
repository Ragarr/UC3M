# Cadena oculta de [[Razonamiento probabilistico en el tiempo#Cadenas de Markov|markov]] p29
Queremos construir un sistema para reconocimiento automático del lenguaje. Concretamente, queremos comprender las palabras que corresponden a ciertas señales acústicas: cada letra corresponde en teoría a una de estas señales. Para simplificar consideraremos un lenguaje en el que hay sólo tres letras (a, r, t), y también las palabras sólo pueden tener tres letras de longitud. El proceso se puede modelar con un HMM con una sola variable oculta que representa la letra, y las observaciones la señal acústica, en forma de un fonema extraído de la señal. • Los estados 𝐿𝑡 representan la letra {a, r , t} • Las observaciones 𝐹𝑡 representan el fonema {a, r , t}
![[Pasted image 20230314151710.png]]
![[Ejercicio cadena oculta markov.excalidraw]]
$P_{0}(0.3,0.3,0.4)$
$P_{1}(0.55,0.21,0.24)$
$P_{1}(a)=P_{0}(a)*P(a/a)+ P_{0}(r)*P(a/r)+P_{0}(t)*P(a/t)=0*0.3+0.3*0.5+0.4*1=0.55$ 

Se conocen las probabilidades a priori de transicion condicional![[Pasted image 20230314153145.png]]

Se pide:
1. ¿Cuál es la probabilidad de que la letra inicial sea a cuando el sistemaescucha el fonema a? $𝑃(𝐿_{0} = 𝑎/F_{0} = 𝑎)$
2. ¿Cuál es la probabilidad de escuchar el fonema a en primeraposición? $𝑃(𝐹_{0} = 𝑎)$
3. ¿Cómo computaría la probabilidad de que la palabra emitida sea“art”?

## 1 ¿Cuál es la probabilidad de que la letra inicial sea a cuando el sistemaescucha el fonema a? 
Es la probabilidad de que el sistema este en **a** cuando se escucha **a**, es la probabilidad de estar en a -> $P_{0}(a)$ multiplicado por la probabilidad de que estando en a escuches una a -> $P(F_{t}=a/L_{t})$.
Es decir $𝑃(𝐿_{0} = 𝑎/F_{0} = 𝑎)=P({\text{estar en a habiendo escuchado a}})=P_{0}(a)*P_{0}(F_{t}=a/L_{t}=a)=0.3*0.9$ 

## 2. ¿Cuál es la probabilidad de escuchar el fonema a en primera posición? $𝑃(𝐹_{0} = 𝑎)$
$P(F_{t}=a/L_{t})=0.9$

## 3. ¿Cómo computaría la probabilidad de que la palabra emitida sea “art”?

# Ej 2 decision de markov p26
Para el tratamiento de un cierto tipo de tumor se pueden ejecutar tres acciones: cirugía, quimioterapia o radioterapia: 
- Si se somete a quimioterapia (**q**), la probabilidad de curación es 0.3, regenerándose en el resto de los casos. 
- Si se somete a radioterapia (**r**), la probabilidad de curación es 0.3, con probabilidad 0.6 se producirá metástasis y con 0.1 se regenerará. 
- Si se decide extirpar (**s**), la probabilidad de curación es 0.5. Con probabilidad 0.4 el tumor se regenerará y con probabilidad 0.1 se producirá metástasis. 
- Para tratar la metástasis se puede utilizar radioterapia o quimioterapia. La radioterapia la cura con probabilidad 0.3, y la quimioterapia con probabilidad 0.6.

El coste de la radioterapia es 6, el de la quimioterapia 10 y el de la cirugía 100. 
**Teniendo en cuenta que el objetivo es alcanzar la cura con el mejor coste posible:** 
- Modelar formalmente el MDP, no es necesario dibujar el diagrama de transiciones.
- Especificar las ecuaciones de Bellman que actualizan los valores de los estados.
- Calcular el valor esperado V(s) para cada estado. 
- Calcular la política óptima.

Se define mediante la tupla: < 𝑆, 𝐴, 𝑃, 𝐶 >
S: Estados:
A: Acciones:
P: Función de transición
C: Coste de ejecutar cada acción

Para el tratamiento de un cierto tipo de tumor se pueden ejecutar tres acciones: cirugía, quimioterapia o radioterapia: 
- Si se somete a quimioterapia (q), la probabilidad de curación es 0.3, regenerándose en el resto de los casos. 
- Si se somete a radioterapia (r), la probabilidad de curación es 0.3, con probabilidad 0.6 se producirá metástasis y con 0.1 se regenerará. 
- Si se decide extirpar (s), la probabilidad de curación es 0.5. Con probabilidad 0.4 el tumor se regenerará y con probabilidad 0.1 se producirá metástasis. 
- Para tratar la metástasis se puede utilizar radioterapia o quimioterapia. La radioterapia la cura con probabilidad 0.3, y la quimioterapia con probabilidad 0.6. 
El coste de la radioterapia es 6, el de la quimioterapia 10 y el de la cirugía 100.

## Estados:
- T: tumor
- M: metastasis
- C: curacion
## Acciones
- q: quimio
- r: radio
- s: extirpar
## Costes
- q: 10
- r: 6
- s: 100
##  Funcion transicion
![[Pasted image 20230314160801.png]]
## Diagrama
![[markov cancer.excalidraw]]
# Calcular V de cada nodo (Bellman)
V es una especie de heuristica donde V(nodo)=coste probabilistico del nodo

Las formulas de V son iterativas por que dependen del nodo del que parten.
$V_{i+1}(E_{orig})= min_{accion}\left[ \text{coste(accion)}+\sum_{E_{dest}}P_{accion}(e_{dest}|E_{orig})*V_{i}(E_{dest}) \right]$
El algoritmo se inicia con todas las $V_{0}=0$ 

$V(c)=0$ siempre
![[Pasted image 20230314161709.png]]
