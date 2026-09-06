// P1-SSOO-22/23

#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{

    if (argc < 3)
    {
        printf("Faltan argumentos\n");
        return -1;
    }
    int fd_env = open("env.txt", O_RDONLY);
    if (fd_env == -1)
    {
        printf("Error abriendo env.txt, asegurate de que esta en la misma carpeta que myenv\n");
        exit(-1);
    }
    int fd_out = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0666); // se abre archivo de salida (escritura), si no existe se crea, si existe se sobreescribe

    if (fd_out == -1)
    {
        printf("Error al abrir o crear %s\n", argv[1]);
        exit(-1);
    }
    char var[strlen(argv[1])]; // variable que vamos a buscar en el fichero
    strcpy(var, argv[1]);      // copiamos el nombre de la variable a buscar
    strcat(var, "=");          // añadimos el igual para que la busqueda sea mas sencilla
    int var_len = strlen(var); // longitud de la variable, incluyendo el igual, se guarda en una variable para no tener que calcularlo cada vez que se use.

    int BUFFER_SIZE = BUFSIZ; // BUFSIZ es una constante del sistema que indica el tamaño del buffer por defecto (8192 bytes), el codigo funciona con cualquier tamaño de buffer mayor que 0
    int n_read;               // numero de bytes leidos
    int n_write;              // numero de bytes escritos
    char buffer[BUFFER_SIZE]; // buffer para leer del fichero

    int index_of_coincidence = 0; // indice que guarda el numero de caracteres que coinciden con la variable, ademas sirve de indice para navegar el string de la variable
    int apariciones = 0;          // numero de apariciones de la variable en el fichero
    int writing = 0;              // si estamos escribiendo o no

    while ((n_read = read(fd_env, buffer, BUFFER_SIZE)) > 0)
    {
        buffer[n_read] = '\0'; // añadimos el caracter de fin de cadena para marcar el final del buffer leido.
        // cuando escribimos sobre un buffer que ya estaba escrito se queda almacenado lo que habia antes si no se reescribe,
        // por eso es necesario poner el caracter de fin de cadena tras el ultimo byte leido para no repetir palabras
        for (int i = 0; i < BUFFER_SIZE; i++)
        {   // recorremos el buffer caracter a caracter
            if (writing == 0)
            {   // si no estamos escribiendo estamos buscando la variable
                if (buffer[i] == var[index_of_coincidence])
                {
                    // las letras actuales coinciden, aumentamos el indice
                    index_of_coincidence++;
                }
                else if (buffer[i] == '\0')
                {
                    // hemos llegado al final del buffer, salimos del bucle for para cargar el siguiente buffer
                    break;
                }
                else
                {
                    // las letras actuales no coinciden, reiniciamos el indice
                    index_of_coincidence = 0;
                }
                if (index_of_coincidence == var_len)
                {   // si el indice coincide con la longitud de la variable, hemos encontrado la variable
                    writing = 1;                            // en la proxima iteracion empezaremos a escribir el contenido de la variable
                    n_write = write(fd_out, &var, var_len); // Escribimos el nombre de la variable con el igual (si no solo se escribiria el contenido)
                    index_of_coincidence = 0;               // reiniciamos el indice para la siguiente aparicion de la variable
                    apariciones++;
                }
            }
            else
            { //  escribimos el contenido de la variable (despues del igual)
                if (buffer[i] == '\n')
                { // si encontramos un salto de linea, hemos llegado al final de la variable, dejamos de escribir
                    writing = 0;
                    n_write = write(fd_out, "\n", 1);
                }
                else
                { // escribimos el caracter actual
                    n_write = write(fd_out, &buffer[i], 1);
                }
                if (n_write == -1)
                { // si hay algun error al escribir, salimos del programa
                    printf("Error escribiendo en %s\n", argv[2]);
                    exit(-1);
                }
            }
        }
    }
    if (n_read == -1)
    {
        printf("Error leyendo env.txt\n");
        exit(-1);
    }
    if (apariciones == 0)
    {
        printf("Variable no encontrada\n");
        exit(0);
    }
    if (close(fd_env) == -1)
    {
        printf("Error cerrando env.txt\n");
        exit(-1);
    }
    if (close(fd_out) == -1)
    {
        printf("Error cerrando %s\n", argv[2]);
        exit(-1);
    }
    exit(0);
}
