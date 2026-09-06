El sistema de ficheros permite organizar la información dentro de los dispositivos de almacenamiento secundario en un formato inteligible para el sistema operativo.
Previamente a la instalación del sistema de ficheros es necesario dividir físicamente, o lógicamente, los discos en particiones o volúmenes .
Una partición es una porción de un disco a la que se la dota de una identidad propia y que puede ser manipulada por el sistema operativo como una entidad lógica independiente.
Una vez creadas las particiones, el sistema operativo debe crear las estructuras de los sistemas de archivos dentro de esas particiones. Para ello se proporcionan mandatos como ``format`` o ``mkfs`` al usuario
# Estructura
## Particiones
- Descripción de sistemas de archivos: 
	- El sector de arranque en MS-DOS
	- El superbloque en UNIX
- Relación sistema de archivos-dispositivo:
	- Típico: 1 dispositivo N sistemas de archivos (particiones) 
	- Grandes archivos: N dispositivos 1 sistema de archivos
- Típicamente cada dispositivo se divide en una o más particiones (en cada partición sistema de archivos)
- La tabla de particiones indica el principio, el tamaño y el tipo de cada partición.

### Tipos de particion
![[Pasted image 20230527132428.png]]
### Bloques y agrupaciones
- **Bloque**: agrupación lógica de sectores de disco. ¤
	- Es la unidad de transferencia mínima que usa el sistema de archivos. 
	- Optimizar la eficiencia de la entrada/salida de los dispositivos secundarios de almacenamiento. 
	- Todos los sistemas operativos proporcionan un tamaño de bloque por defecto. 
	- Los usuarios pueden definir el tamaño de bloque a usar dentro de un sistema de archivos mediante el mandato ``mkfs``.
- **Agrupación**: conjunto de bloques que se gestionan como una unidad lógica de gestión del almacenamiento. 
	- El problema que introducen las agrupaciones, y los bloques grandes, es la existencia de fragmentación interna.

![[Pasted image 20230527132543.png]]
