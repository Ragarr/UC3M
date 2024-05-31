#include <stdio.h>
#include <unistd.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

#define MAX_CLIENTS 10 // MAXIMO DE CLIENTES QUE PUEDEN ESTAR EN COLA

#define INIT 0
#define SET_VALUE 1
#define GET_VALUE 2
#define MODIFY_VALUE 3
#define DELETE_KEY 4
#define EXIST 5
#define COPY 6

#define V2_MIN 1
#define V1_MAX 255
#define V2_MAX 32

// INTERNAL STRUCTS:
struct element
{
    int key;
    char *value1;
    int N_value2;
    double *V_value2;
};

struct element *elements;
int N_elements = 0;

// mutex for elements array
pthread_mutex_t mutex_elements;
pthread_cond_t cond_elements;
int req_not_copied = 1;

// mutex for pending requests
pthread_mutex_t mutex_requests;
pthread_cond_t cond_requests;

// PROTOTIPOS DE FUNCIONES INTERNAS:
void *connection_handler(void *arg);
int send_msg_to_client(int socket, char *buffer, int len);

// PROTOTIPOS DE FUNCIONES PUBLICAS:
int server_init();
int server_set_value(int key, char *value1, int N_value2, double *V_value2);
int server_get_value(int key, char *value1, int *N_value2, double *V_value2);
int server_modify_value(int key, char *value1, int N_value2, double *V_value2);
int server_delete_key(int key);
int server_exist(int key);
int server_copy_key(int key1, int key2);

int main(int argc, char *argv[])
{
    // argv[1] == puerto
    if (argc != 2)
    {
        printf("Uso: %s <puerto>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    pthread_mutex_init(&mutex_elements, NULL);
    pthread_cond_init(&cond_elements, NULL);

    int port = atoi(argv[1]);
    if (port < 1024 || port > 49151)
    {
        printf("El puerto debe estar entre 1024 y 49151\n");
        exit(EXIT_FAILURE);
    }

    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

    // Crear socket del servidor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &(int){1}, sizeof(int));

    // Asignar valores a la estructura address
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    // Asignar puerto al socket
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // Escuchar en el socket
    if (listen(server_fd, MAX_CLIENTS) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    pthread_t thid;
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

    printf("Servidor escuchando en el puerto %d\n", port);
    while (1)
    {
        // Aceptar conexion
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0)
        {
            perror("accept");
            exit(EXIT_FAILURE);
        }
        printf("Connection accepted from %d\n", new_socket);
        int *new_socket_ptr = (int *)malloc(sizeof(int));
        *new_socket_ptr = new_socket;
        if (pthread_create(&thid, &attr, connection_handler, (void *)new_socket_ptr) == 0)
        {
            pthread_mutex_lock(&mutex_requests);
            while (req_not_copied)
            {
                pthread_cond_wait(&cond_requests, &mutex_requests);
            }
            req_not_copied = 1;
            pthread_mutex_unlock(&mutex_requests);
        }
        else
        {
            perror("Error creating thread");
            close(new_socket);
        }
        pthread_detach(thid);
        
    }
    return 0;
}

void *connection_handler(void *arg)
{
    pthread_mutex_lock(&mutex_requests);
    int client_socket = *((int *)arg);
    free(arg);
    req_not_copied = 0;
    pthread_cond_signal(&cond_requests);
    pthread_mutex_unlock(&mutex_requests);
    int buffer_size = 512;
    char* buffer = (char*)malloc(buffer_size);
    bzero(buffer, buffer_size);
    int buffer_used = 0;

    while(1){
        int n = read(client_socket, buffer + buffer_used, buffer_size - buffer_used);
        if(n < 0){
            perror("Error reading from socket");
            close(client_socket);
            free(buffer);
            return NULL;
        }else if(n == 0){
            printf("Connection closed by client %d\n", client_socket);
            close(client_socket);
            free(buffer);
            return NULL;

        }
        buffer_used += n;
        // check if the request is complete
        if (buffer_used>=4 && strcmp(buffer + buffer_used - 4, "\r\n\r\n") == 0){
            break;
        }

        // check if the buffer is full
        if(buffer_used == buffer_size){
            buffer_size *= 2;
            buffer = (char*)realloc(buffer, buffer_size);
        }
    }
    // remove the \r\n\r\n at the end of the request
    buffer[buffer_used - 4] = '\0';
    // evaluar la funcion solicitada
    char *token = strtok(buffer, " ");
    int i = 0;
    char **arguments = NULL;
    while (token != NULL)
    {
        // REMOVE NEWLINE AND SPACES
        if (token[strlen(token) - 1] == '\n')
        {
            token[strlen(token) - 1] = '\0';
        }
        if (token[0] == ' ')
        {
            token++;
        }
        if (token[strlen(token) - 1] == ' ')
        {
            token[strlen(token) - 1] = '\0';
        }
        if (strlen(token) == 0)
        {
            token = strtok(NULL, " ");
            continue;
        }
        // if the token starts with " join it with the next token until it ends with "
        if (token[0] == '"' && token[strlen(token) - 1] != '"')
        {
            char *aux = (char *)malloc(256);
            strcpy(aux, token);
            token = strtok(NULL, " ");
            while (token[strlen(token) - 1] != '"')
            {
                strcat(aux, " ");
                strcat(aux, token);
                token = strtok(NULL, " ");
            }
            strcat(aux, " ");
            strcat(aux, token);
            token = aux;
        }
        // ADD THE ARGUMENTS TO THE ARRAY
        arguments = (char **)realloc(arguments, (i + 1) * sizeof(char *));
        arguments[i] = (char *)malloc(strlen(token) + 1);
        strcpy(arguments[i], token);
        i++;
        token = strtok(NULL, " ");
    }

    // en caso de que exista value1 (argumento 2) y sea un string, se debe quitar las comillas
    if (i > 2 && arguments[2][0] == '"' && arguments[2][strlen(arguments[2]) - 1] == '"')
    {
        char *aux = (char *)malloc(256);
        strcpy(aux, arguments[2] + 1);
        aux[strlen(aux) - 1] = '\0';
        free(arguments[2]);
        arguments[2] = aux;
    }

    // here we have the arguments in the array and the number of arguments in i
    // GET THE FUNCTION
    int function = atoi(arguments[0]);
    
    int result = -1;
    int key, N_value2;
    char *value1;
    double *V_value2;
    char *response = (char *)malloc(2);

    // FOR DEBUG PURPOSES
    //char* functions[] = {"INIT", "SET_VALUE", "GET_VALUE", "MODIFY_VALUE", "DELETE_KEY", "EXIST", "COPY"};
    printf("request recived from %d: {", client_socket);
    for (int j = 0; j < i; j++)
    {
        printf("%s, ", arguments[j]);
    }
    printf("}\n");
    switch (function)
    {
    case INIT:
        result = server_init();
        sprintf(response, "%d", result);
        send_msg_to_client(client_socket, response, strlen(response));
        break;
    case SET_VALUE:
        key = atoi(arguments[1]);
        value1 = arguments[2];
        N_value2 = atoi(arguments[3]);
        V_value2 = (double *)malloc(N_value2 * sizeof(double));
        for (int j = 0; j < N_value2; j++)
        {
            V_value2[j] = atof(arguments[4 + j]);
        }
        result = server_set_value(key, value1, N_value2, V_value2);
        sprintf(response, "%d", result);
        send_msg_to_client(client_socket, response, strlen(response));
        break;
    case GET_VALUE:
        key = atoi(arguments[1]);
        int get_N_value2;
        char get_value1[255];
        double get_V_value2[32];
        int result = server_get_value(key, get_value1, &get_N_value2, get_V_value2);
        char *get_response = (char *)malloc(1024);
        bzero(get_response, 1024);
        sprintf(get_response, "%d %s %d", result, get_value1, get_N_value2);
        char *aux = (char *)malloc(32);
        for (int i = 0; i < get_N_value2; i++)
        {
            sprintf(aux, " %f", get_V_value2[i]);
            strcat(get_response, aux);
        }
        send_msg_to_client(client_socket, get_response, strlen(get_response));
        break;
    case MODIFY_VALUE:
        key = atoi(arguments[1]);
        value1 = arguments[2];
        N_value2 = atoi(arguments[3]);
        V_value2 = (double *)malloc(N_value2 * sizeof(double));
        for (int j = 0; j < N_value2; j++)
        {
            V_value2[j] = atof(arguments[4 + j]);
        }
        result = server_modify_value(key, value1, N_value2, V_value2);
        sprintf(response, "%d", result);
        send_msg_to_client(client_socket, response, strlen(response));
        break;
    case DELETE_KEY:
        key = atoi(arguments[1]);
        result = server_delete_key(key);
        sprintf(response, "%d", result);
        send_msg_to_client(client_socket, response, strlen(response));
        // print reponse sent to client <ip:port>
        
        break;
    case EXIST:
        key = atoi(arguments[1]);
        result = server_exist(key);
        sprintf(response, "%d", result);
        send_msg_to_client(client_socket, response, strlen(response));
        break;
    case COPY:
        key = atoi(arguments[1]);
        int key2 = atoi(arguments[2]);
        printf("copying key %d to key %d\n", key, key2);
        result = server_copy_key(key, key2);
        printf("result: %d\n", result);
        sprintf(response, "%d", result);
        send_msg_to_client(client_socket, response, strlen(response));
        break;
    default:
        send_msg_to_client(client_socket, "-1", 2);
        break;
    }
    // send the response
    close(client_socket);
    return NULL;
}

int server_init()
{
    if (N_elements == 0)
    {
        // lock the elements array
        pthread_mutex_lock(&mutex_elements);
        elements = (struct element *)malloc(sizeof(struct element));
        pthread_mutex_unlock(&mutex_elements);
        if (elements == NULL)
        {
            perror("Error allocating memory");
            return -1;
        }
        return 0;
    }
    pthread_mutex_lock(&mutex_elements);
    for (int i = 0; i < N_elements; i++)
    {
        free(elements[i].value1);
        free(elements[i].V_value2);
    }
    free(elements);
    N_elements = 0;
    elements = (struct element *)malloc(sizeof(struct element));
    pthread_mutex_unlock(&mutex_elements);
    if (elements == NULL)
    {
        perror("Error allocating memory");
        return -1;
    }
    return 0;
}

int server_set_value(int key, char *value1, int N_value2, double *V_value2)
{
    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == key)
        {
            // key already exists
            return -1;
        }
    }

    if (N_value2 < V2_MIN || N_value2 > V2_MAX || strlen(value1) > V1_MAX)
    {
        return -1;
    }

    struct element new_element;
    new_element.key = key;
    new_element.value1 = (char *)malloc(strlen(value1) + 1);
    if (new_element.value1 == NULL)
    {
        perror("Error allocating memory");
        return -1;
    }
    strcpy(new_element.value1, value1);
    new_element.N_value2 = N_value2;
    new_element.V_value2 = (double *)malloc(N_value2 * sizeof(double));
    if (new_element.V_value2 == NULL)
    {
        perror("Error allocating memory");
        return -1;
    }
    memcpy(new_element.V_value2, V_value2, N_value2 * sizeof(double));

    pthread_mutex_lock(&mutex_elements);
    elements = (struct element *)realloc(elements, (N_elements + 1) * sizeof(struct element));
    if (elements == NULL)
    {
        pthread_mutex_unlock(&mutex_elements);
        perror("Error allocating memory");
        return -1;
    }
    elements[N_elements] = new_element;
    N_elements++;
    pthread_mutex_unlock(&mutex_elements);
    return 0;
}

int server_get_value(int key, char *value1, int *N_value2, double *V_value2)
{
    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == key)
        {
            strcpy(value1, elements[i].value1);
            *N_value2 = elements[i].N_value2;
            memcpy(V_value2, elements[i].V_value2, elements[i].N_value2 * sizeof(double));
            return 0;
        }
    }
    return -1;
}

int server_modify_value(int key, char *value1, int N_value2, double *V_value2)
{
    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == key)
        {
            pthread_mutex_lock(&mutex_elements);
            elements[i].N_value2 = N_value2;
            free(elements[i].value1);
            free(elements[i].V_value2);
            elements[i].value1 = (char *)malloc(strlen(value1) + 1);
            if (elements[i].value1 == NULL)
            {
                perror("Error allocating memory");
                pthread_mutex_unlock(&mutex_elements);
                return -1;
            }
            strcpy(elements[i].value1, value1);
            elements[i].V_value2 = (double *)malloc(N_value2 * sizeof(double));
            if (elements[i].V_value2 == NULL)
            {
                perror("Error allocating memory");
                pthread_mutex_unlock(&mutex_elements);
                return -1;
            }
            memcpy(elements[i].V_value2, V_value2, N_value2 * sizeof(double));
            pthread_mutex_unlock(&mutex_elements);
            return 0;
        }
    }
    return -1;
}

int server_delete_key(int key)
{
    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == key)
        {
            pthread_mutex_lock(&mutex_elements);
            free(elements[i].value1);
            free(elements[i].V_value2);
            for (int j = i; j < N_elements - 1; j++)
            {
                elements[j] = elements[j + 1];
            }
            N_elements--;
            elements = (struct element *)realloc(elements, N_elements * sizeof(struct element));
            pthread_mutex_unlock(&mutex_elements);
            return 0;
        }
    }
    return -1;
}

int server_exist(int key)
{
    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == key)
        {
            return 1;
        }
    }
    return 0;
}

int server_copy_key(int key1, int key2)
{
    // localizar ambos elementos
    if (key1 == key2)
    {
        return -1;
    }
    struct element *element1 = NULL;
    struct element *element2 = NULL;
    // si bloqueamos despues puede que un elemento se elimine antes de copiarlo
    pthread_mutex_lock(&mutex_elements);

    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == key1)
        {
            element1 = &elements[i];
        }
        if (elements[i].key == key2)
        {
            element2 = &elements[i];
        }
    }
    if (element1 == NULL)
    {
        pthread_mutex_unlock(&mutex_elements);
        return -1;
    }
    if (element2 == NULL)
    { // si no existe la clave key2, se crea
        pthread_mutex_unlock(&mutex_elements);
        return server_set_value(key2, element1->value1, element1->N_value2, element1->V_value2);
    }
    // si existe se copia
    free(element2->value1);
    free(element2->V_value2);
    element2->value1 = (char *)malloc(strlen(element1->value1) + 1);
    if (element2->value1 == NULL)
    {
        perror("Error allocating memory");
        pthread_mutex_unlock(&mutex_elements);
        return -1;
    }
    strcpy(element2->value1, element1->value1);
    element2->N_value2 = element1->N_value2;
    element2->V_value2 = (double *)malloc(element1->N_value2 * sizeof(double));
    if (element2->V_value2 == NULL)
    {
        pthread_mutex_unlock(&mutex_elements);
        perror("Error allocating memory");
        return -1;
    }
    memcpy(element2->V_value2, element1->V_value2, element1->N_value2 * sizeof(double));
    pthread_mutex_unlock(&mutex_elements);
    return 0;
}

int send_msg_to_client(int socket, char *buffer, int len)
{
    // añadir \r\n\r\n al final del mensaje
    char _buffer[len + 4];
    bzero(_buffer, len + 4);
    strcat(_buffer, buffer);
    strcat(_buffer, "\r\n\r\n");
    if (send(socket, _buffer, strlen(_buffer), 0) < 0)
    {
        return -1;
    }
    printf("Message sent to client %d: %s\n", socket, buffer);
    return 0;
}