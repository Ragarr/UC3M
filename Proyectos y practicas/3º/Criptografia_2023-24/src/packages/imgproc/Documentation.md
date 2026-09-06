# Paquete ImgProc
Se han implementado dos funciones sencillas para tratar píxeles individuales en imágenes
con formato .jpg. Estas funciones son:

## Función `getColors`

Recibe como parámetros la ruta de la imagen y la región de la imagen que se quiere analizar.
La función devuelve, en forma de diccionario, los colores que aparecen en la región de la imagen,
de modo que las claves del diccionario son las coordenadas del píxel y los valores son los colores,
en formato hexadecimal, correspondientes al pixel perteneciente a dichas coordenadas.

Si no se especifica la región de la imagen, la función devuelve los colores de toda la imagen.

### Ejemplo de uso: 

Con el siguiente código:
```python 
from imgproc import getColors

getColors('data/shrek.jpg', 0, 0, 5, 5)
```
Siendo la imagen: 

![shrek](data/shrek.jpg)

Devolvería:

```
{(0, 0): '#FFFFFF',
 (0, 1): '#FFFFFF',
 (0, 2): '#FFFFFF',
 (0, 3): '#FFFFFF',
 (0, 4): '#FFFFFF',
 (1, 0): '#FFFFFF',
 (1, 1): '#FFFFFF',
 (1, 2): '#FFFFFF',
 (1, 3): '#FFFFFF',
 (1, 4): '#FFFFFF',
 (2, 0): '#FFFFFF',
 (2, 1): '#FFFFFF',
 (2, 2): '#FFFFFF',
 (2, 3): '#FFFFFF',
 (2, 4): '#FFFFFF',
 (3, 0): '#FFFFFF',
 (3, 1): '#FFFFFF',
 (3, 2): '#FFFFFF',
 (3, 3): '#FFFFFF',
 (3, 4): '#FFFFFF',
 (4, 0): '#FFFFFF',
 (4, 1): '#FFFFFF',
 (4, 2): '#FFFFFF',
 (4, 3): '#FFFFFF',
 (4, 4): '#FFFFFF'}
 ```

En este caso, todos los colores de los píxeles de la región especificada corresponden al color blanco.


## Función `updatePixels`

Esta función recibe como parámetros la ruta de la imagen y la región de la imagen que se quiere cambiar.
Además, recibe una lista de tuplas, donde cada tupla contiene el color, en formato rgb, de los píxeles
establecidos en la región de la imagen especificada.

### Ejemplo de uso 

Con el siguiente código:

```python
from imgproc import updatePixels
from random import randint as rd

new = []
for _ in range(50):
    for _ in range(100):
        new.append((rd(0, 255), rd(0, 255), rd(0, 255)))

updatePixels("data/shrek.jpg", 0, 0, 50, 100, new)
```

y siendo la imagen la misma utilizada en el ejemplo anterior, se obtendría la siguiente imagen:

![shrek](src/imgproc/new_image.png)