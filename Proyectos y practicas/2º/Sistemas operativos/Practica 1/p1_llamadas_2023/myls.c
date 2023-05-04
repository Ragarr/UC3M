// P1-SSOO-22/23

#include <stdio.h>	  	// Header file for system call printf
#include <unistd.h>	  	// Header file for system call gtcwd
#include <sys/types.h> 	// Header file for system calls opendir, readdir y closedir
#include <dirent.h>		// Header file for system calls opendir, readdir y closedir
#include <sys/stat.h>	// Header file for system call stat
#include <fcntl.h>
#include <stdlib.h>
#include <string.h> 
#include <linux/limits.h> // for PATH_MAX 

int main(int argc, char *argv[])
{
	DIR *dir;			// DIR es un tipo de dato que contiene la informacion de un directorio, 
						// opendir devuelve un puntero a DIR
	
	struct dirent *ent; // readdir devuelve un puntero a struct dirent
						// struct dirent contiene la informacion de un fichero del directorio
	if (argc == 2)
	{// si se pasa un argumento, abrir el directorio pasado como argumento
		dir = opendir(argv[1]);
	}
	else if (argc == 1)
	{// si no se pasa ningun argumento, abrir el directorio actual
		char buffer[PATH_MAX]; 	// PATH_MAX: constante del sistema, maximo tamaño de un path
								// buffer es un array de char que contiene la ruta del directorio actual
		if (getcwd(buffer, PATH_MAX) == NULL)
		{ 	// try to get the current working directory
			printf("Error al obtener el directorio actual\n");
			exit(-1);
		}
		dir = opendir(buffer); // open the current working directory
	}
	else
	{
		printf("Faltan argumentos\n");
		exit(-1);
	}
	if (dir == NULL)
	{
		printf("Error al abrir el directorio\n");
		exit(-1);
	}
	while ((ent = readdir(dir)) != NULL)
	{	// leer el contenido del directorio
		printf("%s\n", ent->d_name); // d_name es un array de char que contiene el nombre del fichero	
	}
	closedir(dir);
	exit(0);
}
