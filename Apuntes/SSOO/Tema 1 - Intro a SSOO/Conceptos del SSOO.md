# Funciones del SO
- Gestor de recursos (UCP, memoria, ...)
	- Asignación y recuperación de recursos
	- Protección de los usuarios
	- Contabilidad/monitorización
	- Soporte de usuario
- Máquina extendida (servicios)
	- Ejecución de programas ([[Procesos|procesos]])
	- Órdenes de E/S
	- Operaciones sobre archivos 
	- Detección y tratamiento de errores 
- Interfaz de usuario 
	- Shell

# Niveles del SO
El SO está formado conceptualmente por 3 capas principales:
- Núcleo o Kernel
- [[Ficheros y directorios en C|Servicios o llamadas al sistema]]
- Intérprete de mandatos o shell
![[Pasted image 20230309133039.png]]
# Estructura conceptual
Modos de ejecución:
- Modo usuario: Ejecución de procesos de usuario.
- Modo supervisor o núcleo: Ejecución del núcleo del SO. 
Los procesos y el SO utilizan espacios de memoria separados. 
Cuando un [[Procesos|proceso]] necesita un servicio lo solicita al SO mediante una llamada al sistema. ->El sistema operativo entra en ejecución para realizar la función solicitada.

# Alternativas de estructura
Existen los SSOO [[Conceptos del SSOO#Monoliticos|monoliticos]] y los [[Conceptos del SSOO#Estructurados|estructurados]] 

## Monoliticos
- No hay una estructura clara y bien definida. 
- Todo el código del SO está enlazado como un único ejecutable (un solo espacio de direcciones) que se ejecuta en modo “núcleo”.
- El código presenta cierta organización pero internamente no existe ocultación de información entre los distintos módulos, pudiéndose llamar unos a otros sin restricciones 
- Aunque es más eficiente en su funcionamiento, su desarrollo y mantenimiento es muy complejo. 
- Ejemplos: 
	- Todos los SO hasta los 80, incluido UNIX 
	- MS-DOS y variantes actuales de UNIX: Solaris, Linux, AIX, HP-UX,...


## Estructurados
### Sistemas Estructurados por capas
  El sistema se organiza como un conjunto de capas superpuestas, cada una con una interfaz clara y bien definida 
- Cada capa se apoya en los servicios de la inmediatamente inferior para realizar sus funciones
- Las ventajas son la modularidad y la ocultación de la información, que facilita mucho el desarrollo y la depuración de cada capa por separado.
- Esta estructura, sin embargo, no resulta tan eficiente porque una determinada operación en la capa superior implica realizar múltiples llamadas desde el nivel superior hasta el inferior. 
- Dificultad a la hora de distribuir las distintas funciones del SO entre las distintas capas 
- Ejemplos:
	- THE 
	- OS/2

![[Pasted image 20230309134116.png]]

###  Cliente/servidor
- Implementar la mayor parte de los servicios del SO como [[Procesos|procesos]] de usuario, dejando solo una pequeña parte corriendo en modo núcleo denominada micronúcleo o microkernel
- Hay dudas sobre qué funciones debe implementar realmente el microkernel pero al menos: interrupciones, gestión básica de [[Procesos|procesos]] y memoria y servicios básicos de comunicación 
- Ventajas 
	- Muy flexible. Cada servidor puede desarrollarse y depurarse más fácilmente al tratarse de programas pequeños y especializados. 
	- Es fácilmente extensible a un modelo distribuido 
- Desventajas 
	- Sobrecarga en la ejecución de los servicios 
- Ejemplos: 
	- Minix y Amoeba (Tanenbaum) 
	- Mac OS y Windows NT, aunque en realidad los servicios se ejecutan en espacio kernel para no penalizar el rendimiento → ¿Microkernel?
![[Pasted image 20230309134421.png]]


# Clasificación de SSOO
![[Pasted image 20230309134631.png]]