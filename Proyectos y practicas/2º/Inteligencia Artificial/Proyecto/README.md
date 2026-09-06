# Práctica Inteligencia Artificial UC3M 2023
### Por Alberto Penas Díaz ([@seniorbeto](https://github.com/seniorbeto)) y Raúl  Aguilar Arroyo ([@Ragarr](https://github.com/Ragarr))
## Resumen
Este proyecto trata de codificar el problema propuesto como enunciado en un Modelo Oculto de Markov (MDP) e implementarlo 
de la manera más general posible en python. Para ello se ha hecho uso de las ecucaciones de Bellman
para distinguir la política óptima de cada estado y así poder generar una simulación realista 
del problema propuesto. 

<img src="https://latex.codecogs.com/svg.image?{\color{White}&space;V(s)=\min_{a&space;\in&space;A(s)}\left[C(a)&space;&plus;&space;\sum_{s'&space;\in&space;S}P(s'&space;\mid&space;s,a)V(s')\right]}" title="https://latex.codecogs.com/svg.image?{\color{White} V(s)=\max_{a \in A(s)}\left[C(a) + \sum_{s' \in S}P(s' \mid s,a)V(s')\right]}" />

El objetivo principal era generalizar la idea al máximo, para poder introducir en el código cualquier 
problema codificabe en un MDP y así, tener máxima flexibilidad a la hora de cambiar parámetros y poder
ver cómo afectan a la resolución del problema. 

## Implementación

Se ha trabajado con las librerías `pandas y matplotlib` para la generación de los data frames y gráficas
respectivamente. Los data frames se generan a partir de los .csv localizados en src/data/ , los cuales representan 
la función de transición de cada posible acción (en nuestro caso, como se trata de un termostato, nuestras
únicas acciones son "Turn ON" y "Turn OFF"). 

Toda la lógica del problema se halla en thermostat.py, el cual es el encargado de llamar en bucle a su función 
interna `calculate_bellman()` para actualizar su valor esperado y su acción más conveniente hasta que este valor
converja. Por defecto, esta convergencia se calcula automáticamente, pero es posible especificar a través de un argumento el número de iteraciones
que se desee en la llamada de lal función `self.__update_V()`. 

## Metodo de uso

Utilizar esta herramienta es muy sencillo, primero de todo, hay que instalar 
las librerías necesarias: desde la terminal (y recomendablemente dentro de un entorno virtual)
ejecutar el siguiente comando: `pip install -r requirements.txt`. Una vez hecho esto, desde el archivo main.py, se pueden generar instancias de la clase 
Thermostat configurando los parámetros del mismo:
+ path_data_on: ruta de la tabla de transiciones de la acción "Turn ON" (se recomienda no modificar)
+ path_data_off: ruta de la tabla de transiciones de la acción "Turn OFF" (se recomienda no modificar)
+ objective_temp: temperatura objetivo 
+ cost_on: coste de la acción "Turn ON"
+ cost_off: coste de la acción "Turn OFF"

Si imprimimos este objeto por pantalla, se mostrará por la terminal 
un registro de cada uno de los estados del modelo, junto con su valor esperado y su política óptima.
Por ejemplo:
```python
thermostat = Thermostat(PATH_ON,
                        PATH_OFF,
                        objetive_temp=22,
                        cost_on=1,
                        cost_off=0.03)

print(thermostat)
```

Se nostrará lo siguiente:
```
V(16): 14.179
Acción recomendada: Turn OFF Asociated state: 16. With cost: 0.03. 
V(16.5): 13.879
Acción recomendada: Turn ON Asociated state: 16.5. With cost: 1. 
V(17): 12.76
Acción recomendada: Turn ON Asociated state: 17. With cost: 1. 
V(17.5): 11.527
Acción recomendada: Turn ON Asociated state: 17.5. With cost: 1. 
V(18): 10.28
Acción recomendada: Turn ON Asociated state: 18. With cost: 1. 
V(18.5): 9.03
Acción recomendada: Turn ON Asociated state: 18.5. With cost: 1. 
V(19): 7.78
Acción recomendada: Turn ON Asociated state: 19. With cost: 1. 
V(19.5): 6.531
Acción recomendada: Turn ON Asociated state: 19.5. With cost: 1. 
V(20): 5.279
Acción recomendada: Turn ON Asociated state: 20. With cost: 1. 
V(20.5): 4.036
Acción recomendada: Turn ON Asociated state: 20.5. With cost: 1. 
V(21): 2.759
Acción recomendada: Turn ON Asociated state: 21. With cost: 1. 
V(21.5): 1.607
Acción recomendada: Turn ON Asociated state: 21.5. With cost: 1. 
V(22): 0
Acción recomendada: Turn OFF Asociated state: 22. With cost: 0.03. 
V(22.5): 0.05
Acción recomendada: Turn OFF Asociated state: 22.5. With cost: 0.03. 
V(23): 0.1
Acción recomendada: Turn OFF Asociated state: 23. With cost: 0.03. 
V(23.5): 0.15
Acción recomendada: Turn OFF Asociated state: 23.5. With cost: 0.03. 
V(24): 0.2
Acción recomendada: Turn OFF Asociated state: 24. With cost: 0.03. 
V(24.5): 0.249
Acción recomendada: Turn OFF Asociated state: 24.5. With cost: 0.03. 
V(25): 0.292
Acción recomendada: Turn OFF Asociated state: 25. With cost: 0.03. 
```
Si se quiere obtener una simulación de la evolución de la temperatura a lo largo del tiempo, es posible llamar a la función 
`simulate()`, que acepta como parámetros el termostato creado, el número de iteraciones (correspondiente a 30 minutos por iteración, 
según el enunciado propuesto) y el estado sobre el cual se incicia la simulación (que por defecto es 16). 
Esta función devuelve una lista con los estados a los que el termostato ha transicionado según su acción 
elegida como política óptima. De tal forma, el siguiente fragmento de código:
```python
thermostat = Thermostat(PATH_ON,
                        PATH_OFF,
                        objetive_temp=22,
                        cost_on=1,
                        cost_off=0.03)

simulation = simulate(thermostat, 25, 16.5)
print(simulation)
```
Mostraría la siguiente lista de 25 elementos:
```
['16.5', '17', '17', '17.5', '18', '18.5', '19.5', '20', '20', '20.5', '21.5', '22',
 '22.5', '22', '22', '21.5', '22', '21.5', '22', '21.5', '22.5', '22', '22', '21.5', '22']
```

## Interpretación

Como consideramos que ver una simulación en una lista de elementos impresa por la terminal es una absoluta agonía, 
también hemos implementado una manera sencilla de visualizar la simulación en forma de gráfico. Para realizar esto 
basta con llamar a la función `draw_graph()`. Usando la instancia del termostato que se ha usado previamente, el siguiente fragmento de código:
```python
simulation = simulate(thermostat, 25, 16.5)
draw_graph(simulation, thermostat)
```
Entregaría la siguiente imagen:

<img src="https://user-images.githubusercontent.com/94072018/234992680-4e9e769b-2f6b-4635-87aa-5080636c0506.png" width="400" height="300">

Como se puede comprobar, la gráfica se corresponde con los valores de la simulación impresos por pantalla. Solo que esta 
vez, es lo suficientemente legible como para no querer que se te salgan los ojos de sus órbitas. Para analizar 
más en detalle el funcionamiento del termostato, probaremos unas simulaciones con valores extremos:
+ Para cost_on = 1, cost_off = 0.003, temperatura inicial de 16º y un rango de 300 iteraciones:
    
    <img src="https://user-images.githubusercontent.com/94072018/234995268-7fdf2328-adb5-4e94-90a9-c719288bcc0f.png" width="400" height="300">
  
    Como la polítca óptima de los estados más bajos es "Turn OFF", el termostato se vale de la pequeña probabilidad que hay de transocionar 
    a un estado superior aún estando apagado hasta llegar a un estado cuya política óptima sea "Turn ON". En esta simulación,
    se tardaría en torno a 110 iteraciones (55 horas) llegar a la temperatura establecida como objetivo. Esto pasa porque la diferencia 
    entre los costes de las acciones es considerable y el termostato decide que es más rentable intentar aumentar la temperatura 
    en base a la pequeña posibilidad de subir de temperatura aún estando apagado. 


+ Para cost_on = 1, cost_off = 1, temperatura inicial de 25º y un rango de 20 iteraciones:
     <img src="https://user-images.githubusercontent.com/94072018/234998457-880862a4-587d-476b-a584-72e8a361a4e8.png" width="400" height="300">

    En esta caso, la temperatura no tarda mucho en caer a la temperatura escogida (aproximadamente unas 3 horas) y se mantiene 
    más estable a lo largo del tiempo.











