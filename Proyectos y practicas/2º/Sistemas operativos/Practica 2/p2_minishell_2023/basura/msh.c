//P2-SSOO-22/23

// MSH main file
// Write your msh source code here

//#include <parser.h> 
#include <stddef.h>         /* NULL */
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <wait.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>
#include <time.h>
#include <pthread.h>

#define MAX_COMMANDS 8


// ficheros por si hay redirección
char filev[3][64];

//to store the execvp second parameter
char *argv_execvp[8];			// crea un array de 8 punteros a caracteres

// prototypes
int myCalc(char *argv[]);
int myTime();
int get_digits(int n);

void siginthandler(int param)
{
	printf("****  Saliendo del MSH **** \n");
	//signal(SIGINT, siginthandler);
	exit(0);
}


/* Timer */
pthread_t timer_thread;
unsigned long  mytime = 0;

void* timer_run ( )
{
	while (1)
	{
		usleep(1000);
		mytime++;
	}
}

/**
 * Get the command with its parameters for execvp
 * Execute this instruction before run an execvp to obtain the complete command
 * @param argvv
 * @param num_command
 * @return
 */
void getCompleteCommand(char*** argvv, int num_command) {
	//reset first
	for(int j = 0; j < 8; j++)
		argv_execvp[j] = NULL;

	int i = 0;
	for ( i = 0; argvv[num_command][i] != NULL; i++)
		argv_execvp[i] = argvv[num_command][i];
}



/**
 * Main sheell  Loop  
 */

int main(int argc, char* argv[])
{
	/**** Do not delete this code.****/
	int end = 0; 
	int executed_cmd_lines = -1;
	char *cmd_line = NULL;
	char *cmd_lines[10];

	if (!isatty(STDIN_FILENO)) {
		cmd_line = (char*)malloc(100);
		while (scanf(" %[^\n]", cmd_line) != EOF){
			if(strlen(cmd_line) <= 0) return 0;
			cmd_lines[end] = (char*)malloc(strlen(cmd_line)+1);
			strcpy(cmd_lines[end], cmd_line);
			end++;
			fflush (stdin);
			fflush(stdout);
		}
	}

	pthread_create(&timer_thread,NULL,timer_run, NULL);

	/*********************************/

	char ***argvv = NULL;
	int num_commands;


	while (1) 
	{
		int status = 0;
		int command_counter = 0;
		int in_background = 0;
		signal(SIGINT, siginthandler);

		// Prompt 
		write(STDERR_FILENO, "MSH>>", strlen("MSH>>"));

		// Get command
		//********** DO NOT MODIFY THIS PART. IT DISTINGUISH BETWEEN NORMAL/CORRECTION MODE***************
		executed_cmd_lines++;
		if( end != 0 && executed_cmd_lines < end) {
			//printf("Correction mode\n"); // for debug
			command_counter = read_command_correction(&argvv, filev, &in_background, cmd_lines[executed_cmd_lines]);
		}
		else if( end != 0 && executed_cmd_lines == end){
			return 0;
		}
		else{
			//printf("Normal mode\n"); // for debug
			command_counter = read_command(&argvv, filev, &in_background); //NORMAL MODE
		}
		//************************************************************************************************


		/************************ STUDENTS CODE ********************************/
		if (command_counter > 0) {
			if (command_counter > MAX_COMMANDS){
				printf("Error: Numero máximo de comandos es %d \n", MAX_COMMANDS);
			}
			else {
				//printf("imprimiendo comandos\n"); // for debug
				// delete this loop after debug
				// print command manually aaa | bbb bbb | ccc ccc ccc > file1.txt < file2.txt &
				/*for (int i = 0; i < command_counter; i++) {
					int j = 0;
					while (argvv[i][j] != NULL) {
						printf("mandato %d, elemento %d %s \n",i,j, argvv[i][j]);
						j++;
					}
					printf("\n");
				}
				printf("fichero de entrada %s \n", filev[0]);
				printf("fichero de salida %s \n", filev[1]);
				printf("fichero de error %s \n", filev[2]);

				printf("in_background %d \n", in_background);
				printf("numero de comandos %d \n", command_counter);
				printf("fin de comandos\n");
				// end delete this loop after debug
				*/
				// Print command
				print_command(argvv, filev, in_background);

				// Execute command
				if (strcmp(argvv[0][0], "mycalc") == 0) {
					// printf("ejecutando mycalc\n"); // for debug
					// ejecutar mycalc en un proceso aparte
					myCalc(argvv[0]);
				}
				else if (strcmp(argvv[0][0], "mytime") == 0){
					myTime();
				}
				else{
					// ejecutar comando externo
					printf("ejecutando comando externo\n"); // for debug

					// create pipes
					int pipes[command_counter-1][2];
					for (int i = 0; i < command_counter-1; i++) {
						pipe(pipes[i]);
					}
					int pid[command_counter];
					for (int i = 0; i < command_counter; i++) {
						
						pid[i] = fork();
						if (pid[i] == 0) {
							// hijo
							fprintf(stderr, "[DEBUG] Proceso hijo %d creado\n", i);
							// ver si hay que redirigir entrada
							if (i == 0 && strcmp(filev[0], "0") != 0){
								// nos encontramos en el primer comando y hay que redirigir entrada (comando < fichero)
								int fd_in = open(filev[0], O_RDONLY);
								if (fd_in < 0) {
									perror("[ERROR] Error al abrir el fichero de entrada");
									exit(1);
								}
								fprintf(stderr, "[DEBUG] El proceso %d tiene un archivo de entrada: \n", i);
								// print_file(fd_in);
								// cambiar el descriptor de fichero de entrada estandar por el del fichero de entrada
								dup2(fd_in, STDIN_FILENO);
								close(fd_in);
							}
							else if (i > 0) {
								// nos encontramos en un comando intermedio (comando | comando_actual)
								
								// cerrar descriptor de lectura (salida) de la tuberia anteriorl
								close(pipes[i-1][1]);
								fprintf(stderr, "[DEBUG] el proceso %d tiene un pipe de entrada: \n", i);
								// cambiar el descriptor de fichero de entrada estandar por el de lectura de la tuberia anterior
								dup2(pipes[i-1][0], STDIN_FILENO);
								// print_file(STDIN_FILENO);
								close(pipes[i-1][0]);
							}
							
							// ver si hay que redirigir salida
							if (i == command_counter-1 && strcmp(filev[1], "0") != 0){
								// nos encontramos en el ultimo comando y hay que redirigir salida (comando_actual > fichero)
								int fd_out = open(filev[1], O_WRONLY | O_CREAT | O_TRUNC, 0666);
								if (fd_out < 0) {
									perror("[ERROR] Error al abrir el fichero de salida");
									exit(1);
								}
								// cambiar el descriptor de fichero de salida estandar por el del fichero de salida
								dup2(fd_out, STDOUT_FILENO);
								close(fd_out);
							}
							else if (i < command_counter-1) {
								// nos encontramos en un comando intermedio (comando_actual | comando)
								
								// cerrar descriptor de escritura (entrada) de la tuberia actual NOT SURE
								close(pipes[i][0]);
								// cambiar el descriptor de fichero de salida estandar por el de escritura de la tuberia actual
								dup2(pipes[i][1], STDOUT_FILENO);
								close(pipes[i][1]);
							}

							// ver si hay que redirigir error
							if (strcmp(filev[2], "0") != 0){
								// hay que redirigir error (comando 2> fichero)
								int fd_err = open(filev[2], O_WRONLY | O_CREAT | O_TRUNC, 0666);
								if (fd_err < 0) {
									perror("[ERROR] Error al abrir el fichero de error");
									exit(1);
								}
								// cambiar el descriptor de fichero de salida de error por el del fichero de error
								dup2(fd_err, STDERR_FILENO);
								close(fd_err);
							}

							// ejecutar comando
							// print argvv[i] for debug
							fprintf(stderr,"ejecutando comando %d: ", i);
							for (int j = 0; argvv[i][j] != NULL; j++) {
								fprintf(stderr,"%s ", argvv[i][j]);
							}
							fprintf(stderr,"\n");
							fprintf(stderr, "[DEBUG] El comando utiliza los ficheros: \n"); // for debug
							fprintf(stderr, "[DEBUG] entrada: %d, salida: %d, error: %d\n", STDIN_FILENO, STDOUT_FILENO, STDERR_FILENO); // for debug
							execvp(argvv[i][0], argvv[i]);
							// si llega aqui es que ha habido un error
							perror("[ERROR] Error al ejecutar el comando");

							// cerrar tuberias
							fprintf(stderr, "[DEBUG] Cerrando tuberias\n"); // for debug
							for (int i = 0; i < command_counter-1; i++) {
								close(pipes[i][0]);
								close(pipes[i][1]);
							}
							exit(1);
						}
						else if (pid[i] < 0) {
							// error al crear el proceso
							perror("[ERROR] Error al crear el proceso");
							// cerrar tuberias
							fprintf(stderr, "[DEBUG] Cerrando tuberias\n"); // for debug
							for (int i = 0; i < command_counter-1; i++) {
								close(pipes[i][0]);
								close(pipes[i][1]);
							}
							exit(1);
						}
						else {
							// esperar a que termine el proceso 
							fprintf(stderr, "[DEBUG] Esperando a que termine el proceso %d\n", i);
							waitpid(pid[i], &status, 0);
							fprintf(stderr, "[DEBUG] Proceso %d terminado\n", i);

						}
					}

					
						else if (pid < 0) {
							// error
							printf("Error: no se ha podido crear el proceso hijo \n");
							exit(1);
						}
					}
					// parent process

					
					
			}
		}
	}
	
	return 0;
}

int myCalc(char *argv[]){
	/*	El minishell debe proporcionar el comando interno mycalc cuya
		sintaxis es:
		mycalc <operando_1> <add/mul/div> <operando_2>
		Para ello debe:
		1. Comprobar que la sintaxis es correcta.
		2. Ejecutar la operación elegida: suma (add), multiplicación
		(mul) o división (div).
		3. Mostrar por pantalla los resultados.
		• Caso correcto por la salida estándar de error.
		• Error por la salida estándar.
		Operación “add” tiene una variable de entorno “Acc” que acumula
		los resultados de las sumas realizadas, pero no de las
		multiplicaciones y las divisiones.*/
	// Comprobar que la sintaxis es correcta.
	// comprobar que hay 4 argumentos
	
	long long int acc;	// variable local que guarda Acc (de entorno)
	char *acc_str=(char*) malloc(sizeof(char));
	long long int resultado = 0;
	int resto = 0;
	if (argv[1] == NULL || argv[2] == NULL || argv[3] == NULL || argv[4] != NULL){
		fprintf(stdout, "[ERROR] La estructura del comando es mycalc <operando 1> <add/mul/div> <operando 2>\n");
		return -1;
	} // comprobar que el comando es mycalc
	if (strcmp(argv[0], "mycalc") != 0){
		// esto no deberia pasar nunca
		fprintf(stdout, "[ERROR] La estructura del comando es mycalc <operando 1> <add/mul/div> <operando 2>\n");
		return -1;
	}// comprobar que los operandos son numeros
	if (atoi(argv[1]) == 0 || atoi(argv[3]) == 0){
		fprintf(stdout, "[ERROR] La estructura del comando es mycalc <operando 1> <add/mul/div> <operando 2>\n");
		return -1;
	}// comprobar que la operacion es correcta
	if (strcmp(argv[2], "add") != 0 && strcmp(argv[2], "mul") != 0 && strcmp(argv[2], "div") != 0){
		fprintf(stdout, "[ERROR] La estructura del comando es mycalc <operando 1> <add/mul/div> <operando 2>\n");
		return -1;
	}
	// Ejecutar la operación elegida: suma (add), multiplicación (mul) o división (div).
	switch (argv[2][0]){
		case 'a':
			// CREAR LA VARIABLE DE ENTORNO ACC SI NO EXISTE
			if (getenv("Acc") == NULL){
				setenv("Acc", "0", 1);
			}
			resultado = atoi(argv[1]) + atoi(argv[3]);
			// guardar resultado en Acc
			acc = atoi(getenv("Acc"));
			acc += resultado;
			acc_str = malloc(sizeof(char)*get_digits(acc));
			sprintf(acc_str, "%lld", acc);
			setenv("Acc", acc_str, 1);
			// mostrar resultado por pantalla
			fprintf(stderr, "[OK] %s + %s = %lld, Acc = %lld\n", argv[1], argv[3], resultado, acc);
			break;
		case 'm':
			resultado = atoi(argv[1]) * atoi(argv[3]);
			// mostrar resultado por pantalla
			fprintf(stderr, "[OK] %s * %s = %lld\n", argv[1], argv[3], resultado);
			break;
		case 'd':
			resultado = atoi(argv[1]) / atoi(argv[3]);
			resto = atoi(argv[1]) % atoi(argv[3]);
			// mostrar resultado por pantalla
			fprintf(stderr, "[OK] %s / %s = %lld, resto = %d\n", argv[1], argv[3], resultado, resto);
			break;
	}
	return 0;
}


int myTime(){
	//la variable global esta en milisegundos
	int horas, minutos, segundos;
	segundos = mytime / 1000; // segundos
	minutos = segundos / 60;  // minutos
	segundos = segundos % 60; // segundos restantes despues de quitar los minutos
	horas = minutos / 60; // horas
	minutos = minutos % 60; // minutos restantes despues de quitar  las horas
	fprintf(stderr, "%02d:%02d:%02d\n", horas, minutos, segundos);
}

int get_digits(int num){
	int digits = 0;
	while (num != 0){
		digits++;
		num /= 10;
	}
	return digits;
}



------------------------------------------------------------------------------------------------------------------------------
// crear tuberias
					int pipes[command_counter-1][2];
					for (int i = 0; i < command_counter-1; i++) {
						pipe(pipes[i]);
					}
					fprintf(stderr,"[DEBUG] %d tuberias creadas\n", command_counter-1); // for debug

					// crear procesos
					int pid[command_counter];
					for (int i = 0; i < command_counter; i++) {
						pid[i] = fork();
						if (pid[i]==0){
							// proceso hijo
							fprintf(stderr, "[DEBUG] proceso hijo %d\n", i); // for debug
							// redireccionar entrada
							if (i == 0 && strcmp(filev[0], "0") != 0) {
								fprintf(stderr, "[DEBUG] redireccionando entrada\n"); // for debug
								int fd = open(filev[0], O_RDONLY);
								if (fd == -1) {
									perror("[ERROR] open");
									exit(EXIT_FAILURE);
								}
								close(STDIN_FILENO);
								dup2(fd, STDIN_FILENO);
								close(fd);
							}
							// redireccionar salida
							if (i == command_counter-1 && strcmp(filev[1], "0") != 0) {
								fprintf(stderr, "[DEBUG] redireccionando salida\n"); // for debug
								int fd = open(filev[1], O_WRONLY | O_CREAT | O_TRUNC, 0666);
								if (fd == -1) {
									perror("[ERROR] open");
									exit(EXIT_FAILURE);
								}
								close(STDOUT_FILENO);
								dup2(fd, STDOUT_FILENO);
								close(fd);
							}
							// redireccionar error
							if (i == command_counter-1 && strcmp(filev[2], "0") != 0) {
								fprintf(stderr, "[DEBUG] redireccionando error\n"); // for debug
								int fd = open(filev[2], O_WRONLY | O_CREAT | O_TRUNC, 0666);
								if (fd == -1) {
									perror("[ERROR] open");
									exit(EXIT_FAILURE);
								}
								close(STDERR_FILENO);
								dup2(fd, STDERR_FILENO);
								close(fd);
							}
							// redireccionar tuberias

							// AIUDA

							// ejecutar comando
						
							execvp(argvv[i][0], argvv[i]);
							perror("[ERROR] execvp");
							exit(EXIT_FAILURE);
						}else if (pid[i] > 0){
							// proceso padre
							

						}else{
							// error
							perror("[ERROR] fork");
							exit(EXIT_FAILURE);
						}
				