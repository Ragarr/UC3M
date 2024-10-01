# Introducción

## Neuronas artificiales
Son las unidades básicas de una red neuronal artificial. 
- **Reciben señales** de entrada provenientes **del mundo exterior o de otras neuronas**. 
- Las señales de entrada se transmiten **a través de conexiones** **que tienen un peso** asociado. 
- La neurona **procesa la información** recibida **mediante operaciones simples** 
- **Emite una señal de salida** como respuesta a las señales de entrada.
![[Pasted image 20230525105719.png]]
- La salida de la neurona es: $S=f(NET)$
- El umbral en una red neuronal es un valor que se utiliza para determinar si una neurona debe emitir una señal de salida o no, en función de la cantidad de activación que ha recibido. Cada neurona tiene su propio umbral
- $f$ es la función de activación$$NET=X_{1}w_{1}+X_{2}W_{2}+\dots+X_{n}w_{n}+U=U+\sum_{i=1}^nX_{i}w_{i}$$
## Funciones de activación
![[Pasted image 20230525110043.png]]
![[Pasted image 20230525110829.png]]
## Otros conceptos
- **Red de neuronas:**
	- Es un **conjunto de neuronas artificiales** **conectadas** entre sí **mediante** una serie de arcos llamados **conexiones**. Estas conexiones tienen números reales asociados, llamados **peso** de la conexión.
	- Las neuronas generalmente se distribuyen en capas de distintos niveles, con conexiones que unen las neuronas de distintas capas y/o neuronas de una misma capa.
- **Aprendizaje de la red**:
	- Es el proceso mediante el cual la red modifica sus respuestas ante las entradas para que **sus pesos se vayan adaptando** de manera paulatina al funcionamiento que se considera correcto. 
	- La modificación de los pesos se realiza basándose en un criterio establecido y que permite que la red “aprenda” a dar las respuestas adecuadas.
- **Aprendizaje supervisado:**
	- Para cada patrón (ejemplo) presentado a la red **existe una respuesta deseada**. 
	- La respuesta de la red se compara con su salida deseada y **en base a esa comparación se ajustan los pesos de la red**.
- **Aprendizaje no supervisado**: 
	- No se especifica a la red cuál es la respuesta correcta. 
	- A través de unas reglas de aprendizaje, **la red descubre las relaciones** presentes en los ejemplos
- **Patrones de entrenamiento:**
	- **Conjunto de** muestras o **ejemplos** para realizar el aprendizaje (determinación de pesos y umbrales).
- **Patrones de test o validación:** 
	- Conjunto de **ejemplos** utilizados para **evaluar la capacidad de generalización de la red**
- **Ciclo de aprendizaje:** 
	- Presentación del conjunto completo de patrones de entrenamiento una única vez.
	- Por lo tanto, si tienes un conjunto de 100 ejemplos de entrenamiento, durante un ciclo de aprendizaje, se presentarán esos 100 ejemplos a la red neuronal uno tras otro.

## Clasificación de redes de neuronas
- Basándonos en las conexiones:
	- Redes **feedforward** 
		- **Conexiones en un solo sentido** 
		- Perceptrón simple y multicapa, Redes de Base Radial 
	- **Redes recurrentes** 
		- **Conexiones en todas las direcciones **
	- Redes **parcialmente recurrentes** 
		- Unas pocas conexiones recurrentes 
		- Red de Jordan, Red de Elman

- Basándonos en el aprendizaje:
	- Redes supervisadas 
		- Redes feedforward 
		- Redes recurrentes 
	- Redes no supervisadas 
		- Kohonen, ART

# Redes de neuronas
## Perceptrón simple
- Es la forma mas simple de red de neuronas
- Tiene adaptación supervisada 
- Se encarga de tareas de clasificación lineal. 
	- Dado un conjunto de ejemplos o patrones, determinar el **hiperplano capaz de discriminar** los patrones en dos clases
**Ejemplo**

| Ejemplos                                     | Hiperplano                            | Grafica |
| -------------------------------------------- | ------------------------------------- | ------- |
| Puntos de $\mathbb{R}^n:(x_{1},\dots,x_{n})$ | $x_{1}w_{1}+\dots+x_{n}w_{n}+w_{0}=0$ |   ![[Pasted image 20230525112648.png]]      |


### Arquitectura:
![[Pasted image 20230525112826.png]]
- $y = f (x1·w1 + x2·w2 + \dots + xn ·wn +u)$
- $$f(x)=
\begin{equation}
  \left\{\begin{array}{@{}l@{}}
   1  \text{ si }   x>0 \\
-1   \text{ en otro caso}
  \end{array}\right.\,
\end{equation}$$
	- Si $x1·w1 +x2·w2+\dots+xn·wn+u>0 \implies y=1 \implies (x1 , \dots , xn ) \in C^{1}$
	- Si $x1·w1 +x2·w2+\dots+xn·wn+u\leq0 \implies y=-1 \implies(x1 , \dots , xn ) \in C^{1}$
- **Hiperplano**: $x_{1}w_{1}+\dots+x_{n}w_{n}+w_{0}=0$

### Proceso de aprendizaje
- Proceso iterativo supervisado: modificación de los parámetros de la red (pesos y umbral) hasta encontrar el hiperplano discriminante.
- Número finito de iteraciones

| Dado                                    | Encontrar                             |
| --------------------------------------- | ------------------------------------- |
| Conjunto de patrones                    | Hiperplano discriminante              |
| Vector entrada: $x=(x_{1},\dots,x_{n})$ | $(w_{1},\dots,w_{n}, u)$  tales que   |
| salida deseada: $d(x)=1$ si $x\in C^1$  | $x_{1}w_{1}+\dots+x_{n}w_{n}+w_{0}=0$ |
|                 $d(x)=-1$ si $x\in C^2$| separe las clases $C^1$ y $C^2$       |


**Pasos del proceso de aprendizaje:
1. Inicialización aleatoria de los pesos y el umbral de la red $\{w_{i}(0)\}_{i=0,\dots,n}u(0)$
2. Se toma un patrón entrada-salida $[x=(x_1 ,x_2 , ..., x_n ), d(x)]$
3. Se calcula la salida de la red: $y = f (x1·w1 + x2·w2 + \dots + xn ·wn +u)$
	- Si $y = d(x)$ (clasificación correcta) se vuelve al paso 2
	- Si $y \neq d(x)$ (clasificación incorrecta) se modifican los parámetros y se vuelve al paso 2
	- Ley de aprendizaje: 
		 $w_{i}(t+1)=w_{i}(t)+d(x)·x_{i}$
		- $u(t+1)=u(t)+d(x)$


**Regla de aprendizaje de Windrow-Hoff
- $w_{i}(t+1)=w_{i}(t)+(d(x)-y(x))·x_{i}$
- $u(t+1)=u(t)+d(x)-y(x)$
Para casos en los que la función de activación sea entre 0 y 1, tiene un comportamiento similar a la ley anterior .
La idea es utilizar el error cometido por la red para adaptar los pesos

**Razón de aprendizaje:

A veces pasa que entre iteraciones puede haver cambios muy bruscos, haciendo que se clasifiquen mal patrones que ya estaban bien clasificados, para esto se introduce la razón de aprendizaje:
- $w_{i}(t+1)=w_{i}(t)+d(x)·x_{i}· \alpha$
- $u(t+1)=u(t)+d(x)· \alpha$
### Limitaciones
Si no existe un hiperplano ->La ley de aprendizaje no encuentra la solución, por ejemplo al clasificar estos puntos:
![[Pasted image 20230525121343.png]]
Una solución puede ser combinando varios perceptrones:
![[Pasted image 20230525121409.png]]

Esta aproximación puede ser complicada de llevar a cabo en al práctica, pues **la ley de aprendizaje no es aplicabe** y los pesos tendrían que ser determinados mediante un proceso manual

### Ejemplo patrones bidimensionales
**Hiperplano**: $x_{1}w_{1}+x_{2}w_{2}+u=0$

|     |     |
| --- | --- |
| ![[Pasted image 20230525113537.png]]    | ![[Pasted image 20230525113545.png]]    |


