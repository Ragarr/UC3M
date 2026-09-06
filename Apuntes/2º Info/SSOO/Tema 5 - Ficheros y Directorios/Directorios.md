# Directorios
Su objetivo es organizar y localizar los ficheros.
- Es un objeto que relaciona de forma unívoca un nombre de usuario de fichero con su descriptor interno.
- Organizan y proporcionan información sobre la estructuración de los sistemas de ficheros.
- Un directorio tiene entrada por cada fichero que alberga.
	- Información de la entrada: 
		- Descriptor interno del fichero. 
		- Posiblemente, algunos atributos del fichero

## Vision logica
- Cuando se abre un fichero el SO busca el nombre en la estructura de directorios.
- Operaciones sobre un directorio:
	- Crear (insertar) y borrar (eliminar) directorios. 
	- Abrir y cerrar directorios. 
	- Renombrar directorios. 
	- Leer entradas de un directorio.
- La organización jerárquica de un directorio
	- Simplifica el nombrado de ficheros (nombres únicos)
	- Proporciona una gestión de la distribución -> agrupar ficheros de forma lógica (mismo usuario, misma aplicación)

# Estructura
- Alternativas:
	- Directorio de un único nivel. 
	- Directorio de dos niveles. 
	- Directorio con estructura de árbol. 
	- Directorio con estructura de grafo acíclico. 
	- Directorio con forma de grafo generalizado.

## Directorio de un nivel
- Un único directorio para todos los usuarios.
- Problemas con el nombrado de los ficheros. 
	- Alta probabilidad de coincidencia de nombres.
![[Pasted image 20230527115153.png]]

## Directorio de dos niveles
- Un directorio por cada usuario.
- Camino de acceso automático o manual
- El mismo nombre de fichero para varios usuarios
- Búsqueda eficiente, pero problemas de agrupación
![[Pasted image 20230527115244.png]]

## Directorio con estructura de arbol
- Búsqueda eficiente y agrupación
- Nombres relativos y absolutos -> directorio de trabajo
![[Pasted image 20230527115317.png]]
Los nombres relativos parten del directorio de trabajo o 
actual
 - Cambio de directorio: 
	- cd /spell/mail/prog
	- cd prog
- Borrar un fichero: rm \<nombre-fichero>
- Crear un subdirectorio: mkdir \<nombre_dir>
- Ejemplo: 
	- cd /spell/mail 
	- mkdir count
	- ls /spell/mail/count
- Borrar un subdirectorio: rm -r mail

## Directorio de grafo aciclico
- Tienen ficheros y subdirectorios compartido
- Este concepto no es visible para el usuario en Windows.
![[Pasted image 20230527115536.png]]
- **link**: Un fichero con varios nombres -> control de enlaces 
	- un único fichero con contador enlaces en descriptor (e. Físicos) 
	- ficheros nuevos con el nombre destino dentro (e. simbólicos)
- Borrado de enlaces: 
	- a) decrementar contador; si 0 borrar fichero 
	- b) recorrer los enlaces y borrar todos 
	- c) borrar únicamente el enlace y dejar los demás
- Problema grave: existencia de bucles en el árbol. Soluciones:
	- Permitir sólo enlaces a ficheros, no subdirectorios 
	- Algoritmo de búsqueda de bucle cuando se hace un enlace
- Limitación de implementación en UNIX: sólo enlaces físicos dentro del mismo sistema de ficheros.

## Estructura de los directorios
- Alternativas de implementación de directorios: 
	- Utilizar bloques especiales con la información del directorio. 
	- Utilizar un fichero cuyo contenido es el directorio.
- Información en un directorio: nombre, tipo, dirección, longitud máxima y actual, tiempos de acceso y modificación, dueño, etc.
	- En caso de usar un fichero la mayoría son metadatos de dicho fichero.

### Alternativas
- Directorios para ficheros contiguos. 
	- Asumen que todos los ficheros se almacenan con asignación contigua+
- Directorios para ficheros enlazados. 
	- Asumen que todos los ficheros se almacenan con asignación no contigua y los bloques se representan como una lista enlazada.
- Directorios para ficheros indexados. 
	- Asumen que todos los ficheros se almacenan con asignación no contigua y los bloques o extents se representan mediante una estructura indexada


#### Directorio para ficheros contiguos
- Entrada de directorio: 
	- Atributos del fichero en entrada de directorio. 
	- Identificador del primer bloque del fichero. 
	- Tamaño del fichero.
- Ej: ISO-9660 de CD-ROM
![[Pasted image 20230527120005.png]]

#### Directorios para ficheros enlazados
- Entrada de directorio: 
	- Atributos de fichero. 
	- Número del primer bloque. 
	- Tamaño del fichero
- Ej: FAT
![[Pasted image 20230527120048.png]]

#### Directorio para ficheros indexados
- Alternativa más usada.
- Entrada de directorio:
	- Nombre. 
	- Identificador de metadatos de fichero (nodo-i, entrada MFT, …)
![[Pasted image 20230527120144.png]]
- Ventajas:
	- No hay que modificar el directorio para cambiar los atributos de un fichero. 
	- No hay que modificar el directorio cuando un fichero cambia de longitud. 
	- Un nodo-i puede representar un directorio o un fichero. 
		- Sencillez en la construcción de sistemas jerárquicos. 
	- La longitud de los nombres no está predeterminada.
	- Fácil creación de sinónimos para el nombre de un fichero.
	-  Eficiencia: localizar un fichero rápidamente
	- Nombrado: conveniente y sencillo para los usuarios 
		- Dos usuarios pueden tener el mismo nombre para ficheros distintos 
		- Los mismos ficheros pueden tener nombres distintos 
		- Nombres de longitud variable 
	- Agrupación: agrupación lógica de los ficheros según sus propiedades (por ejemplo: programas Pascal, juegos, etc.) 
	- Estructurado: operaciones claramente definidas y ocultación
	- Sencillez: la entrada de directorio debe ser lo más sencilla posible.

# Interpretación de nombres
- Cada directorio se almacena como un fichero con pares <número de i-nodo, nombre de fichero>.
- Inicialmente en memoria el directorio /.
- ¿Cuantos bloques de disco ocupa un directorio? 
	- Depende del número de ficheros en el directorio y de la longitud de los nombres.
- La búsqueda en un directorio es secuencial

Ejemplo: Localizar el i-nodo del fichero ``/users/daniel/notas.txt.
![[Pasted image 20230527122600.png]]

## Jerarquia de directorios
- ¿Árbol único de directorios? 
	- Por dispositivo lógico en Windows (c:\users\miguel\claves, j:\pepe\tmp, ...) ¤
	- Para todo el sistema en UNIX (/users/miguel/claves, /pepe/tmp, ...).
- Hacen falta servicios para construir la jerarquía: ``mount`` y ``umount``. 
	- ``mount /dev/hda /users
	- ``umount /users
- Ventajas: imagen única del sistema y ocultan el tipo de dispositivo
- Desventajas: complican la traducción de nombres, problemas para enlaces físicos entre ficheros

## Sistema de ficheros y particiones
- **Volumen**: conjunto coherente de metainformación y datos. 
- Ejemplos de Sistemas de ficheros:
![[Pasted image 20230527122749.png]]

## Montado de particiones
![[Pasted image 20230527122830.png]]

# Manipulación de directorios
Servicios que realizan el tratamiento de los archivos que representan directorios.

- ``int mkdir(const char *name, mode_t mode);
	- ``name`` nombre del directorio 
	- ``mode`` bits de protección
	- Devuelve 0 ó -1 si error
	- Descripción: 
		- Crea un directorio de nombre name.
		- UID_dueño = UID_efectivo 
		- GID_dueño = GID_efectivo

- ``int rmdir(const char *name);
	- ``name`` nombre del directorio
	- Devuelve:  0 ó -1 si error
	- Descripción: 
		- Borra el directorio si está vacío. 
		- Si el directorio no está vacío no se borra.

- ``DIR *opendir(char *dirname);
	- ``dirname`` puntero al nombre del directorio
	- Devuelve: 
		- Un puntero para utilizarse en readdir() o closedir(). 
		- NULL si hubo error.
	- Descripción: Abre un directorio como una secuencia de entradas. Se coloca en el primer elemento.

- ``int closedir(DIR *dirp);
	- ``dirp`` puntero devuelto por opendir().
	- Devuelve: 0 ó -1 si error.
	- Descripción: Cierra la asociación entre ``dirp`` y la secuencia de entradas de directorio.

- ``struct dirent *readdir(DIR *dirp);
	- ``dirp`` puntero retornado por opendir().
	- Devuelve: 
		- Un puntero a un objeto del tipo ``struct dirent`` que representa una entrada de directorio 
		- NULL si hubo error.
	- Descripción: 
		- Devuelve la siguiente entrada del directorio asociado a ``dirp``. 
		- Avanza el puntero a la siguiente entrada.
		- La estructura es dependiente de la implementación. Debería asumirse que tan solo se obtiene un miembro: ``char *d_name``.

- ``void rewindir(DIR *dirp);
	- ``dirp`` puntero devuelto por opendir()
	- Descripción: Sitúa el puntero de posición dentro del directorio en la primera entrada.

- ``int link(const char *existing, const char *new);``
- ``int symlink(const char *existing, const char *new);
	- ``existing`` nombre del archivo existente.
	- ``new`` nombre de la nueva entrada que será un enlace al archivo existente.
	- Devuelve: 0 ó -1 si error.
	- Descripción: 
		- Crea un nuevo enlace, físico o simbólico, para un archivo existente. 
		- El sistema no registra cuál es el enlace original. 
		- ``existing`` no debe ser el nombre de un directorio salvo que se tenga privilegio suficiente y la implementación soporte el enlace de directorios

- ``int unlink(char *name);
	- ``name`` nombre de archivo
	- Devuelve: 0 ó -1 si error
	- Descripción: 
		- Elimina la entrada de directorio y decrementa el número de enlaces del archivo correspondiente. 
		- Cuando el número de enlaces es igual a cero y ningún proceso lo mantiene abierto, se libera el espacio ocupado por el archivo y el archivo deja de ser accesible.

- ``int chdir(char *name);
	- ``name`` nombre de un directorio
	- Devuelve: 0 ó -1 si error
	- Descripción: Modifica el directorio actual, aquel a partir del cual se forman los nombre relativos.

- ``int rename(char *old, char *new);
	- ``old`` nombre de un archivo existente 
	- ``new`` nuevo nombre del archivo
	- Devuelve: 0 ó -1 si error
	- Descripción:  Cambia el nombre del archivo ``old``. El nuevo nombre es ``new``.

- ``char *getcwd(char *buf, size_t size);``
	- ``buf`` puntero al espacio donde almacenar el nombre del directorio actual 
	- ``size`` longitud en bytes de dicho espacio
	- Devuelve: Puntero a ``buf`` o NULL si error.
	- Descripción: Obtiene el nombre del directorio actual