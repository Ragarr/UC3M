//P1-SSOO-22/23

# include <fcntl.h> // for open 
# include <stdio.h> // for printf and scanf
# include <stdlib.h> // for exit
# include <unistd.h> // for close, read, write

int main(int argc, char *argv[])
{

	//If less than two arguments (argv[0] -> program, argv[1] -> file to process) print an error y return -1
	if(argc < 2)
	{
		printf("Faltan argumentos\n");
		exit(-1);
	}
	int fd = open(argv[1], O_RDONLY);
	if(fd == -1)
	{
		printf("Error al abrir el archivo\n");
		exit(-1);
	}
	int bytes = 0; 	// bytes del archivo
	int words = 0;	// palabras del archivo  
	int lines = 0; 	// lineas del archivo -1
					// El comando de Linux wc no cuenta la ultima linea (solo cuenta los intros)
					// nuestro programa hace lo mismo y no cuenta la ultima linea tampoco
					// sino habría que añadir el comando lines++;

	char c, c_prev = '\0'; // se inicializa a \0 para que en caso de que el primer char sea espacio, tabulador o intro no se cuente como palabra
	// c es el char actual y c_prev el char anterior (se usa para no contar multiples espacios como palabras)

	int n_read; // bytes leidos por la funcion read
	char *buffer = (char *) malloc(BUFSIZ);		// BUFSIZ: constante del sistema, buffer por defecto

	while ((n_read = read(fd, buffer, BUFSIZ)) > 0)
	{
		bytes += n_read; // bytes leidos por read
		for(int i = 0; i < n_read; i++)
		{
			c_prev = c;
			c = buffer[i];
			
			if((c == ' ' || c== '\t' || c== '\n') && c_prev!='\0' && c_prev != ' ' && c_prev != '\n' && c_prev != '\t')
			{
				// cada espacio, intro o tabulador es una palabra.
				// Si c_prev es espacio, intro, tabulador o \0 no cuenta la palabra
				// ya que se trata de multiples espacios
				words++;
			} 
			if(c == '\n')
			{
				// cada intro es una linea
				lines++;
			}
		}
	}
	if (n_read == -1)
	{
		printf("Error al leer el archivo\n");
		exit(-1);
	}

	if (c != ' ' && c != '\n' && c != '\t' && c_prev != ' ' && c_prev!='\0' && c!='\0')
	{// este if es para contar la ultima palabra del archivo si no acaba en espacio, tabulador o intro, por que si no se contaria dos veces
		words++;
	}
	if (close(fd)==-1)
	{
		printf("Error al cerrar el archivo\n");
		exit(-1);
	}
	printf("%d %d %d %s\n", lines, words, bytes, argv[1]);
	free(buffer);
	exit(0);
}

