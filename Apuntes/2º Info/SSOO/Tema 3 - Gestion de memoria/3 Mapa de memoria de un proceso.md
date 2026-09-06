# Generación de un ejecutable
## Definiciones
Aplicación: conjunto de módulos en lenguaje de alto nivel 
Procesado en dos fases: Compilación y Montaje 
- Compilación: 
	- Resuelve referencias dentro cada módulo fuente 
	- Genera módulo objeto
```
Un módulo fuente es un archivo que contiene código en un lenguaje de programación de alto nivel (legible para personas).
Por ejemplo, cada archivo .c que crees es un módulo fuente.
Estos módulos fuente son procesados por un compilador para generar módulos objeto, que son versiones del código en lenguaje de máquina que pueden ser ejecutadas por el procesador.
```
- Montaje (o enlace):
	- Resuelve referencias entre módulos objeto.
	- Resuelve referencias a símbolos de bibliotecas.
	- Genera ejecutable incluyendo bibliotecas.
```
Los módulos objeto pueden ser enlazados juntos para crear un programa ejecutable mediante el enlazador, que resuelve las referencias entre los diferentes módulos objeto y las bibliotecas de funciones para crear un archivo ejecutable que pueda ser cargado en la memoria y ejecutado por el procesador
```
![[Pasted image 20230414161225.png]]
## Formato del ejecutable
Distintos fabricantes usan diferentes formatos, en Linux: Executable and Linkable Format (ELF)
Estructura: Cabecera y conjunto de secciones.
Cabecera:
- Número mágico que identifica a ejecutable
- Punto de entrada del programa
- Tabla de secciones
```
Las secciones contienen diferentes tipos de información, como código ejecutable, datos inicializados, datos no inicializados y otros recursos necesarios para la ejecución del programa.
Por ejemplo, una sección de código contiene el código ejecutable del programa, mientras que una sección de datos contiene variables y constantes utilizadas por el programa.
```
# Mapa de memoria de un proceso
Mapa de memoria o imagen del proceso es un conjunto de regiones
Una región tiene asociada una información (u “objeto memoria”) y es una zona contigua que se trata como una unidad al proteger o compartir.
Cada región se caracteriza por:
- Su región de inicio y fin
- el soporte donde se almacena su contenido inicial
- su protección - RWX (read-write-execute)
- si es de uso compartido o privado
- si es de tamaño fijo o variable
## Creación del mapa de memoria a partir de ejecutable
Ejecución de un programa: Crea mapa a partir de ejecutable
- Regiones de mapa inicial → Secciones de ejecutable
Secciones:
- Código
	- Compartida, RX, T. Fijo, Soporte en Ejecutable 
- Datos con valor inicial 
	- Privada, RW, T. Fijo, Soporte en Ejecutable 
- Datos sin valor inicial 
	- Privada, RW, T. Fijo, Sin Soporte (rellenar 0) 
- Pila 
	- Privada, RW, T. Variable, Sin Soporte (rellenar 0) 
	- Crece hacia direcciones más bajas 
	- Pila inicial: argumentos del programa
![[Pasted image 20230414164026.png]]
### Otras regiones
Durante ejecución de proceso se crean nuevas regiones → Mapa de memoria tiene un carácter dinámico.
- Región de Heap:
	- Soporte de memoria dinámica (malloc en C) 
	- Privada, RW, T. Variable, Sin Soporte (rellenar 0) 
	- Crece hacia direcciones más altas
- Archivo proyectado 
	- Región asociada al archivo proyectado 
	- T. Variable, Soporte en Archivo 
	- Protección y carácter compartido o privado especificado en proyección
```
Un archivo proyectado es un archivo que se ha mapeado en la memoria de un proceso, lo que permite acceder a su contenido directamente desde la memoria en lugar de tener que leerlo desde el disco. Esto se logra mediante el uso de funciones del sistema operativo como mmap en POSIX, que establece una proyección entre el espacio de direcciones de un proceso y un archivo en el disco. Una vez que se ha establecido la proyección, el contenido del archivo se puede acceder como si fuera una estructura de datos en memoria, lo que puede mejorar el rendimiento al evitar copias intermedias y reducir el número de llamadas al sistema. Los archivos proyectados también pueden ser compartidos entre procesos, lo que permite una comunicación rápida y eficiente entre ellos.
```
- Memoria compartida 
	- Región asociada a la zona de memoria compartida. 
	- Compartida, T. Variable, Sin Soporte (rellenar 0) 
	- Protección especificada en proyección 
- Pilas de threads
	- Cada pila de thread corresponde con una región 
	- Mismas características que pila del proceso 
- Carga de biblioteca dinámica 
	- Se crean regiones asociadas al código y datos de la biblioteca

#### Características de regiones
| Región        | Soporte     | Protección  | Comp/Priv   | Tamaño   |
| ------------- | ----------- | ----------- | ----------- | -------- |
| Código        | Fichero     | RX          | Compartida  | Fijo     |
| Dat. con v.i. | Fichero     | RW          | Privada     | Fijo     |
| Dat. sin v.i. | Sin soporte | RW          | Privada     | Fijo     |
| Pilas         | Sin soporte | RW          | Privada     | Variable |
| Heap          | Sin soporte | RW          | Privada     | Variable |
| F. Proyect.   | Fichero     | por usuario | Comp./Priv. | Variable |
| M. Comp.      | Sin soporte | por usuario | Compartida  | Variable | 
Ejemplo de mapa: 
![[Pasted image 20230414164759.png]]

# Bibliotecas de objetos
Las bibliotecas son colecciones de módulos objeto relacionados.Estas bibliotecas pueden ser del sistema o creadas por el usuario. 
Las **bibliotecas estáticas** se enlazan con los módulos objeto del programa durante el montaje, lo que resulta en un ejecutable autocontenido.
Sin embargo, el montaje estático tiene algunas desventajas, como el tamaño grande de los ejecutables, la repetición del código de función de biblioteca en muchos ejecutables, múltiples copias en memoria del código de función de biblioteca y la necesidad de volver a montar para actualizar una biblioteca.
## Bibliotecas dinámicas
Un ejecutable puede contener el nombre de una biblioteca y una rutina para cargarla y montarla en tiempo de ejecución.
Cuando se hace referencia a un símbolo de la biblioteca por primera vez durante la ejecución, la rutina carga y monta la biblioteca correspondiente y ajusta la instrucción que realiza la referencia para que las próximas referencias accedan al símbolo de la biblioteca. Sin embargo, esto podría modificar el código del programa, por lo que una solución típica es utilizar una referencia indirecta mediante una tabla.
El uso de bibliotecas dinámicas es transparente, los mandatos de compilación y montaje son igual que con estáticas.
### Pros y contras
**Pros**:
- Menor tamaño de los ejecutables.
- Código de rutinas de biblioteca solo en archivo de biblioteca.
- Procesos pueden compartir código de biblioteca. 
- Actualización automática de bibliotecas: Uso de versiones.
**Contras**:
- Mayor tiempo de ejecución debido a carga y montaje
	- Tolerable: Compensa el resto de las ventajas
- Ejecutable no autocontenido.
### Compartición de bibliotecas dinámicas
Las bibliotecas dinámicas contienen referencias internas, lo que puede presentar un problema cuando se comparten entre procesos debido a las autorreferencias.
```
Las referencias internas en una biblioteca dinámica son referencias a símbolos (como funciones o variables) que se encuentran dentro de la misma biblioteca. Estas referencias son necesarias para que el código de la biblioteca pueda llamar a sus propias funciones o acceder a sus propias variables.
```
Hay tres posibles soluciones para este problema:
1. Asignar un rango de direcciones fijo a cada biblioteca dinámica, lo que puede ser poco flexible.
2. Reajustar las autorreferencias durante el montaje en tiempo de ejecución, lo que impide compartir el código de la biblioteca.
3. Crear una biblioteca con código independiente de posición (PIC), que se genera con direccionamiento relativo a un registro, aunque esto puede ser menos eficiente (tolerable).
