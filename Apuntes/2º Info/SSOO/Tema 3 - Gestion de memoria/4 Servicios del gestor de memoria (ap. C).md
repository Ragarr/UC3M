El gestor de memoria realiza funciones internas y ofrece pocos servicios directos a aplicaciones. 
# Servicios POSIX
- Gestión de la proyección de archivos: mmap, munmap.
- Gestión de bibliotecas dinámicas: dlopen, dlsym, dlclose.

## Proyección de archivos en memoria
Los archivos proyectados en memoria son una forma alternativa de acceder a archivos en comparación con read/write. Esto reduce las llamadas al sistema, evita copias intermedias en la caché del sistema de archivos y facilita la programación. 
Una vez proyectado, se puede acceder al archivo como si fuera una estructura de datos en memoria. 
Esta técnica se utiliza para cargar bibliotecas dinámicas, donde la zona de código se proyecta como compartida y la zona de datos con valor inicial se proyecta como privada.
![[Pasted image 20230414173529.png]]
### Proyección en POSIX
#### `void *mmap(argumentos);
Establece proyección entre espacio de direcciones de un proceso y un archivo.
**6 rgumentos**:
- `void *direc`, dirección donde proyectar. Si es `NULL` el SO elige una.
- `size_t lon`, especifica el número de bytes a proyectar
- `int prot`, Protección para la zona (se pueden combinar con |):
	- `PROT_READ`: Se puede leer. 
	- `PROT_WRITE`: Se puede escribir. 
	- `PROT_EXEC`: Se puede ejecutar. 
	- `PROT_NONE`: No se puede acceder a los datos.
- `int flags`, Propiedades de la región:
	- `MAP_SHARED`: La región es compartida. Las modificaciones afectan al fichero. <mark style="background: #ABF7F7A6;">Los procesos hijos comparten la región</mark>. 
	- `MAP_PRIVATE`: La región es privada. El fichero no se modifica. <mark style="background: #ABF7F7A6;">Los procesos hijos obtienen duplicados no compartidos.</mark> 
	- `MAP_FIXED`: El fichero debe proyectarse en la dirección especificada por la llamada.
- `int fd`, Descriptor del fichero que se desea proyectar en memoria.
- `off_t desp`, Desplazamiento inicial sobre el archivo.
Figura: Arriba fichero, abajo proceso.
![[Pasted image 20230414173921.png]]

### Desproyección en POSIX
#### `void munmap(void *direc, size_t lon);`
Desproyecta parte del espacio de direcciones de un proceso desde la dirección ``direc`` hasta ``direc``+``lon``.

### Ejemplos:
#### Contar el número de blancos en un fichero
```c
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main() {
	int fd;
	struct stat dstat;
	int i, n;
	char *c,
	char * vec;
	// primero se abre el fichero de forma tradicional
	fd = open(“datos.txt”,O_RDONLY);
	// te dice info sobre el fichero en la struct dstat
	fstat(fd, &dstat);
	// proyectamos sobre el vector  vec el archivo fd, que tiene 
	// tamaño dstat.st_size, con permisos de lectura y compartido
	vec = mmap(NULL, dstat.st_size, PROT_READ, MAP_SHARED, fd, 0);
	// cerramos el fichero tradicional pero seguira proyectado
	close(fd);
	c =vec;
	// ahora el fichero se trata como un vector de datos, como
	// so fuera un buffer enorme
	for (i=0;i<dstat.st_size;i++) {
		if (*c==‘ ‘) {
			
			n++;
		}
		c++;
	}
	// hay que desmapear el fichero para cerrarlo
	munmap(vec, dstat.st_size);
	printf(“n=%d,\n”,n);
	return 0;
}
```

#### Copiar un fichero
```c
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main() {
	int i, fd1, fd2;
	struct stat dstat;
	char *vec1, *vec2, *p, *q;
	// abrimos los dos ficheros de forma normal
	fd1 = open(“f1”, O_RDONLY);
	fd2 = open(“f2”,O_CREAT|O_TRUNC|O_RDWR,0640);
	// vemos el tamaño del fichero 1 y ponemos el tamaño
	// del segundo igual al primero
	fstat(fd1,&dstat);
	ftruncate(fd2, dstat.st_size);
	// mapeamos los ficheros
	vec1=mmap(0, bstat.st_size,PROT_READ, MAP_SHARED, fd1,0);
	vec2=mmap(0, bstat.st_size, PROT_READ, MAP_SHARED, fd2,0);
	// cerramos los ficheros tradicionales
	close(fd1); close(fd2);
	
	// navegamos los ficheros mientras que los copiamos 
	p=vec1; 
	q=vec2;
	for (i=0;i<dstat.st_size;i++) {
		*q++ = *p++;
	}
	
	munmap(fd1, bstat.st_size);
	munmap(fd2, bstat.st_size);
	return 0;
}
```
## Bibliotecas dinámicas
### Generación
![[Pasted image 20230414174508.png]]
### Enlace
Normalmente el enlace implícito con bibliotecas dinámicas es suficiente.

Si se hace un enlace explícito, hay que escribir el código para cargar y enlazar los símbolos de la biblioteca dinámica. Ejemplo de uso: Decidir en tiempo de ejecución entre dos bibliotecas dinámicas que implementan una misma API.
### Bibliotecas dinámicas en POSIX

#### `void * dlopen(const char * bib, int flags);`
Carga una biblioteca dinámica y la enlaza con el proceso actual.
Devuelve un descriptor que puede usarse posteriormente con dlsym y dlclose.
**Argumentos:**
- ``const char * bib``: Nombre de la biblioteca.
- `int flags`: Opciones.
	- RTLD_LAZY: Resolución diferida de referencias.
	- RTLD_NOW: Resolución inmediata de referencias

####  `void * dlsym(void * ptrbib, char * simb);`
 Devuelve un puntero a un símbolo de la biblioteca dinámica.
 **Argumentos**:
 - `void * ptrbib`: Es el descriptor de biblioteca obtenido mediante dlopen.
 - `char * simb`: Cadena con el nombre del símbolo a cargar

#### `void dlclose(void * ptrbib);`
Descarga la biblioteca dinámica del proceso.

### Ejemplos
#### Carga explícita de biblioteca dinámica
```c
#include <stdio.h>
typedef void (*pfn)(void);
int main() {
	void * bib;
	pfn func;
	bib = dlopen(“libhola.so”, RTLD_LAZY);
	func=dlsym(bib,”hola”);
	(*func)();
	dlclose(bib);
	return 0;
}
```
