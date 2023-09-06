//SSOO-P3 2022-2023

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stddef.h>
#include <sys/stat.h>
#include <pthread.h>
#include "queue.h"
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <semaphore.h>

// Definiciones
#define MAX_OPERACIONES 200

// Prototipos
int comprobar_n_operaciones(char *vec);
int check_arguments(int argc, char * argv[]);
char *project_file(char *filename);
char **get_list_client_ops(char *vec, int n_op);
void *f_cajero(void *arg);
void *f_trabajador(void *arg);
element get_elem(char *op, int numop);
int procesar_operacion(element* elem);
int traspasar(int cuenta_origen, int cuenta_destino, int cantidad);
int crear_cuenta(int cuenta_origen);
int ingresar(int cuenta_origen, int cantidad);
int retirar(int cuenta_origen, int cantidad);
int saldo(int cuenta_origen);
int traspasar(int cuenta_origen, int cuenta_destino, int cantidad);

// Variables globales
char ** list_client_ops;    // lista de operaciones de los clientes
int client_numop = 0;       // numero de operaciones de los clientes, se incrementa cada
                            // vez que un cliente va a hacer una operación desde un cajero

int bank_numop = 0;         //  se incrementa cada vez que un trabajador va a hacer una operacion
                            // extraıda de la cola circular compartida con los cajero

int global_balance = 0;     //  se actualiza con las operaciones que se realizan (puede ser positivo o negativo).

int total_op;               // numero total de operaciones que se van a realizar
int MAX_CUENTAS;            // numero maximo de cuentas que se pueden crear
int *saldo_cuenta;          // array de cuentas, cada indice es una cuenta y el valor es el saldo de la cuenta

queue * cola_circular;      // cola circular compartida entre cajeros y trabajadores
int quedan_operaciones_por_insertar = 1;  // 1 si quedan operaciones por insertar en la cola circular

// Mutex y variables condicion
pthread_mutex_t mutex_client_numop;
pthread_mutex_t mutex_bank_numop;

pthread_cond_t cond_bank_numop;
pthread_cond_t cond_cola_no_llena;
pthread_cond_t cond_cola_no_vacia;


pthread_mutex_t mutex_cola;
// semaforos
sem_t ** sem_cola;  // mantiene orden de entrada de operaciones a la cola circular desde los cajeros

/**
 * Entry point
 * @param argc
 * @param argv
 * @return
 */

int main (int argc, char * argv[] ) {
    // comprobar correccion de argumentos de entrada
    if (check_arguments(argc, argv) == 0) return -1; 
    
    char * vec;
    if ((vec = project_file(argv[1])) == NULL) return -1; // proyectar fichero en memoria
    
    // comprobar que el numero de operaciones no supera el maximo de 200 y 
    // que el numero de operaciones del fichero coincide con el que pone en la cabecera.
    if ((total_op = comprobar_n_operaciones(vec)) < 0) return -1; 

    // inicializar variables procedentes de parametros de entrada
    int N_CAJER = atoi(argv[2]);
    int N_TRABAJ = atoi(argv[3]);
    MAX_CUENTAS = atoi(argv[4]);
    int TAM_BUFFER = atoi(argv[5]);

    // inicializar array de cuentas
    saldo_cuenta = (int *)malloc(MAX_CUENTAS*sizeof(int));
    for (int i = 0; i < MAX_CUENTAS; i++) {
        // incializamos las cuentas en -infinito
        saldo_cuenta[i] = -__INT32_MAX__;
    }

    list_client_ops = get_list_client_ops(vec, total_op); // lista de operaciones de los clientes
    munmap(vec, strlen(vec)); // desproyectar fichero de memoria
    
    cola_circular = queue_init(TAM_BUFFER); // cola circular compartida entre cajeros y trabajadores

    // inicializar semaforos
    sem_cola = (sem_t **) malloc((total_op)*sizeof(sem_t*));     
    sem_cola[0] = (sem_t *) malloc(sizeof(sem_t));
    // el primer semaforo se inicializa a 1 (el cajero 0 y el trabajador 0 pueden empezar a trabajar)                        
    sem_init(sem_cola[0], 0, 1);
    // el resto de semaforos se inicializan a 0 (el resto de cajeros y trabajadores están bloqueados)
    for (int i = 1; i < total_op; i++) {
        sem_cola[i] = (sem_t *)malloc(sizeof(sem_t));
        sem_init(sem_cola[i], 0, 0);
    }

    // inicializar mutex y variables condicion
    pthread_mutex_init(&mutex_client_numop, NULL);
    pthread_mutex_init(&mutex_bank_numop, NULL);
    pthread_mutex_init(&mutex_cola, NULL);

    pthread_cond_init(&cond_cola_no_llena, NULL);
    pthread_cond_init(&cond_cola_no_vacia, NULL);
    pthread_cond_init(&cond_bank_numop, NULL);


    // inicializar arrays de threads
    pthread_t *cajero;                                              // array de threads de cajeros
    pthread_t *trabajador;                                          // array de threads de trabajadores
    cajero = (pthread_t *)malloc(N_CAJER * sizeof(pthread_t));      // reservar memoria para los arrays
    trabajador = (pthread_t *)malloc(N_TRABAJ * sizeof(pthread_t)); 
    
    // lanzar los N threads de cajeros
    for (int i = 0; i < N_CAJER; i++) {
        pthread_create(&cajero[i], NULL, f_cajero, NULL);
    }
    // lanzar los M threads de trabajadores
    for (int i = 0; i < N_TRABAJ; i++) {
        pthread_create(&trabajador[i], NULL, f_trabajador, NULL);
    }

    // esperar a que terminen los cajeros
    for (int i = 0; i < N_CAJER; i++) {
        pthread_join(cajero[i], NULL);
    }
    // esperar a que terminen los trabajadores
    for (int i = 0; i < N_TRABAJ; i++) {
        pthread_join(trabajador[i], NULL);
    }
    // liberar memoria de los arrays
    free(cajero);
    free(trabajador);

    // destruir mutex y variables condicion
    pthread_mutex_destroy(&mutex_client_numop);
    pthread_mutex_destroy(&mutex_bank_numop);
    pthread_cond_destroy(&cond_cola_no_llena);
    pthread_cond_destroy(&cond_cola_no_vacia);
    pthread_mutex_destroy(&mutex_cola);
    // destruir semaforos
    for (int i = 0; i < total_op; i++) {
        sem_destroy(sem_cola[i]);
    }
    free(sem_cola);

    // destruir cola circular
    queue_destroy(cola_circular);

    return 0;
}

void * f_cajero(void *arg) {
    /*
    Funcion de los cajeros
    */
    int my_numop;           // numero de operacion que va a insertar el cajero en la cola
    element elem;
    while (1){
        // obtener el numero de operacion que va a procesar el cajero y 
        // aumentar el contador de operaciones procesadas por los cajeros
        pthread_mutex_lock(&mutex_client_numop);    
        if (client_numop == total_op) {         // si se han procesado todas las operaciones, salir del bucle
            pthread_mutex_unlock(&mutex_client_numop);
            break;
        }
        my_numop = client_numop;   
        client_numop++;
        pthread_mutex_unlock(&mutex_client_numop);
        
        // crear la el elemento de cola correspondiente a la operacion...
        elem = get_elem(list_client_ops[my_numop], my_numop);       
        sem_wait(sem_cola[my_numop]);       // sirve para que las operaciones se inserten en orden dentro de la cola (la segunda op espera a la primera, el tercero al segundo...)
        
        // bloquear cola para insertar operacion
        pthread_mutex_lock(&mutex_cola);
        while (queue_full(cola_circular))
        {   // si la cola está llena, esperamos a que se libere algun espacio (señal que recibe del trabajador)
            pthread_cond_wait(&cond_cola_no_llena, &mutex_cola);
        }
        queue_put(cola_circular, &elem);    // insertar operacion en cola
        if (my_numop < total_op - 1) {
            // liberar el semaforo del siguiente cajero
            sem_post(sem_cola[my_numop+1]);
        }

        pthread_cond_signal(&cond_cola_no_vacia);       // el trabajador recibe señal de que hay operaciones en cola
        pthread_mutex_unlock(&mutex_cola);
    }
    
    if (my_numop == total_op-1){    // el ultimo cajero envia señal de que no quedan operaciones por insertar a los trabajadores
        quedan_operaciones_por_insertar = 0;
        pthread_cond_broadcast(&cond_cola_no_vacia);    // los trabajadores comprueban si quedan operaciones en cola
    }
    pthread_exit(0);
}

void * f_trabajador(void *arg) {
    /*
    Funcion de los trabajadores
    */
    element * elem;
    int my_bank_numop;  // numero de operacion que va a procesar el trabajador

    while (1){
        // cojer operacion de la cola
        pthread_mutex_lock(&mutex_cola);
        while (queue_empty(cola_circular)) // si la cola está vacia, esperamos a que se inserte alguna operacion (señal que recibe del cajero)
        {  
            if (!quedan_operaciones_por_insertar) {
                // no se van a insertar mas operaciones y todas han sido procesadas, terminar ejecucion del thread
                pthread_mutex_unlock(&mutex_cola);
                pthread_exit(0);
            }
            pthread_cond_wait(&cond_cola_no_vacia, &mutex_cola);
        }
        elem = queue_get(cola_circular);    // se hace pop de la cola circular (elimina elemento)
        pthread_cond_signal(&cond_cola_no_llena);   // mandamos señal al cajero de que hay espacio en la cola
        pthread_mutex_unlock(&mutex_cola);
        my_bank_numop = elem->numop;
        
        // consultamos y modificamos bank_numop de forma segura
        pthread_mutex_lock(&mutex_bank_numop);
        while (my_bank_numop != bank_numop) // el trabajador comprueba si es su turno
        {   // esperamos a que otro trabajador haya terminado su operacion para ver si es nuestro turno (conserva orden)
            pthread_cond_wait(&cond_bank_numop, &mutex_bank_numop); 
        }

        // procesar operacion
        if (procesar_operacion(elem) < 0){   // si la operacion es erronea, terminar ejecucion del thread
            pthread_mutex_unlock(&mutex_bank_numop);
            pthread_exit(0);
        }
        else{   // si la operacion es correcta, aumentar el numero de operaciones procesadas por los trabajadores y mandar señal a los trabajadores
            bank_numop++;
            pthread_cond_broadcast(&cond_bank_numop);
        }
        
        // imprimir resultado de la operacion
        if(elem->tipo_op == TRASPASAR){ 
            printf("%d %s SALDO=%d TOTAL=%d\n", my_bank_numop+1, elem->str, saldo_cuenta[elem->cuenta_destino], global_balance);
        }
        else{
            printf("%d %s SALDO=%d TOTAL=%d\n", my_bank_numop+1, elem->str, saldo_cuenta[elem->cuenta_origen], global_balance);
        }
        pthread_mutex_unlock(&mutex_bank_numop);
    }
}


int comprobar_n_operaciones(char *vec) {
    /*
    Se comprueba que el numero de operaciones no supera el maximo de 200 y
    que el numero de operaciones del fichero coincide con el que pone en la cabecera.
    */

    int n = 0;          // contador de operaciones del fichero
    int i;              // indice del bucle while (para recorrer el fichero)
    int n_op = 0;       // n_op es el numero de operaciones en la cabecera del fichero
    int dig[3] = {-1,-1,-1};  // array que almacena los digitos del num de op de la cabecera
                              // dig[1] es las centenas cuando hay 3 digitos, las decenas cuando hay 2 y las unidades cuando hay 1
                              // dig [2] es las decenas cuando hay 3 digitos las unidades cuando hay 2
                              // dig [3] es las unidades cuando hay 3 digitos

    // obtenemos el numero de operaciones de la cabecera del fichero (n_op)
    for (i = 0; i < 3; i++) {
        if ((atoi(&vec[i]) == 0 && strcmp(&vec[i],"0")!=0) == 0) {
            // comprobamos si el char i es un numero
            dig[i] = atoi(&vec[i]);
        }
    }
    for (i = 0; i < 3; i++) {
        // transformamos dig a un entero: n_op de cabecera
        if (dig[i] != -1) {
            n_op = 10*n_op + dig[i];
        }
    }

    // contar el numero de operaciones del fichero (n)
    i=0;
    while (vec[i] != '\0') {        // leer chars de fichero
        if (vec[i] == '\n') {       // contar numero de operaciones (= numero de lineas)
            n++;
        }
        i++;
    }
    n--;                           // restamos 1 porque la ultima linea no es una operacion

    // comprobar que el numero de operaciones no supera el maximo de 200
    if (n>200 || n_op > MAX_OPERACIONES) {
        printf("Error: numero de operaciones mayor que 200");
        return -1;
    }
    // comprobar que el numero de operaciones del fichero concuerda con el de la cabecera
    if (n == n_op) {
        return n;
    } 
    else {
        printf("Error: el numero de operaciones de la cabecera no coincide con el numero real de operaciones en el fichero.\n");
        return -1;
    }
}

int check_arguments(int argc, char * argv[]){
    /*
    Checks everything is ok with the arguments of main and returns 1 if so, 0 otherwise
    */
    if (argc != 6) {
        printf("Usage: ./bank <nombre fichero> <num cajeros> <num trabajadores> <max cuentas> <tam buff>");
        return 0;
    }
    if (atoi(argv[2]) < 1) {
        printf("Error: numero de cajeros debe ser mayor que 0");
        return 0;
    }
    if (atoi(argv[3]) < 1) {
        printf("Error: numero de trabajadores debe ser mayor que 0");
        return 0;
    }
    if (atoi(argv[4]) < 1) {
        printf("Error: numero maximo de cuentas debe ser mayor que 0");
        return 0;
    }
    if (atoi(argv[5]) < 1) {
        printf("Error: tamaño del buffer circular debe ser mayor que 0");
        return 0;
    }
    return 1;
}

char * project_file(char *filename) {
    /*
    Projects the file into memory and returns a pointer to the first element (vector de chars)
    */
    int fd;
    if ((fd=open(filename, O_RDONLY)) < 0) {        // abrir fichero
        perror("open");
        return NULL;
    }

    struct stat dstat;
    fstat(fd, &dstat);
    char *vec;
    vec = mmap (NULL, dstat.st_size, PROT_READ, MAP_PRIVATE, fd, 0);    // proyectar fichero en memoria
    
    if (close(fd) < 0) {    // cerrar fichero
        perror("close");
        return NULL;
    }
    return vec;
}

char ** get_list_client_ops(char *vec, int n_op) {
    /*
    Returns a list of strings with the operations of each client
    */
    char **list_client_ops = malloc(n_op*sizeof(char*));    // reservar memoria para la lista de punteros a chars
    int i = 0; // indice de vec
    int j = 0; // indice de list_client_ops
    int k = 0; // indice de inicio de la operacion
    
    // salta la primera linea, ya que es el número de operaciones totales
    while (vec[i] != '\n') {
        i++;
    }
    
    i++;    // saltar el char "\n"
    k = i;
    // recorrerse el vector y guardar en list_client_ops cada operacion
    while (vec[i] != '\0') {
        if (vec[i] == '\n') {
            list_client_ops[j] = malloc((i-k+1)*sizeof(char));  // reservar memoria para la operacion
            strncpy(list_client_ops[j], &vec[k], i-k);          // copiar la operacion en la lista
            list_client_ops[j][i-k] = '\0';                     // añadir el caracter de fin de string
            k = i+1;                                            // actualizar el indice de inicio de la operacion
            j++;                                                // actualizar el indice de la lista
        }
        i++;
    }
    return list_client_ops;
}


element get_elem(char* op, int numop){
    /*
    Funcion que crea una estructura element a partir de una operacion (str) y un numero de operacion.
    */
    element elem;
    elem.str = op;
    // seleccionar tipo de operacion
    if (op[0]=='C'){
        elem.tipo_op = CREAR;
    }
    else if (op[0]=='I'){
        elem.tipo_op = INGRESAR;
    }
    else if (op[0]=='R'){
        elem.tipo_op = RETIRAR;
    }
    else if (op[0]=='S'){
        elem.tipo_op = SALDO;
    }
    else if (op[0]=='T'){
        elem.tipo_op = TRASPASAR;
    }
    // extraer argumentos (enteros): cantidad, cuenta_origen, cuenta_destino
    // orden del string "op": (OPERACION ARG1 ARG2 ARG3)
    int args[3]= {-1,-1,-1};
    int i = 0;
    int j = 0;
    int k = 0;
    // saltarse la operacion
    while (op[i]!=' '){
        i++;
    }
    i++;    // saltarse el espacio
    k = i;
    // recorrerse el vector, guardando los argumentos en el vector args
    while (op[i]!='\0'){
        if (op[i]==' '){
            args[j] = atoi(&op[k]);
            j++;
            k = i+1;
        }
        i++;
    }
    args[j] = atoi(&op[k]);             // guardar el ultimo argumento
    
    // asignar valores a los atributos a la estructura element
    switch (elem.tipo_op){
        case CREAR:                     // estructura: CREAR cuenta_origen
            elem.cuenta_origen = args[0];
            elem.cantidad = -1;
            elem.cuenta_destino = -1;
            break;
        case INGRESAR:                  // estructura: INGRESAR cuenta_origen cantidad
            elem.cuenta_origen = args[0];
            elem.cantidad = args[1];
            elem.cuenta_destino = -1;
            break;
        case RETIRAR:                   // estructura: RETIRAR cuenta_origen cantidad
            elem.cuenta_origen = args[0];
            elem.cantidad = args[1];
            elem.cuenta_destino = -1;
            break;
        case SALDO:                     // estructura: SALDO cuenta_origen
            elem.cuenta_origen = args[0];
            elem.cantidad = -1;
            elem.cuenta_destino = -1;
            break;
        case TRASPASAR:                 // estructura: TRASPASAR cuenta_origen cuenta_destino cantidad
            elem.cuenta_origen = args[0];
            elem.cuenta_destino = args[1];
            elem.cantidad = args[2];
            break;
    }
    elem.numop = numop;                 // sirve para organizar a los trabajadores (ejecutan operaciones en orden)

    return elem;
}

int procesar_operacion(element* elem){
    /*
    Funcion que selecciona la operacion y llama a la funcion que la realiza.
    Devuelve 0 en caso correcto y -1 si ha habido algun error.
    */
    int res = 0;
    switch (elem->tipo_op){
        case CREAR:
            res = crear_cuenta(elem->cuenta_origen);
            break;
        case INGRESAR:
            res = ingresar(elem->cuenta_origen, elem->cantidad);
            break;
        case RETIRAR:
            res = retirar(elem->cuenta_origen, elem->cantidad);
            break;
        case SALDO:
            res = saldo(elem->cuenta_origen);
            break;
        case TRASPASAR:
            res = traspasar(elem->cuenta_origen, elem->cuenta_destino, elem->cantidad);
            break;
    }
    return res;
}

int traspasar(int cuenta_origen, int cuenta_destino, int cantidad){
    /*
    Funcion que traspasa una cantidad de una cuenta a otra.
    Devuelve 0 en caso correcto y -1 si ha habido algun error.
    */
    int res = 0;
    if (cuenta_origen < 0 || cuenta_origen > MAX_CUENTAS || saldo_cuenta[cuenta_origen] == -__INT32_MAX__){
        res = -1;
    }
    else if(cuenta_destino < 0 || cuenta_destino > MAX_CUENTAS || saldo_cuenta[cuenta_destino] == -__INT32_MAX__){
        res = -1;
    }
    else if(cuenta_origen == cuenta_destino){
        res = -1;
    }
    else if(cantidad < 0){
        res = -1;
    }
    else{
        saldo_cuenta[cuenta_origen] -= cantidad;
        saldo_cuenta[cuenta_destino] += cantidad;
    }
    return res;
}

int crear_cuenta(int cuenta_origen){
    /*
    Funcion que crea una cuenta (inicializa a 0 el saldo).
    Devuelve 0 en caso correcto y -1 si ha habido algun error.
    */
    int res = 0;
    if (cuenta_origen < 0 || cuenta_origen > MAX_CUENTAS){
        res = -1;
    }
    else{
        saldo_cuenta[cuenta_origen] = 0;
    }
    return res;
}

int ingresar(int cuenta_origen, int cantidad){
    /*
    Funcion que ingresa una cantidad en una cuenta. 
    Devuelve 0 en caso correcto y -1 si ha habido algun error.
    */
    int res = 0;
    if (cuenta_origen < 0 || cuenta_origen > MAX_CUENTAS || saldo_cuenta[cuenta_origen] == -__INT32_MAX__){
        res = -1;
    }
    else{
        saldo_cuenta[cuenta_origen] += cantidad;
    }
    global_balance += cantidad;
    return res;
}

int retirar(int cuenta_origen, int cantidad){
    /*
    Funcion que retira una cantidad de una cuenta.
    Devuelve 0 en caso correcto y -1 si ha habido algun error.
    */
    int res = 0;
    if (cuenta_origen < 0 || cuenta_origen > MAX_CUENTAS || saldo_cuenta[cuenta_origen] == -__INT32_MAX__){
        res = -1;
    }
    else{
        saldo_cuenta[cuenta_origen] -= cantidad;
    }
    global_balance -= cantidad;
    return res;
}

int saldo(int cuenta_origen){
    /*
    Funcion que devuelve el saldo de una cuenta.
    Devuelve 0 en caso correcto y -1 si ha habido algun error.
    */
    int res = 0;
    if (cuenta_origen < 0 || cuenta_origen > MAX_CUENTAS || saldo_cuenta[cuenta_origen] == -__INT32_MAX__){
        res = -1;
    }
    return res;
}   
