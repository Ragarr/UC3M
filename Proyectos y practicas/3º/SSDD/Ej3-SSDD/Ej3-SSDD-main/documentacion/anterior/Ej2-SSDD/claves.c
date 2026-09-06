#define _POSIX_C_SOURCE 200112L // for the timespec struct and mq_timedreceive
#include "claves.h"
#include <stdio.h>
#include <netdb.h>
#include <strings.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <stdlib.h>

#define INIT 0
#define SET_VALUE 1
#define GET_VALUE 2
#define MODIFY_VALUE 3
#define DELETE_KEY 4
#define EXIST 5
#define COPY 6

#define TIMEOUT 5

int sendMessage(int socket, char *buffer, int len)
{
    int r;
    int l = len;

    do
    {
        r = write(socket, buffer, l);
        l = l - r;
        buffer = buffer + r;
    } while ((l > 0) && (r >= 0));

    if (r < 0)
        return (-1); /* fail */
    else
        return (0); /* full length has been sent */
}

int recvMessage(int socket, char *buffer, int len)
{
    int r;
    int l = len;

    do
    {
        r = read(socket, buffer, l);
        l = l - r;
        buffer = buffer + r;
    } while ((l > 0) && (r >= 0));

    if (r < 0)
        return (-1); /* fallo */
    else
        return (0); /* full length has been receive */
}

int init_communication()
{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)
    {
        return -1;
    }

    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    char *server_hostname = getenv("IP_TUPLAS");
    if (server_hostname == NULL)
    {
        perror("Error: IP_TUPLAS not set\n");
        return -1;
    }

    struct hostent *hp = gethostbyname(server_hostname);
    if (hp == NULL)
    {
        perror("Error: Host not found\n");
        return -1;
    }

    char *server_port = getenv("PORT_TUPLAS");
    if (server_port == NULL)
    {
        perror("Error: PORT_TUPLAS not set\n");
        return -1;
    }

    serv_addr.sin_port = htons(atoi(server_port));
    memcpy(&serv_addr.sin_addr, hp->h_addr_list[0], hp->h_length);

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        return -1;
    }

    return sock;
}


/*
 * divide buffer en substrings separadas por espacios, devuelve un array de estos strings
 * los string entre comillas se consideran un solo string y se mantienen juntos
 * los strings vacios no se agregan al array
 * no hay ningun indicador de que el array terminó, se asume que se conoce la cantidad de elementos
 */
char **tokenize_response(char *buffer, int *n_args)
{
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
    *n_args = i;
    return arguments;
}

int communicate(int sock, char *msg)
{
    // add \r\n\r\n at the end of the message
    char _msg[1024];
    bzero(_msg, 1024);
    strcat(_msg, msg);
    strcat(_msg, "\r\n\r\n");
    if (sendMessage(sock, _msg, strlen(_msg)) < 0)
    {
        return -1;
    }
    char *response = (char *)malloc(2); 
    bzero(response, 2);
    read(sock, response, 2);
    int result = atoi(response);
    return result;
}


int init()
{
    int sock = init_communication();
    if (sock < 0)
    {
        return -1;
    }

    char msg[2];
    sprintf(msg, "%d", INIT);
    int result = communicate(sock, msg);
    return result;
}

int set_value(int key, char *value1, int N_value2, double *V_value2)
{
    int sock = init_communication();
    if (sock < 0)
    {
        return -1;
    }

    char *msg = (char *)malloc(1024);
    sprintf(msg, "%d %d \"%s\" %d ", SET_VALUE, key, value1, N_value2);
    char aux[32] = "";
    for(int i = 0; i < N_value2; i++){
        sprintf(aux, "%f ", V_value2[i]);
        strcat(msg, aux);
    }
    int result = communicate(sock, msg);
    free(msg);
    return result;
}

int get_value(int key, char *value1, int *N_value2, double *V_value2)
{
    // (void)value1; // elimina el warning de value1 no utilizado
    int sock = init_communication();
    if (sock < 0)
    {
        return -1;
    }

    char *msg = (char *)malloc(1024);
    sprintf(msg, "%d %d", GET_VALUE, key);
    strcat(msg, "\r\n\r\n");
    int result = send(sock, msg, strlen(msg), 0);
    if (result < 0)
    {
        free(msg);
        return result;
    }

    int resp_buffer_size = 512;
    char *resp_buffer = (char *)malloc(resp_buffer_size);
    int buffer_used = 0;
    bzero(resp_buffer, resp_buffer_size);
    while(1){
        int n = read(sock, resp_buffer + buffer_used, resp_buffer_size - buffer_used);
        if (n < 0){
            perror("Error reading from socket");
            free(resp_buffer);
            return -1;
        }
        else if (n == 0){
            break;
        }
        buffer_used += n;
        if (buffer_used >=4 && strcmp(resp_buffer + buffer_used - 4, "\r\n\r\n") == 0){
            break;
        }

        // resize buffer if needed
        if (buffer_used == resp_buffer_size){
            resp_buffer_size *= 2;
            resp_buffer = (char *)realloc(resp_buffer, resp_buffer_size);
        }
    }
    char* response = resp_buffer;
    // remove the \r\n\r\n at the end of the response
    bzero(response + buffer_used - 4, 4);
    int n_args = 0;
    // tokenize the response with spaces
    char **arguments = tokenize_response(response, &n_args); 
    if (strcmp(arguments[0], "-1") == 0)
    {
        return -1;
    }
    strcpy(value1, arguments[1]);
    *N_value2 = atoi(arguments[2]);
    double value;
    for (int j = 0; j < *N_value2; j++)
    {
        value = atof(arguments[j + 3]);
        memcpy(&V_value2[j], &value, sizeof(double));
    }
    free(arguments);
    free(resp_buffer);
    free(msg);
    return 0;
}

int modify_value(int key, char *value1, int N_value2, double *V_value2)
{
    // check for errors
    if (value1 == NULL || V_value2 == NULL)
    {
        return -1;
    }
    if (N_value2 < 1 || N_value2 > 32)
    {
        return -1;
    }
    if (strlen(value1) > 255)
    {
        return -1;
    }
    char *msg = (char *)malloc(1024);
    sprintf(msg, "%d %d \"%s\" %d ", MODIFY_VALUE, key, value1, N_value2);
    char aux[32] = "";
    for(int i = 0; i < N_value2; i++){
        sprintf(aux, "%f ", V_value2[i]);
        strcat(msg, aux);
    }
    int sock = init_communication();
    if (sock < 0)
    {
        return -1;
    }
    int result = communicate(sock, msg);
    return result;
}

int delete_key(int key)
{
    char *msg = malloc(128);
    sprintf(msg, "%d %d", DELETE_KEY, key);
    int sock = init_communication();
    if (sock < 0)
    {
        return -1;
    }
    int result = communicate(sock, msg);
    return result;
}

int exist(int key){
    char *msg = malloc(128);
    sprintf(msg, "%d %d", EXIST, key);
    int sock = init_communication();
    if (sock < 0)
    {
        return -1;
    }
    int result = communicate(sock, msg);
    return result;
}

int copy_key(int key1, int key2){
        char *msg = malloc(128);
    sprintf(msg, "%d %d %d", COPY, key1, key2);
    int sock = init_communication();
    if (sock < 0)
    {
        return -1;
    }
    int result = communicate(sock, msg);
    return result;
}


/*
INPUT: set 1 ejemplo 2 1.0 2.0 Message sent: 1 1 "ejemplo" 2 1.000000 2.000000 


*/