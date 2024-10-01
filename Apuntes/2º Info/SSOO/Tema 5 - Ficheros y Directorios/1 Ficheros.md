# Repaso almacenamiento
- Memoria principal. 
	- Memoria volátil -> datos no persistentes. 
	- Datos accedidos por el procesador. 
- Memoria secundaria. 
	- Memoria no volátil -> datos persistentes. 
	- Organizada en bloques de datos. 
	- Se necesita una abstracción para simplificar las aplicaciones: Fichero

# Sistemas de ficheros
- Ofrece al usuario una visión lógica simplificada del manejo de los dispositivos periféricos en forma de ficheros.
- Proporciona un mecanismo de abstracción que oculta los detalles relacionados con el almacenamiento y distribución de la información en los periféricos.
- Constituye la parte del S.O. que gestiona los ficheros.
- Funciones: 
	- Organización 
	- Almacenamiento 
	- Recuperación 
	- Gestión de nombres 
	- Implementación de la semántica de Coutilización 
	- Protección

La funcion principal del SF es establecer una correspondencia entre los los ficheros y los dispositivos logicos. Mientras el usuario tiene una vision logica (Ficheros, Directorios, Sistemas de Ficheros y particiones) el sistema tiene la vision fisica (Bloques y bytes).

El acceso a dispositivios es incomodo (hay que saber los detalles fisicos del dispositivo y dependiente de las direcciones fisicas), ademas no es seguro.
El sistema de ficheros es una capa de software que se situa entre dispositivos y usuarios.
Objetivos:
- Suministrar una visión lógica de los dispositivos. 
- Ofrecer primitivas de acceso cómodas e independientes de los detalles físicos. 
- Mecanismos de protección.

## Caracteristicas para el usuario
- Almacenamiento permanentes de información. 
- No desaparece aunque se apague el computador. 
- Conjunto de información estructurada de forma lógica según criterios de aplicación. 
- Nombres lógicos y estructurados. 
- No están ligados al ciclo de vida de una aplicación particular. 
- Abstraen los dispositivos de almacenamiento físico. 
- Se acceden a través de llamadas al sistema operativo o de bibliotecas de utilidades.

# Atributos y operaciones de un fichero
## Atributos de un fichero
- **Nombre**: Identificador en formato legible por una persona. 
- **Identificador**: Etiquetan unívoca del archivo 
	- Suele ser numérico. 
- **Tipo de fichero**: necesario en sistemas que proporcionan distintos formatos de Ficheros. 
	- Como mínimo se suele diferenciar el atributo de ejecutable. 
- **Ubicación**: Identificación del dispositivo de almacenamiento y la posición dentro del dispositivo. 
- **Tamaño del fichero**: número de bytes en el fichero, máximo tamaño posible, etc. 
- **Protección**: control de accesos y de las operaciones sobre el fichero. 
- **Información temporal**: de creación, de acceso, de modificación, etc.

### Nombres de fichero y extensión
- **Muy importante para los usuarios**. Es característico de cada sistema de Ficheros. 
- Problema: usar nombre lógicos basados en tiras de caracteres. 
- Motivo: los usuarios no recuerdan el nombre 001223407654 
- **Tipo y longitud cambian** de un sistema a otro: 
	- **Longitud**: fija en MS-DOS o variable en UNIX, Windows. 
	- **Extensión**: obligatoria o no, más de una o no, fija para cada tipo de Ficheros, etc. 
- **Sensibles a tipografía**. 
	- Ejemplo: CATALINA y catalina son el mismo fichero en Windows pero distintos en LINUX. 
- **El sistema de ficheros** **trabaja con descriptores internos**, sólo distingue algunos formatos (ejecutables, texto, ...). 
	- Ejemplo: número mágico UNIX.
- Los **directorios** relacionan nombres lógicos y descriptores internos de ficheros
- Las **extensiones son significativas para las aplicaciones** (html, c, cpp, etc.)

## Operaciones sobre ficheros
- Creación: Asignación de espacio inicial y metadatos. 
- Borrado: Liberación de recursos asociados. 
- Escritura: Almacena información en el fichero. 
- Lectura: Recupera información del fichero.

# Vision logica de un fichero
Conjunto de información relacionada que ha sido definida por su creador. 
## Estructura
Secuencia o tira de bytes (UNIX, POSIX)
![[Pasted image 20230526140111.png]]
- Ninguna 
	- Secuencia de palabras o bytes (UNIX) 
- Estructura sencilla de registros 
	- Líneas 
	- Longitud fija 
	- Longitud variable 
- Estructuras complejas 
	- Documentos con formato (HTML, postscript) 
	- Fichero de carga reubicable (módulo de carga) 
- Se puede simular estructuras de registro y complejas con una estructura plana y secuencias de control 
- ¿Quién decide la estructura? 
	- Interna: El sistema operativo 
	- Externa: Las aplicaciones

## Metodos de acceso
- Acceso directo 
	- Basado en el modelo de acceso a dispositivo de disco. 
	- Fichero dividido en registros de longitud fija. 
	- Se puede especificar el número de registro para las operaciones de lectura y escritura. 
	- Se puede utilizar un puntero de posición para evitar tener que especificar la posición en todas las operaciones. 
	- Permite construir sobre él otros métodos de acceso más complejos (ejemplo: secuencial indexado).

# Compartición
Varios procesos pueden acceder simultáneamente aun fichero, por lo tanto es necesario definir una semántica de coherencia (¿Cuándo son observables por otros procesos las modificaciones a un fichero?) . Se plantean 3 opciones:
- Semántica UNIX. 
- Semántica de sesión. 
- Semántica de archivos inmutables.

## Semántica UNIX
- Las escrituras en un archivo son inmediatamente visibles a todos los procesos.
- Un archivo abierto tiene asociado un puntero de posición.
	- Alternativas en cuanto al puntero. 
		- Cada proceso mantiene su propio puntero de posición. 
		- Posibilidad de que dos procesos puedan compartir el puntero de posición.
- Implicación: 
	- El sistema operativo debe mantener una imagen única del fichero. 
	- Problemas de contención por acceso exclusivo a la imagen.

## Semántica de sesión
- Las escrituras sobre un archivo abierto no son visibles por otros procesos con el archivo abierto.
- Cuando se cierra un fichero los cambios son visibles por otros procesos que abran el fichero posteriormente
- Un fichero puede estar asociado con varias imágenes distintas.
- No hay contención.

## Semántica inmutable
- Un archivo puede ser declarado como compartido. 
	- A partir de ese momento no se puede modificar.
- Un archivo inmutable no admite modificación de 
	- Nombre. 
	- Contenido.

## Semántica de versiones
- Las actualizaciones se hacen sobre copias con nº versión.
- Sólo son visibles cuando se consolidan versiones.
- Sincronización explícita si se requiere actualización inmediata.

## Control de acceso
- Listas de control de acceso. 
	- Definen la lista de usuarios que pueden acceder a un fichero.
	- Si hay diferentes tipos de acceso una lista por tipo de control de acceso.
- Permisos. 
	- Versión condensada. 
	- Tres tipos de acceso (rwx). 
	- Permisos para tres categorías (usuario, grupo, otros).


# Representación
El sistema operativo debe mantener información sobre el fichero llamada metadatos. Los metadatos son dependientes del sistema de ficheros. 
- Importante: Un sistema operativo puede admitir varios sistemas de ficheros.
	- Ejemplo: en Linux se pueden montar particiones Ext2, NTFS, …

## Asignación de espacio en disco
- **Preasignación**: Asignación en creación del tamaño máximo posible del fichero.
	- Se reserva todo el espacio que podría necesitar el fichero.
- **Asignación dinámica**: Asignación de espacio según se va necesitando.
	- División del fichero en unidades de asignación que se van tomando según haga falta.

### Tamaño de asignación
- Cuestiones a considerar:
	- Tamaño de asignación grande -> información contigua en disco.
		- Mas rendimiento
	- Tamaño de asignación pequeño -> aumenta el tamaño de los metadatos.
- Tamaño de asignación fijo -> reasignación de espacio simple
- Tamaño de asignación fijo y grande -> incrementa el malgasto de espacio (fragmentación interna).
- Tamaño de asignación variable y grande -> incrementa el rendimiento, pero aumenta la fragmentación externa.
### Asignación continua

| Asignación continua sin compactar    | Asignacion continua compactada       |
| ------------------------------------ | ------------------------------------ |
| ![[Pasted image 20230527113332.png]] | ![[Pasted image 20230527113343.png]] | 

### Asignación encadenada
- Cada bloque contiene un puntero al bloque siguiente.
- Asignación de bloques de uno en uno.
- No hay fragmentación externa.
- Bloques distribuidos por todo el disco.
- Consolidación del sistema para mejorar las prestaciones de procesamiento de archivos secuenciales.

| Asignación encadenada sin consolidar | Asignación encadenada consolidada    |
| ------------------------------------ | ------------------------------------ |
| ![[Pasted image 20230527113606.png]] | ![[Pasted image 20230527113614.png]] |

### Asignación indexada
- Se mantiene una tabla con los identificadores de las unidades de asignación que forman el fichero.
- Alternativas: 
	- Asignación por bloques. 
	- Asignación por porciones (extents).

| Asignación indexada por bloques      | Asignación por porciones |
| ------------------------------------ | ------------------------ |
| ![[Pasted image 20230527113726.png]] | ![[Pasted image 20230527113740.png]]                         |

## Gestión de espacio de disco
-  El sistema operativo debe saber que bloques están libres.
- Alternativas: 
	- Mapas de bits: Vector con un bit por bloque.
	- Lista encadenada de porciones libres.
	- Indexación: Tabla índice de porciones libres.

## Tipos de representación

### FAT
![[Pasted image 20230527113920.png]]
### UNIX
- Tipo de fichero y protección. 
- Usuario propietario del fichero. 
- Grupo propietario del fichero. 
- Tamaño del fichero. 
- Hora y fecha de creación. 
- Hora y fecha del último acceso. 
- Hora y fecha de la última modificación. 
- Número de enlaces. 
- Punteros directos a bloques (10).
- Puntero indirecto simple. 
- Puntero indirecto doble. 
- Puntero indirecto triple.
![[Pasted image 20230527114004.png]]

### NTFS
![[Pasted image 20230527114021.png]]


# Llamadas al sistema (C)
- `int open(const char * path, int flags, [mode_t mode])
	- Flags: ``O_RDONLY, O_WRONLY, or O_RDWR.
	- Mode: ``O_CREAT, O_APPEND, O_TRUNC, …
	- Devuelve un descriptor de fichero (o -1 si error).

- ``int close(int fildes)
	- Cierra un archivo abierto anteriormente asociado al descriptor fildes (o -1 si error).

- ``ssize_t read(int fd, void * buf, size_t nbyte)
	- fd es el descriptor del archivo
	- buf es el puntero al buffer donde se almacenan los datos leidos
	- nbytes es el numero de bytes a leer (en este caso bufsiz)
	- Devuelve el numero de bytes leidos o -1 si hay error.
Transfiere nbytes bytes del archivo asociado al descriptor fd a la variable (buffer) buf, si se rebasa el final del archivo se leen los bytes que queden.
Si se llega al final del archivo devuelve 0.

- ``ssize_t readd (int fd, void * buf, size_t nbyte)
	- fd es el descriptor del archivo
	- buf es el puntero al buffer donde se almacenan los datos a escribir
	- nbytes es el numero de bytes a escribir
Devuelve el numero de bytes escritos o -1 si hay error.
Transfiere nbytes bytes del buffer buf al archivo asociado al descriptor fd.
Puede escribir menos bytes de los que se le piden, por ejemplo si se llena el disco, se llega al tamaño maximo de un archivo o se interrumpe por una señal.

- ``off_t lseek(int fd, off_t offset, int whence) 
	- ``offset`` es lo que quieres desplazar, puede ser negativo o positivo
	- ``whence`` es desde donde empiezas a contar
		- ``SEEK_SET`` → desde el principio del fichero. 
		- ``SEEK_CUR`` → desde la posición actual 
		- ``SEEK_END`` → desde el final del fichero.
	- Modifica el valor del apuntador del descriptor ``fd`` en el archivo, a la posición explícita en desplazamiento (``offset``) a partir de la referencia impuesta en origen (``whence``). 
	- Retorno = -1 → Error de posicionamiento.

- ``int link(const char *nombre, const char *nuevo);
	- Crea un hard link con nombre ``nuevo`` al archivo ``nombre``.
	- Incrementa contador de enlaces del fichero ``nombre``.

- ``int symlink(const char *nombre, const char *nombre_enlace);
	- Crea un enlace simbólico hacia ``nombre`` desde ``nombre_enlace``. 
	- Crea un nuevo archivo ``nombre_enlace`` que incluye ``nombre`` como únicos datos.

- ``int unlink(const char *nombre);
	- Borra el archivo ``nombre`` siempre que NO tenga enlaces hard pendientes (contador enlaces = 0) y nadie lo tenga abierto.
	- Si hay enlaces duros (contador enlaces > 0) , se decrementa el contador de enlaces.
	- Si algún proceso lo tiene abierto, se espera a que lo cierren todos.