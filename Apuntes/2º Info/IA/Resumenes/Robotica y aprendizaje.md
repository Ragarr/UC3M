# Robótica
## Concepto de robot
![[Pasted image 20230523185833.png]]
### Sensores y actuadores
Los sensores recogen la información del entorno y los actuadores se encargan de "actuar" sobre el entorno.
Algunos ejemplos:

| Sensores | Actuadores |
| -------- | ---------- |
| Infrarojo | Brazo      |
| Laser     | Altavoz    |
| GPS       | email      |
| ...       | ...        |


### Controladores
Hay varios tipos de controladores:
- **Teoría de Control Clásica**
	- Valores de los controladores relacionados matemáticamente con la entrada. 
	- Aplicaciones industriales. 
- **Sistemas de Reglas** 
	- Valores de los controladores relacionadas semánticamente con las entradas. 
	- Por lo que generan movimientos bruscos
	- Juegos, entornos planificados, etc.. 
- **Sistemas Borrosos** 
	- El uso de los conceptos borrosos permite un controlador que aúna los dos anteriores. 
	- Permiten eliminar los saltos entre situaciones y hacer las transiciones más suaves.
	- Lavadoras, frenos de trenes, ABS, enfoque de las cámaras.

### Cerebro del robot
**Representación del Mundo** de manera semántica mediante relaciones entre objetos o mediante quadtree.
Generación de acciones mediante planificación.
Uso fundamentalmente de las capacidades de razonamiento y del Alto nivel.

#### Representación del mundo
Por ejemplo, la construcción de un mapa, pre-programado o aprendido.
![[Pasted image 20230523190638.png]]
### Planificación por tareas
![[Pasted image 20230523191014.png]]

#### Relación entre la representación del mundo y el planificador
- **Estado o situación**: 
	- descripción instantánea en(robot1, sala1), puerta-abierta(puerta1,sala1,sala2), puerta-cerrada(puerta2, sala1, sala3), ... 
- Acción u Operador: qué puede hacer el robot 
	- levantar, dejar, empujar, mover, girar, … 
	- Metas: visitada(sala3) 
	- Plan: mover(robot1, sala1, sala2, puerta1), … 
- Criterios: 
	- tiempo, precio, …

## Arquitectura Reactiva
En lugar de seguir un plan predefinido o depender de modelos internos complejos, la arquitectura reactiva permite que el robot tome decisiones y realice acciones basadas en estímulos inmediatos y cambios en su entorno.
![[Pasted image 20230523191421.png]]


# Aprendizaje Automático
## Metodología
1. Formular el problema 
2. Determinar la representación (atributos y clases) 
	- directamente 
	- hablando con expertos 
	- a partir de otras técnicas (filtros) 
3. Identificar y recolectar datos de entrenamiento 
	- bases de datos, ficheros, …
4. Preparar datos para análisis 
5. Selección de modelo, construcción y entrenamiento 
6. Evaluar lo aprendido
	- validación cruzada, expertos 
7. Integrar la base de conocimiento a la espera de nuevos datos tras acciones

## Elementos de entrada
En el aprendizaje automático, los elementos básicos de entrada son el **concepto**, el **atributo**, la **clase** y la **instancia o ejemplo**. 
- **El concepto** es la **tarea** que se quiere aprender y puede ser:
	- **clasificación**
	- **predicción**/estimación
	- **asociación**
	- **agrupamiento**. 
- El atributo es la característica que se utiliza para describir el concepto y puede ser:
	- continuo o nominal/categórico. 
	- Ej.: En un modelo de **clasificación** de spam, los atributos pueden ser la frecuencia de 
- **La clase** son los diferentes valores (etiquetas) que puede tomar el concepto aprendido.
- La **instancia** o ejemplo es cada muestra a partir de la cual se extrae el concepto.

### Ejemplos
#### Modelo de clasificación de spam
- **El concepto** sería  **CLASIFICACIÓN**, si un correo electrónico es spam o no spam. 
- **Los atributos** podrían ser el **remitente del correo**, el **asunto del correo**  y el **contenido del correo**. 
- **La clase** sería si el correo electrónico **es spam** o **no spam**. 
- **Una instancia** sería **un correo electrónico específico** que se está clasificando como spam o no spam
#### Modelo predicción de precio de una casa
- El concepto sería **ESTIMAR** el precio de la casa. 
- Los atributos podrían ser el número de habitaciones, el tamaño del lote, la ubicación de la casa y la edad de la casa. 
- La clase sería el precio de la casa. 
- Una instancia sería una casa específica que se está evaluando para predecir su precio.
#### Modelo clasificar una fruta según su sabor
- El concepto es “sabor”
- Los atributos podrían ser las características de la fruta, tamaño, color, forma…
- La clase sería amarga, dulce, salado, …
- Una instancia sería una fruta concreta.
## Tabla de datos
Entrada: Instancias (ejemplos)
![[Pasted image 20230524114527.png]]
Salida: Árbol o tabla de decisión, unas reglas, clúster, modelos de regresión, …

## Preparación de los datos
**Objetivo: única tabla de datos (instancias, atributos)**
Para ello hay que ensamblar, integrar formatos, agregar, …
Que hay que hacer:
- **En las fi**las:
	- **Agregar datos**: seleccionar datos atómicos  y resumirlos con totales o estadísticas que los resuman
- **En las columnas**:
	- **Seleccionar los atributos útiles**: Eliminar campos redundantes o inapropiados, como IDs, etc
	- **Cambiar atributos** de interés de campos textuales, ejemplos:
		- fecha/hora → Edad o estación o mañana-tarde-noche…
		- Dirección/código postal. → lugar geográfico, área, ciudad …

### Integración
Combinar múltiples fuentes (bases o ficheros distintas) en una única, para ello hay que limpiar, transformar y reducir los datos.

#### Limpieza
##### Ruido en los datos-Outliers
Hay que eliminar los outliers (valores anormales), ya sea tratándolos o de manera manual

 Analisis de Clusters                 | Regresión                            
 ------------------------------------ | ------------------------------------ 
 ![[Pasted image 20230524120501.png]] | ![[Pasted image 20230524120510.png]] 
##### Datos incompletos o redundantes
- Datos redundantes: Frecuente al integrar varias bases de datos
	- Detectar relaciones causales o funcionales en datos
		- El mismo atributo con diferente nombre 
		- Relaciones directas: atributo “calculado”
- Datos Incompletos: faltan atributos en algunos ejemplos
	- Relleno manual: tedioso o no posible
	- Ignorar ejemplo: cuando son pocos casos 
	- Nuevo valor “desconocido” 
	- Valor medio, valor más probable según resto, …

#### Selección de datos de entrada
- Aleatoriamente: conjuntos grandes. Verificación.
- Aquellos que se parecen más entre sí.
- Aquellos que se diferencian más entre sí.
- Los datos que están en las fronteras entre las clases.
- Los datos que tienen mayores errores de clasificación se tratan (proporcionalmente) más veces.
- Incremental: incorporar sucesivamente datos de un conjunto reserva

#### Filtrado de atributos
Los errores en los datos son muy comunes y pueden degradar fuertemente el análisis.
Se pueden aplicar técnicas que permitan identificar potenciales problemas, evitando o agilizando la supervisión manual.

**Mejora de árboles de decisión **
- El ruido en los atributos debe incorporarse también en el entrenamiento para aprender a combatirlo 
- Descartar los ejemplos mal clasificados (y reentrenar) frecuentemente reduce la complejidad de la estructura, con diferencias no significativas de prestaciones
- Equivale a un proceso de poda global

**Regresión robusta** 
- Eliminar ejemplos separados más de $3\sigma$
- Estimadores de mínimo error absoluto o de mínima mediana de error cuadrático

#### Búsqueda de atributos
En un espacio de búsqueda con $F$ atributos hay $2^F$ posibles grupos.
Una exploración exhaustiva no es factible con atributos numerosos (>30)
Se puede comenzar por:
- conjunto de atributos de entrada completo (backward elimination) e ir eliminando
- conjunto vacío de atributos (forward selection) e ir añadiendo
Se puede realizar búsqueda:
- En escalada (greedy): mueve 1 atributo cada vez y encuentra el óptimo local.
- Mejor-primero: mantiene todas las ramas y puede hacer backtracking. Es exhaustivo si no se para.
La evaluación de cada nodo  (subconjunto de atributos) se realiza llamando al algoritmo seleccionado (wrapper) o independientemente.

Algunos atributos pueden ser redundantes (como “salario” y “categoría laboral”). y hacen que el proceso de aprendizaje sea más lento, además pueden confundir a algunos clasificadores.
Otros son irrelevantes (como DNI para predecir si una persona va a devolver un credito), puede perjudicar al clasificador.
Todos los esquemas se degradan al incorporar atributos irrelevantes.

**Sobredimensionalidad**:
El número de datos puede crecer exponencialmente con el número de atributos (dimensiones), además puede llevar a sobreaprendizaje, pues incrementa la complejidad del modelo en relacion al número de datos disponibles.

En ocasiones es útil tener el conocimiento de qué atributos son relevantes para una tarea. Cuantos menos atributos, más fácil de interpretar es el modelo

##### Seleccionar atributos
Hay métodos automáticos que permiten seleccionar los atributos basándose en los 3 objetivos mencionados: 
- mejorar las prestaciones
- aumentar la velocidad de ejecución 
- aumentar la legibilidad de la representación
**Tipos de selección:**
- **Métodos filtro**: un método estadístico determina si un atributo es relevante o no respecto a la variable dependiente: Ej. Chi-cuadrado
- **Métodos Wrapper**: la selección de atributos es un problema de búsqueda combinatoria, Ej. Algoritmo de eliminación recursiva de atributos
- **Métodos Embedded**: utilizan métodos de aprendizaje a la vez que se construye el modelo, Ej. LASSO
##### Proyección de atributos
Es una tecnica que puede mejorar el rendimiento del modelo. Se utiliza para reducir la dimensionalidad de los datos y eliminar los atributos redundantes o irrelevantes. Algunas proyecciones interesantes son:
- diferencias de atributos
- el cociente de atributos
- la concatenación de valores de atributos nominales
- la pertenencia a cluster
- la adición de ruido
- la eliminación aleatoria o selectiva de datos.

Aunque ambos persiguen el mismo objetivo, no es lo mismo seleccionar atributos que reducir dimensionalidad.
Reducir atributos o seleccionarlos implica escoger aquellos más representativos/relevantes. Reducir la dimensionalidad crea nuevos atributos a partir de la combinación de otros que posteriormente serán eliminados.

**Proyeccion PCA:**
Es un algoritmo para transformar las columnas de un conjunto de datos en un nuevo conjunto de características llamadas Componentes principales.
La idea detrás del PCA es encontrar una combinación lineal de las variables originales que capture la mayor cantidad posible de la variabilidad en los datos.
- Método no supervisado para identificar las direcciones principales del conjunto de datos 
- Rotación de los datos sobre el sistema de coordenadas (reducido) dado por estas direcciones 
- PCA es un método de reducción de dimensiones
Algoritmo:
1. Encontrar la dirección (eje) de máxima varianza
2. Encontrar la dirección de máxima varianza perpendicular a la anterior y repetir

Implementación: encontrar los autovectores de la matriz de covarianza de los datos
Dados vectores k-dimensionales, buscar vectores ortogonales de dimensión $c\leq k$
$$C=\frac{1}{n}X'X=U \Lambda U'= \begin{pmatrix}
u_{11} & u_{21} \\
u_{12} & u_{22}
\end{pmatrix}\begin{pmatrix}
\lambda_{1} & 0  \\
0 & \lambda_{}{2}
\end{pmatrix}\begin{pmatrix}
u_{11} & u_{12} \\
u_{21} & u_{22}
\end{pmatrix}$$
Donde:

- $C$ es la matriz de covarianza de dimensiones $k \times k$.
- $X$ es la matriz de datos de dimensiones $n \times k$ , donde $n$ es el número de observaciones y $k$ es el número de variables.
- $X'$ es la transpuesta de la matriz $X$.
- $U$ es una matriz de autovectores de dimensiones $k \times k$, donde cada columna de $U$ representa un autovector.
- $\Lambda$ es una matriz diagonal de dimensiones $k \times k$, donde cada elemento en la diagonal es un autovalor.

 .    |     
 --- | --- 
 ![[Pasted image 20230524134558.png]]   |   ![[Pasted image 20230524134547.png]]  

#### Transformación de datos
- **Agregación**: resumen, cubos de datos
- **Normalización**: re-escalar las variables (para distancias)
	- normalización min-max  $$v'=\frac{v-min_{A}}{max_{A}-min_{A}}$$
	- normalización estadística (tipificar) $$v'=\frac{v-media_{a}}{stand\_{dev}_{a}}$$
- **Discretización**: Reducir número de valores, o poner intervalos a variables continuas. Reduce el tamaño de los datos y mejora la precisión. **Ej.: edad->(joven, adulto, mayor).** Se puede discretizar siguiendo:
	- Misma amplitud:
		- Cajas (de un histograma): Amplitud = (Max-min)/N. $W=\frac{max-min}{N}$
		- El más directo. Problemas de escala y con outliers
	- Misma frecuencia
		- Cada caja el mismo número de muestras
	- Métodos supervisados: analogo al filtro del wrapper

## Técnicas de MD-AA
![[Pasted image 20230524134841.png]]
### Tipos de tecnicas
- **Paramétricas**, no paramétricas.
- **Grado de supervisión** 
	- Supervisadas, no supervisadas, por refuerzo 
- **Tipo de información resultante** 
	- Simbólica, subsimbólica/numérica, mixta.
- **Número de técnicas empleadas**.
	- Sencillos, meta-clasificadores.
- **Tipo de clases** 
	- Discretas, continuas, desconocidas.

## Técnicas supervisadas
Se dividen en:
- Clasificación: 
	- Separar instancias de cada categoría (aprender fronteras de clases)
- Predicción:
	- Predecir valores numéricos (aprender funciones de interpolación)

## Clasificación
La clasificación es el proceso de dividir un conjunto de datos en grupos mutuamente excluyentes.

**Precisión de una clasificación**
La precisión de un subconjunto S de atributos para todos los ejemplos de entrenamientos se calculará:
- Clases simbólicas: $$\text{precision}(S)=\frac{\text{ejemplos bien clasificados}}{\text{ejemplos totales}}$$
- Clases numéricas: $$\text{precision}(S)=-RMSE=-\sqrt{ \frac{ \sum_{i \in I}(y_{i}-\hat{y}_{i})^2 }{n} }$$
RMSE es la raíz cuadrada del error cuadrático medio, $n$ es el número de **ejemplos totales**, $y_{i}$ el **valor de la clase** para el ejemplo $i$ y $\hat{y}_{i}$ el **valor predicho** por el modelo para el ejemplo $i$. 

### Tablas de decisión
La tabla de decisión constituye la forma más simple y rudimentaria de representar la salida de un algoritmo de aprendizaje, que es justamente representarlo como la entrada.
Se escopje un subconjunto de atributos y se crea la tabla de decision con este conjunto mas la clase. Ejemplo:

| **Tabla origen**                         | **Tabla de decisión mala**               | **Tabla de decisión buena**              |
| ------------------------------------ | ------------------------------------ | ------------------------------------ |
| ![[Pasted image 20230524151812.png]] | ![[Pasted image 20230524151825.png]] | ![[Pasted image 20230524151834.png]] |
|                                      | Precisión: 50%                       | Precisión: 100%                      |

### Árboles de decisión
Un árbol de decisión es una representación visual de reglas que nos ayudan a tomar decisiones basadas en diferentes atributos. Puede ser visto como un árbol en el que cada rama está etiquetada con un par atributo-valor y las hojas del árbol están etiquetadas con una clase.

#### Problemas apropiados para árboles de decisión
Un problema es apropiado para un arbol de decisión tiene:
- **Atributos discretos** o categóricos: Los atributos del problema deben ser discretos o categóricos, lo que significa que toman un conjunto finito de valores
- **Datos etiquetados**: El conjunto de datos debe estar etiquetado con las clases correspondientes. Esto significa que se deben conocer las clases a las que pertenecen los ejemplos de entrenamiento.
- **Interpretabilidad**: Si se busca una solución fácil de interpretar y explicar
- **Conjunto de datos de tamaño moderado**: Si bien los árboles de decisión pueden manejar conjuntos de datos grandes, tienden a funcionar mejor en problemas con un tamaño moderado de datos.

### Obtener reglas de clasificación
Las reglas de clasificación se pueden obtener mediante dos métodos principales:
1. **Generando un árbol de decisión**: Se puede utilizar un algoritmo de aprendizaje de árboles de decisión para construir un árbol que represente las decisiones basadas en los atributos de los ejemplos de entrenamiento. Una vez que se tiene el árbol de decisión, se pueden extraer las reglas a partir de él. **Cada camino desde la raíz del árbol hasta una hoja representa una regla**, donde los atributos en los nodos internos del camino establecen las condiciones y la etiqueta de la hoja representa la clase asignada.
    
2. **Estrategia de covering**: En este enfoque, se selecciona una clase a la vez y se buscan las reglas necesarias para cubrir todos los ejemplos de esa clase. En otras palabras, **se toma una clase y se buscan los atributos y condiciones que sean comunes a todos los ejemplos de esa clase**. Una vez que se encuentra una regla que cubre todos los ejemplos, se eliminan esos ejemplos y se repite el proceso con la clase siguiente. Este proceso se repite hasta que ya no queden ejemplos de la clase actual.


#### Teoría de la información de Shannon
Dado un conjunto de eventos $A=\{A1, A2,..., An\}$, con probabilidades $\{p1, p2,..., pn\}$
- **Información en el conocimiento de un suceso** $A_{i}$ (bits) $$I(A_{i})=\log_{2}\left( \frac{1}{p_{i}} \right)=-\log_{2}(p_{i})$$
- Información media de A (bits) $$I(A)=\sum_{i=1}^n p_{i}I(A_{i})=-\sum_{i=1}^n p_{i}\log_{2}(p_{i})$$
- Ganancia de información $$G(A_{i})=I-I(A_{i})$$
Donde $p_{i}$ es la probabilidad del suceso.

La información en el conocimiento de un suceso se refiere a la medida de la novedad o sorpresa que obtenemos cuando ocurre un suceso en particular. 
Cuanto menos probable sea un suceso, más información nos proporcionará su ocurrencia.

### Sistema ID3
Seleccionar un atributo como raíz del árbol y crear una rama con cada uno de los posibles valores de dicho atributo.
- Se selecciona el atributo que mejor separe (ordene) los ejemplos de acuerdo a las clases. Para ello se emplea la entropía.

**Pseudocodigo de ID3**
1. Seleccionar el atributo $A_{i}$ que maximice la ganancia $G(A_{i})$. 
2. Crear un nodo para ese atributo con tantos sucesores como valores tenga. 
3. Introducir los ejemplos en los sucesores según el valor que tenga el atributo $A_{i}$. 
4. Por cada sucesor: 
	- Si sólo hay ejemplos de una clase, $C_k$, entonces etiquetarlo con $C_k$. 
	- Si no, llamar a ID3 con una tabla formada por los ejemplos de ese nodo, eliminando la columna del atributo $A_{i}$.

**Ejemplo**
![[Pasted image 20230524161009.png]]
![[Pasted image 20230524161018.png]]

### Algoritmo 1R
Este algoritmo genera un árbol de decisión de un nivel expresado mediante reglas:
```
1R (ejemplos) { 
	Para cada atributo (A) 
		Para cada valor del atributo (Ai) 
			Contar el número de apariciones de cada clase con Ai 
			Obtener la clase más frecuente (Cj) 
			Crear una regla del tipo Ai -> Cj 
		Calcular el error de las reglas del atributo A 
	Escoger las reglas con menor error 
}
```
![[Pasted image 20230524161737.png]]

## Evaluación de un sistema de aprendizaje
Medida de la calidad de un esquema de análisis de datos: tasa de error de clasificación, desviación de predicción,…
Evaluación principalmente de métodos predictivos (clasificación/predicción).
Evaluación de la capacidad para generalizar.

Medidas de calidad: 
-  Número de aciertos (clasificaciones correctas) 
- Precisión de estimadores de probabilidad 
- Error en predicción numérica

**Dilema de la evaluación**
El conjunto de ejemplos se divide en dos partes: entrenamiento (E) y test (T).
Se aplica la técnica (p.e. Naïve Bayes) al conjunto de entrenamiento, generando un clasificador, se estima el error (o tasa de aciertos) que el clasificador comete en el conjunto de test

A mayor conjunto de entrenamiento mejor clasificador. A mayor conjunto de test, más precisa la estimación del error
**Metodo HoldOut**:
- Con un solo conjunto de datos este método reserva un conjunto independiente para test y usa el resto para entrenamiento 
	- Típico: un tercio test, dos tercios entrenamiento 
- Problema: muestras no representativas.
	- Ejemplo: alguna clase falta en el conjunto de test 
- Solución: estratificación
	- Asegura que cada clase se representa con las mismas proporciones en ambos conjuntos

**Validación cruzada**
Una solucion el dilema anterior: Validación cruzada k -veces (k-fold cross validation)
Se divide el conjunto de ejemplos en k partes iguales, $E_{i}$
Se realiza lo siguiente k veces: 
- se entrena con $E - E_{i} (i=1,\dots, k )$
- se calcula el error con el $E_{u}$ , $e_i$ (o el éxito, $f_{i}$ )
Se estima la tasa de error/éxito haciendo la media de los errores

**Leave-one-out**
Leave-one-out es caso particular de of k-fold cross-validation donde se entrena con todos los datos menos con 1.

- Número de carpetas (folds) es el número de ejemplos de entrenamiento.
- Implica construir el clasificador n veces.
- Máximo aprovechamiento de datos
- No hay aleatoriedad en muestreo
- Método más costoso
- No permite estratificación (un solo ejemplo en cada evaluación)

