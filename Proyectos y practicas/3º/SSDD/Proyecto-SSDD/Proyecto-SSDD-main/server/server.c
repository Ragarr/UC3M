#include <stdio.h>
#include <unistd.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <stdbool.h>
#include <ifaddrs.h> // getifaddrs para obtener la ip de la maquina y poder imprimirla al principio
#include <stdint.h>
#include <math.h>
#include "logger.h"

// PROTOTYPES
// Funcion que maneja la conexion con el cliente
void *handle_client(void *arg);

// Funcion que parsea los argumentos de la linea de comandos -> devuelve el puerto
int parseArgs(int argc, char *argv[]);
// Funcion que obtiene la ip del servidor
char *getServerIP();
// Funcion que lee un mensaje del cliente
char *readMsgFromClient(int client_sock);

// funcion para convertir un entero en un string de longitud variable
char *intToString(int n);


// funciones de la aplicacion
uint8_t registerUser(char *user);
uint8_t unregisterUser(char *user);
uint8_t connectUser(char *user, char *port, char *ip);
uint8_t disconnectUser(char *user);
uint8_t publishFile(char *user, char *fileName, char *description);
uint8_t deleteFile(char *user, char *fileName);
uint8_t listUsers(char* user, int* n_users, char**** users);
uint8_t listContent(char* user, char* userToSearch, int* n_files, char**** files);

// TYPE DEFINITIONS
typedef struct User
{
    char *name;
    bool isConected;
    char ip[INET_ADDRSTRLEN];
    int port;
} User;

typedef struct SharedFile
{
    char *name;        // MAX 256
    char *description; // MAX 256
    char *seeder;
} SharedFile;

// Constants
#define MAX_CLIENTS 16
#define MAX_NAME_SIZE 256
#define BUFFER_INIT_SIZE 256
#define FILE_NAME_MAX_SIZE 256
#define FILE_DESCRIPTION_MAX_SIZE 256

// GLOBAL VARIABLES
// Mutex and condition variable to synchronize the request copying
pthread_mutex_t request_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t request_cond = PTHREAD_COND_INITIALIZER;
bool request_not_copied = true;

// Clients
User *clients;
int clients_count = 0;
pthread_mutex_t clients_mutex = PTHREAD_MUTEX_INITIALIZER;

// Shared files
SharedFile *sharedFiles;
int sharedFiles_count = 0;
pthread_mutex_t sharedFiles_mutex = PTHREAD_MUTEX_INITIALIZER;


// IMPLEMENTATION
int main(int argc, char *argv[])
{
    // Se ejecutar´a de la siguiente manera:
    //  $ ./ server -p < port >
    int port = parseArgs(argc, argv);

    // Crear e inicializar el socket del servidor
    int server_sock, client_sock;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    if ((server_sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }
    // set the socket as reusable
    setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, &(int){1}, sizeof(int));
    // set the server address
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port);

    // bind the socket to the server address
    if (bind(server_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0)
    {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // listen for incoming connections
    if (listen(server_sock, MAX_CLIENTS) < 0)
    {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    // prepare multithreading -> bajo demanda
    pthread_t thid;
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

    char *serverIP = getServerIP();

    printf("s > init server %s:%d\n", serverIP, port);

    printf("s > ");
    fflush(stdout);
    for (;;)
    {
        // accept a new connection
        if ((client_sock = accept(server_sock, (struct sockaddr *)&client_addr, &client_len)) < 0)
        {
            perror("Accept failed");
            exit(EXIT_FAILURE);
        }
        // create a new thread to handle the client
        if (pthread_create(&thid, &attr, handle_client, (void *)&client_sock) != 0)
        {
            perror("Thread creation failed");
            exit(EXIT_FAILURE);
        }
        // let the thread copy the request // MAYBE NOT NEEDED
        pthread_mutex_lock(&request_mutex);
        while (request_not_copied)
        {
            pthread_cond_wait(&request_cond, &request_mutex);
        }
        request_not_copied = true;
        pthread_mutex_unlock(&request_mutex);
        pthread_detach(thid);
        printf("s > ");
    }
    return 0;
}

void *handle_client(void *arg)
{
    // copy the request
    pthread_mutex_lock(&request_mutex);
    int client_sock = *(int *)arg;
    request_not_copied = false;
    pthread_cond_signal(&request_cond);
    pthread_mutex_unlock(&request_mutex);

    // we allways expect the operation and the user
    char *op = readMsgFromClient(client_sock);
    if (op == NULL)
    {
        printf("Error reading from client\n");
        return NULL;
    }
    char* datetime = readMsgFromClient(client_sock);
    if (datetime == NULL)
    {
        printf("Error reading from client\n");
        return NULL;
    }
    char *user = readMsgFromClient(client_sock);
    if (user == NULL)
    {
        printf("Error reading from client\n");
        return NULL;
    }
    // el log ahora se hace en el RPC PERO lo vamos a conservar por comodiad
    printf("\rs > %s FROM %s AT %s\n", op, user, datetime);

    char* msg = (char*)malloc(strlen(op) + strlen(user) + strlen(datetime) + 1);
    sprintf(msg, "%s %s %s", user, op, datetime);
    if (log_msg(msg) != 0)
    {
        printf("Error writing to log, petition will be processed anyways\n");
        
    }
    free(msg);
    // handle the request according to the operation
    if (strcmp(op, "REGISTER") == 0)
    {
        fflush(stdout);
        uint8_t result = registerUser(user);
        fflush(stdout);
        if (result != 0 && result != 1)
        {   // cualquier caso de error no contemplado
            result = 2;
        }
        write(client_sock, &result, 1);
        fflush(stdout);
        
    }
    else if (strcmp(op, "UNREGISTER") == 0)
    {
        uint8_t result = unregisterUser(user);
        if (result != 0 && result != 1)
        {   // cualquier caso de error no contemplado
            result = 2;
        }
        write(client_sock, &result, 1);
    }
    else if (strcmp(op, "CONNECT") == 0)
    {
        char *client_port_txt = readMsgFromClient(client_sock);
        if (client_port_txt == NULL)
        {
            printf("Error reading from client\n");
            return NULL;
        }
        // obtener la ip del socket del cliente
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        getpeername(client_sock, (struct sockaddr *)&client_addr, &client_len);
        char *client_ip = inet_ntoa(client_addr.sin_addr);
        // comprobar si es la direccion de loopback
        if (strcmp(client_ip, "127.0.0.1") == 0)
        {
            // obtener la ip del cliente a partir de la direccion de loopback
            client_ip = getServerIP();
        }
        uint8_t result = connectUser(user, client_port_txt, client_ip);
        if (result != 0 && result != 1 && result != 2)
        {   // cualquier caso de error no contemplado
            result = 3;
        }
        write(client_sock, &result, 1);
    }
    else if (strcmp(op, "DISCONNECT") == 0)
    {
        uint8_t result = disconnectUser(user);
        if (result != 0 && result != 1 && result != 2)
        {   // cualquier caso de error no contemplado
            result = 3;
        }
        write(client_sock, &result, 1);
    }
    else if(strcmp(op, "PUBLISH") == 0)
    {
        char *fileName = readMsgFromClient(client_sock);
        if (fileName == NULL)
        {
            printf("Error reading from client\n");
            return NULL;
        }
        char *description = readMsgFromClient(client_sock);
        // printf("description: %s\n", description);
        if (description == NULL)
        {
            printf("Error reading from client\n");
            return NULL;
        }
        uint8_t result = publishFile(user, fileName, description);
        if (result != 0 && result != 1 && result != 2 && result != 3)
        {   // cualquier caso de error no contemplado
            result = 4;
        }
        write(client_sock, &result, 1);
    }
    else if (strcmp(op, "DELETE") == 0)
    {
        char *fileName = readMsgFromClient(client_sock);
        if (fileName == NULL)
        {
            printf("Error reading from client\n");
            return NULL;
        }
        uint8_t result = deleteFile(user, fileName);
        if (result != 0 && result != 1 && result != 2 && result != 3 && result != 4)
        {   // cualquier caso de error no contemplado
            result = 5;
        }
        write(client_sock, &result, 1);
    }
    else if (strcmp(op, "LIST_USERS") == 0)
    {
        int n_users;
        char*** users;
        uint8_t result = listUsers(user, &n_users, &users);
        if (result != 0 && result != 1 && result != 2)
        {   // cualquier caso de error no contemplado
            result = 3;
        }
        write(client_sock, &result, 1);
        if (result == 0)
        {
            char* n_users_str = intToString(n_users);
            n_users_str = realloc(n_users_str, strlen(n_users_str) + 1);
            n_users_str[strlen(n_users_str)] = '\0';
            write(client_sock, n_users_str, strlen(n_users_str)+1);
            free(n_users_str);
            for (int i = 0; i < n_users; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    // escribir para cada usuario, su nombre, ip y puerto en ese orden
                    write(client_sock, users[i][j], strlen(users[i][j]) + 1);
                    
                }
            }            
        }
    }
    else if(strcmp(op, "LIST_CONTENT")==0){
        char* userToSearch = readMsgFromClient(client_sock);
        if(userToSearch == NULL){
            printf("Error reading from client\n");
            return NULL;
        }
        int n_files;
        char*** files;
        uint8_t result = listContent(user, userToSearch, &n_files, &files);
        if(result != 0 && result != 1 && result != 2 && result != 3)
        {
            result = 4;
        }
        if(result == 0){
            write(client_sock, &result, 1);
            char* n_files_str = intToString(n_files);
            n_files_str = realloc(n_files_str, strlen(n_files_str) + 1);
            n_files_str[strlen(n_files_str)] = '\0';
            write(client_sock, n_files_str, strlen(n_files_str)+1);
            free(n_files_str);
            for (int i = 0; i < n_files; i++)
            {
                for (int j = 0; j < 2; j++)
                {
                    // escribir para cada archivo, su nombre y descripcion en ese orden
                    write(client_sock, files[i][j], strlen(files[i][j]) + 1);
                }
            }
        }
        else{
            write(client_sock, &result, 1);
        }
        
    }
    else
    {
        printf("Invalid operation\n");
        write(client_sock, "Invalid operation", 3);
    }
    return NULL;
}

int parseArgs(int argc, char *argv[])
{
    int port = -1;
    if (argc != 3)
    {
        fprintf(stderr, "Uso: %s -p <puerto>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    if (strcmp(argv[1], "-p") != 0)
    {
        fprintf(stderr, "Uso: %s -p <puerto>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    port = atoi(argv[2]);
    if (port < 1024 || port > 65535)
    {
        fprintf(stderr, "El puerto debe estar entre 1024 y 65535\n");
        exit(EXIT_FAILURE);
    }
    return port;
}

char *getServerIP()
{
    // get the ip of the machine to print it at the beginning
    struct ifaddrs *ifAddrStruct = NULL;
    struct ifaddrs *ifa = NULL;
    void *tmpAddrPtr = NULL;
    getifaddrs(&ifAddrStruct);
    char *serverIP = NULL;
    for (ifa = ifAddrStruct; ifa != NULL; ifa = ifa->ifa_next)
    {
        if (!ifa->ifa_addr)
        {
            continue;
        }
        if (ifa->ifa_addr->sa_family == AF_INET)
        { // check it is IP4
            tmpAddrPtr = &((struct sockaddr_in *)ifa->ifa_addr)->sin_addr;
            serverIP = (char *)malloc(INET_ADDRSTRLEN);
            inet_ntop(AF_INET, tmpAddrPtr, serverIP, INET_ADDRSTRLEN);
            if (strcmp(ifa->ifa_name, "eth0") == 0)
            {
                break;
            }
            // also check for "wlan0" in case the server is running on a laptop
            if (strcmp(ifa->ifa_name, "wlan0") == 0)
            {
                break;
            }
        }
    }
    if (ifAddrStruct != NULL)
        freeifaddrs(ifAddrStruct);
    return serverIP;
}

char *readMsgFromClient(int client_sock)
{
    char *buffer = (char *)malloc(BUFFER_INIT_SIZE);
    int buffer_size = BUFFER_INIT_SIZE;
    int buffer_used = 0;
    int bytes_read;
    // memset(buffer, -1, buffer_size);
    while (true)
    {
        // if you dont read byte by byte dosent work, because we dont know the size of the message
        bytes_read = read(client_sock, buffer + buffer_used, 1);
        if (bytes_read < 0)
        {
            perror("Read failed");
            close(client_sock);
            free(buffer);
            return NULL;
        }
        if (bytes_read == 0)
        {
            // printf("Client disconnected\n");
            break; // nothing to read, try again
        }
        // if last byte is '\0', the request is complete
        if (buffer[buffer_used + bytes_read - 1] == '\0')
        {
            break;
        }
        // if the buffer is full, double its size
        buffer_used += bytes_read;
        if (buffer_used == buffer_size)
        {
            buffer_size *= 2;
            buffer = (char *)realloc(buffer, buffer_size);
        }
    }
    return buffer;
}

char *intToString(int n)
{
    if (n == 0)
    {
        char *zero = (char *)malloc(2);
        zero[0] = '0';
        zero[1] = '\0';
        return zero;
    }
    int digit_count = (int)log10(abs(n)) + 1;
    char *str = (char *)malloc(digit_count + 1);
    sprintf(str, "%d", n);
    return str;
} 


uint8_t registerUser(char *user)
{
    // 0 en caso de exito, 1 si el usuario ya esta registrado previamente, 2 en cualquier otro caso.
    // check if username is not empty
    if (strlen(user) == 0)
    {
        return 2;
    }
    // check if user is already registered
    pthread_mutex_lock(&clients_mutex);
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            pthread_mutex_unlock(&clients_mutex);
            return 1;
        }
    }
    clients = (User *)realloc(clients, (clients_count + 1) * sizeof(User));
    if (clients == NULL)
    {
        pthread_mutex_unlock(&clients_mutex);
        return 2;
    }
    clients[clients_count].name = user;
    clients[clients_count].isConected = false;
    clients[clients_count].port = -1;
    clients_count++;
    pthread_mutex_unlock(&clients_mutex);
    return 0;
}

uint8_t unregisterUser(char * user)
{
    pthread_mutex_lock(&clients_mutex);
    for (int i = 0; i < clients_count; i++)
    {
        if ((strcmp(clients[i].name, user) == 0))
        {
            if (clients[i].isConected)
            {
                pthread_mutex_unlock(&clients_mutex);
                return 2; // user is connected
            }
            free(clients[i].name);

            for (int j = i; j < clients_count - 1; j++)
            {
                clients[j] = clients[j + 1];
            }
            clients_count--;
            clients = (User *)realloc(clients, clients_count * sizeof(User));
            pthread_mutex_unlock(&clients_mutex);
            return 0;
        }
    }
    pthread_mutex_unlock(&clients_mutex);
    return 1;
}

uint8_t connectUser(char *user, char *port, char *ip)
{
    int port_int = atoi(port);
    if (port_int < 1024 || port_int > 65535)
    {
        return 3; // fail
    }
    pthread_mutex_lock(&clients_mutex);
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            if (clients[i].isConected)
            {
                pthread_mutex_unlock(&clients_mutex);
                return 2; // user already connected
            }
            clients[i].isConected = true;
            clients[i].port = port_int;
            strcpy(clients[i].ip, ip);
            pthread_mutex_unlock(&clients_mutex);
            return 0; // success
        }
    }
    pthread_mutex_unlock(&clients_mutex);
    return 1; // user not found
}

uint8_t disconnectUser(char *user)
{
    pthread_mutex_lock(&clients_mutex);
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            if (!clients[i].isConected)
            {
                pthread_mutex_unlock(&clients_mutex);
                return 2; // user already disconnected
            }
            clients[i].isConected = false;
            clients[i].port = -1;
            clients[i].ip[0] = '\0';
            pthread_mutex_unlock(&clients_mutex);
            return 0; // success

        }
    }
    pthread_mutex_unlock(&clients_mutex);
    return 1; // user not found
}

uint8_t publishFile(char *user, char *fileName, char *description)
{
    // check if user exists
    // check len of fileName and description (max 256)
    if (strlen(fileName) == 0 || strlen(description) == 0 || strlen(fileName) > FILE_NAME_MAX_SIZE || strlen(description) > FILE_DESCRIPTION_MAX_SIZE)
    {
        return 4; // fail
    }


    pthread_mutex_lock(&clients_mutex);
    bool userExists = false;
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            userExists = true;
            break;
        }
    }
    pthread_mutex_unlock(&clients_mutex);
    if (!userExists)
    {
        return 1; // user not found
    }
    // check if user is connected
    pthread_mutex_lock(&clients_mutex);
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            if (!clients[i].isConected)
            {
                pthread_mutex_unlock(&clients_mutex);
                return 2; // user not connected
            }
            break;
        }
    }
    pthread_mutex_unlock(&clients_mutex);


    // check if file is already published
    pthread_mutex_lock(&sharedFiles_mutex);
    for (int i = 0; i < sharedFiles_count; i++)
    {
        if (strcmp(sharedFiles[i].name, fileName) == 0)
        {
            pthread_mutex_unlock(&sharedFiles_mutex);
            return 3; // file already published
        }
    }
    sharedFiles = (SharedFile *)realloc(sharedFiles, (sharedFiles_count + 1) * sizeof(SharedFile));
    if (sharedFiles == NULL)
    {
        pthread_mutex_unlock(&sharedFiles_mutex);
        return 4; // fail
    }
    sharedFiles[sharedFiles_count].name = malloc(strlen(fileName) + 1);
    strcpy(sharedFiles[sharedFiles_count].name, fileName);
    sharedFiles[sharedFiles_count].description = malloc(strlen(description) + 1);
    strcpy(sharedFiles[sharedFiles_count].description, description);
    sharedFiles[sharedFiles_count].seeder = malloc(strlen(user) + 1);
    strcpy(sharedFiles[sharedFiles_count].seeder, user);
    sharedFiles_count++;
    pthread_mutex_unlock(&sharedFiles_mutex);

    return 0; // success
}

uint8_t deleteFile(char *user, char *fileName)
{
    // check if user exists
    pthread_mutex_lock(&clients_mutex);
    bool userExists = false;
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            userExists = true;
            break;
        }
    }
    pthread_mutex_unlock(&clients_mutex);
    if (!userExists)
    {
        return 1; // user not found
    }
    // check if user is connected
    pthread_mutex_lock(&clients_mutex);
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            if (!clients[i].isConected)
            {
                pthread_mutex_unlock(&clients_mutex);
                return 2; // user not connected
            }
            break;
        }
    }
    pthread_mutex_unlock(&clients_mutex);
    // check if file is published
    pthread_mutex_lock(&sharedFiles_mutex);
    for (int i = 0; i < sharedFiles_count; i++)
    {
        if (strcmp(sharedFiles[i].name, fileName) == 0)
        {
            if (strcmp(sharedFiles[i].seeder, user) != 0)
            {
                pthread_mutex_unlock(&sharedFiles_mutex);
                return 4; // user is not the seeder
            }
            free(sharedFiles[i].name);
            free(sharedFiles[i].description);
            for (int j = i; j < sharedFiles_count - 1; j++)
            {
                sharedFiles[j] = sharedFiles[j + 1];
            }
            sharedFiles_count--;
            sharedFiles = (SharedFile *)realloc(sharedFiles, sharedFiles_count * sizeof(SharedFile));
            pthread_mutex_unlock(&sharedFiles_mutex);
            return 0; // success
        }
    }
    pthread_mutex_unlock(&sharedFiles_mutex);

    return 3; // file not found
}

uint8_t listUsers(char *user, int* n_users, char**** users)
{
    // check if user exists
    pthread_mutex_lock(&clients_mutex);
    bool userExists = false;
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            userExists = true;
            break;
        }
    }
    pthread_mutex_unlock(&clients_mutex);
    if (!userExists)
    {
        return 1; // user not found
    }
    // check if user is connected
    pthread_mutex_lock(&clients_mutex);
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            if (!clients[i].isConected)
            {
                pthread_mutex_unlock(&clients_mutex);
                return 2; // user not connected
            }
            break;
        }
    }
    pthread_mutex_unlock(&clients_mutex);

    // list users
    pthread_mutex_lock(&clients_mutex);
    *n_users = 0;
   /*
    users -> [ user1 -> [ name  -> userName1
                          ip    -> userIp1
                          port  -> userPort1 ]
               user2 -> [ name  -> userName2
                          ip    -> userIp2
                          port  -> userPort2 ]
               ...
               userN -> [ name  -> userNameN
                          ip    -> userIpN
                          port  -> userPortN ] ]
    users es un char****, un puntero a un arreglo de char***.
    user1, user2, ..., userN son char***, cada uno es un puntero a un arreglo 
        de tres char** (name, ip, port).

    name, ip, port son char**, cada uno es un puntero a un arreglo de char* que contiene la cadena correspondiente (userName1, userIp1, userPort1, etc.).
   */
    *users = (char***)malloc(clients_count * sizeof(char**));
    for (int i = 0; i < clients_count; i++)
    {
        // check if is connected
        if (!clients[i].isConected)
        {
              continue;         
        }
        (*users)[*n_users] = (char**)malloc(3 * sizeof(char*)); // 3 strings por usuario
        (*users)[*n_users][0] = (char*)malloc(strlen(clients[i].name) + 1); // el nombre varia en longitud
        strcpy((*users)[*n_users][0], clients[i].name);
        (*users)[*n_users][1] = (char*)malloc(INET_ADDRSTRLEN); // la ip son 15 caracteres + '\0'
        strcpy((*users)[*n_users][1], clients[i].ip);
        (*users)[*n_users][2] = (char*)malloc(6); // el puerto son 5 caracteres + '\0'
        sprintf((*users)[*n_users][2], "%d", clients[i].port);
        (*n_users)++;
    }
    pthread_mutex_unlock(&clients_mutex);
    return 0; // success
}


uint8_t listContent(char * user, char * userToSearch, int * n_files, char**** files)
{
    // check if user exists
    pthread_mutex_lock(&clients_mutex);
    bool userExists = false;
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            userExists = true;
            break;
        }
    }
    pthread_mutex_unlock(&clients_mutex);
    if (!userExists)
    {
        return 1; // user not found
    }
    // check if user is connected
    pthread_mutex_lock(&clients_mutex);
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, user) == 0)
        {
            if (!clients[i].isConected)
            {
                pthread_mutex_unlock(&clients_mutex);
                return 2; // user not connected
            }
            break;
        }
    }
    pthread_mutex_unlock(&clients_mutex);
    
    // check if user to search exists
    pthread_mutex_lock(&clients_mutex);
    bool userToSearchExists = false;
    for (int i = 0; i < clients_count; i++)
    {
        if (strcmp(clients[i].name, userToSearch) == 0)
        {
            userToSearchExists = true;
            break;
        }
    }
    pthread_mutex_unlock(&clients_mutex);
    if (!userToSearchExists)
    {
        return 3; // user to search not found
    }

    // list files
    pthread_mutex_lock(&sharedFiles_mutex);
    *n_files = 0;
    *files = (char***)malloc(sharedFiles_count * sizeof(char**));

    for (int i = 0; i < sharedFiles_count; i++)
    {
        if (strcmp(sharedFiles[i].seeder, userToSearch) == 0) 
        {
            (*files)[*n_files] = (char**)malloc(2 * sizeof(char*)); // 2 strings por archivo
            (*files)[*n_files][0] = (char*)malloc(strlen(sharedFiles[i].name) + 1); // el nombre varia en longitud
            strcpy((*files)[*n_files][0], sharedFiles[i].name);
            (*files)[*n_files][1] = (char*)malloc(strlen(sharedFiles[i].description) + 1); // la descripcion varia en longitud
            strcpy((*files)[*n_files][1], sharedFiles[i].description);
            (*n_files)++;
        }
    }
    pthread_mutex_unlock(&sharedFiles_mutex);
    return 0; // success
}