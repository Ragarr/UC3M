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

// for background processes that are zombies or not finished
int *background_processes;
int background_processes_counter = 0;

// es necesario que sea global para que padre e hijos compartan el mismo array 
int *pids; 

// prototypes
int myCalc(char *argv[]);
int myTime();
int get_digits(int n);
int wait_background_processes();

void siginthandler(int param)
{
	printf("****  Saliendo del MSH **** \n");
	//signal(SIGINT, siginthandler);
	exit(0);
}


/* Timer */
pthread_t timer_thread;
unsigned long  mytime = 0;

void* timer_run ()
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
	background_processes = (int*)malloc(10*sizeof(int));

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
				if (strcmp(argvv[0][0], "mycalc") == 0) {
					myCalc(argvv[0]);
				}
				else if (strcmp(argvv[0][0], "mytime") == 0){
					myTime();
				}
				else{// es un comando externo
					// vamos a crear tantos procesos como comandos haya (dentro del bucle for) 
					// y tantos pipes como comandos - 1
					pids = (int*)malloc(command_counter*sizeof(int));
					int pipefd[command_counter-1][2];
					
					for (int i = 0; i<command_counter; i++){
						// crear pipe para el proceso actual (i)
						if (pipe(pipefd[i]) < 0) {
							perror("[ERROR] Error al crear el pipe");	
						}
						// crear proceso hijo
						int pid=fork();

						if (pid==0){ // proceso hijo
							// el proceso hijo configura su entrada y salida (a pipes o ficheros)
							// y ejecuta el comando correspondiente

							if (i>0){// comando intermedio o final
								// vamos a redireccionar la entrada hacia el pipe anterior 
								// y esperar al proceso anterior
								
								dup2(pipefd[i-1][0], STDIN_FILENO); // leer el pipe anterior
								close(pipefd[i-1][1]); // cerrar escritura del pipe anterior
								waitpid(pids[i-1], &status, 0); // esperar al proceso anterior
							}

							else{ // comando inicial
								// vamos a redireccionar la entrada desde un fichero si es necesario

								if (strcmp(filev[0], "0") != 0) {
									int fd = open(filev[0], O_RDONLY);
									if (fd < 0) {
										perror("[ERROR] Error al abrir el fichero de entrada");
										exit(1);
									}
									dup2(fd, STDIN_FILENO);
									close(fd);
								}
							}
							// ningun proceso lee su propio pipe asi que cerramos la lectura del pipe actual
							close(pipefd[i][0]);

							if (i<command_counter-1){// no es el comando final
								// vamos a redireccionar la salida hacia el pipe actual
								dup2(pipefd[i][1], STDOUT_FILENO); 
							}
							else{ // comando final
								// vamos a redireccionar la salida y la salida de erro a un fichero si es necesario
								// el ultimo proceso no usa el pipe i para nada asi que lo cerramos
								close(pipefd[i][1]);
								close(pipefd[i][0]);

								// redireccionar salida
								if (strcmp(filev[1], "0") != 0) {
									int fd = open(filev[1], O_WRONLY | O_CREAT | O_TRUNC, 0666);
									if (fd < 0) {
										perror("[ERROR] Error al abrir el fichero de salida");
										exit(1);
									}
									dup2(fd, STDOUT_FILENO);
									close(fd);
								}
								// redireccionar salida de error
								if (strcmp(filev[2], "0") != 0) {
									int fd = open(filev[2], O_WRONLY | O_CREAT | O_TRUNC, 0666);
									if (fd < 0) {
										perror("[ERROR] Error al abrir el fichero de salida de error");
										exit(1);
									}
									dup2(fd, STDERR_FILENO);
									close(fd);
								}
							}
							
							// ya estan redireccionadas las pipes y los ficheros
							// ejecutar el comando
							execvp(argvv[i][0], argvv[i]);
						} 
						else if (pid<0){perror("[ERROR] fork");}
						else{ // proceso padre
							// va a añadir el pid del proceso hijo a la lista de pids
							// cerrar pipes que no se usan
							// y comprobar si el proceso se ejecuta en background o no
							
							pids[i]=pid;
							if (i>0){ 
								// cerrar pipes que no se usan (los del proceso anterior) 
								// porque el proceso que los necesitaba ya los ha heredado y ya no son necesarios
								close(pipefd[i-1][0]);
								close(pipefd[i-1][1]);
							}

							if (i==command_counter-1){ // acabamos de crear el ultimo proceso
								// el pipe del ultimo proceso no se usan nunca asi que lo cerramos
								close(pipefd[i][0]);
								close(pipefd[i][1]);

								if (in_background!=1) { // FOREGROUND
									// esperar a que terminen todos los procesos de la secuencia actual
									for (int j = command_counter-1; j >=0; j--){
										waitpid(pids[j], &status, 0); 
									}
									// esperar a que terminen los procesos en background de secuencias anteriores
									wait_background_processes();

								} else { // BACKGROUND
									// imprimir el pid del ultimo proceso de la secuencia
									// y añadir los pids de esta secuencia a la lista de procesos en background
									fprintf(stderr, "[%d]\n", pid);
									
									// relocalizar memoria para la lista de procesos en background anteriores
									// para concatenarle los pids de esta nueva secuencia al final
									background_processes=(int*)realloc(background_processes, (background_processes_counter+command_counter)*sizeof(int));
									background_processes_counter+=command_counter;
									for (int j = 0; j < command_counter; j++){ 
										// añadir los pids de esta secuencia a la lista de procesos en background (de atrás hacia delante)
										background_processes[background_processes_counter-j]=pids[j];
									}
								}
							}
						}
					}
				}	
			}
		}
	}
	return 0;
}

int wait_background_processes(){ 
	// espera a que terminen todos los procesos en background de secuencias anteriores
	// si han terminado, los recoge para que no queden zombies, y sino los espera

	int status; 
	while (background_processes_counter!=0){
		// se espera de atrás hacia delante por comodidad
		waitpid(background_processes[background_processes_counter-1], &status, 0); 
		background_processes_counter--;
	}
	return 0;
}

int myCalc(char *argv[]){
	// funcion que ejecuta el comando interno mycalc
	// primero comprueba que los argumentos son correctos
	// luego calcula el resultado y lo imprime por pantalla

	long long int acc;							// variable local que guarda Acc (de entorno)
	char *acc_str=(char*) malloc(sizeof(char)); // variable local que guarda Acc (de entorno) en formato string
	long long int resultado = 0; 				// resultado de la operacion
	int resto = 0; 								// resto de la division
	
	// comprobar que el comando tiene 3 argumentos
	if (argv[1] == NULL || argv[2] == NULL || argv[3] == NULL || argv[4] != NULL){
		fprintf(stdout, "[ERROR] La estructura del comando es mycalc <operando_1> <add/mul/div> <operando_2>\n");
		return -1;
	} 
	// comprobar que los operandos son numeros
	if ((atoi(argv[1]) == 0 && strcmp(argv[1],"0")!=0) || (atoi(argv[3]) == 0 && strcmp(argv[3],"0")!=0)){
		fprintf(stdout, "[ERROR] La estructura del comando es mycalc <operando_1> <add/mul/div> <operando_2>\n");
		return -1;
	}
	// comprobar que la operacion es correcta
	if (strcmp(argv[2], "add") != 0 && strcmp(argv[2], "mul") != 0 && strcmp(argv[2], "div") != 0){
		fprintf(stdout, "[ERROR] La estructura del comando es mycalc <operando_1> <add/mul/div> <operando_2>\n");
		return -1;
	}
	
	// con el primer caracter de argv[2] (el operador) seleccionamos la operación
	switch (argv[2][0]){
		case 'a': // SUMA
			// si no existe la variable de entorno Acc, se crea con valor 0
			if (getenv("Acc") == NULL){
				setenv("Acc", "0", 1);
			}
			// calcular resultado
			resultado = atoi(argv[1]) + atoi(argv[3]);
			
			// modificar Acc
			acc = atoll(getenv("Acc"));
			acc += resultado;
			// convertir acc a string
			acc_str = malloc(sizeof(char)*get_digits(acc));
			sprintf(acc_str, "%lld", acc);
			// guardar acc_str en la variable de entorno Acc
			setenv("Acc", acc_str, 1);
			
			// mostrar resultado por pantalla
			fprintf(stderr, "[OK] %s + %s = %lld; Acc %lld\n", argv[1], argv[3], resultado, acc);
			break;
		
		case 'm': // MULTIPLICACION
			// calcular resultado
			resultado = atoi(argv[1]) * atoi(argv[3]);
			
			// mostrar resultado por pantalla
			fprintf(stderr, "[OK] %s * %s = %lld\n", argv[1], argv[3], resultado);
			break;
		
		case 'd': // DIVISION
			// comprobar que el divisor no es 0
			if (atoi(argv[3])==0){ 
				fprintf(stdout, "[ERROR] Division por 0\n"); 
				return -1;
			}
			// calcular resultado y resto
			resultado = atoi(argv[1]) / atoi(argv[3]);
			resto = atoi(argv[1]) % atoi(argv[3]);
			
			// mostrar resultado por pantalla
			fprintf(stderr, "[OK] %s / %s = %lld; Resto %d\n", argv[1], argv[3], resultado, resto);
			break;
	}
	return 0;
}

int myTime(){
	// funcion que ejecuta el comando interno mytime
	// imprime por pantalla el tiempo transcurrido desde el inicio del minishell (HH:MM:SS)
	int horas, minutos, segundos;
	segundos = mytime / 1000; 	// convertir de milisegundos a segundos
	minutos = segundos / 60; 	// calculo de minutos
	segundos = segundos % 60; 	// segundos restantes despues de quitar los minutos
	horas = minutos / 60; 		// calculo de horas
	minutos = minutos % 60; 	// minutos restantes despues de quitar  las horas
	
	// imprimir por pantalla
	fprintf(stderr, "%02d:%02d:%02d\n", horas, minutos, segundos);
	return 0;
}

int get_digits(int num){
	// funcion que devuelve el numero de digitos de un entero
	// se usa para saber cuanto espacio reservar para guardar el entero en formato string
	int digits = 0;
	while (num != 0){
		// dividir entre 10 y contar el numero de veces que se puede hacer (que es el numero de digitos)
		digits++;
		num /= 10;
	}
	return digits;
}