#include <mqueue.h>
#include <pthread.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>

// COMUNICATION STRUCTS:
struct request
{
    int queue_id;        // id of the client queue to send the response
    int op;              //  0: init, 1: set_value, 2: get_value, 3: modify_value, 4: delete_key, 5: exist
    int key;             // key of the element
    char value1[255];    // FIXME make size variable
    int N_value2;        // size of the vector V_value2
    double V_value2[31]; // FIXME make size variable
};
struct response
{
    char value1[255]; // FIXME make size variable
    int N_value2;
    double V_value2[31]; // FIXME make size variable
    int error;
};

// INTERNAL STRUCTS:
struct element
{
    int key;
    char *value1;
    int N_value2;
    double *V_value2;
};

// CONSTANTS:
#define SERVER_QUEUE "/SERVER_QUEUE_100472050"
#define CLIENT_QUEUE_START "/CLIENT_QUEUE_100472050_" // + QUEUE_ID
#define INIT 0
#define SET_VALUE 1
#define GET_VALUE 2
#define MODIFY_VALUE 3
#define DELETE_KEY 4
#define EXIST 5

#define V2_MIN 1
#define V1_MAX 255
#define V2_MAX 32

// INTERNAL FUNCTIONS PROTOTYPES:
int send_response(struct response *res, int queue_id);
void init_server_queue();
mqd_t open_client_queue(int queue_id);
void kill_handler(int signum);
void *server_thread(void *arg);

// PUBLIC FUNCTIONS PROTOTYPES:
// the "server_" is not necessary, but ill include it to make it clear
// that these functions are not the ones implemented in claves.c
void server_init(struct request *req);
void server_set_value(struct request *req);
void server_get_value(struct request *req);
void server_modify_value(struct request *req);
void server_delete_key(struct request *req);
void server_exist(struct request *req);
void server_invalid_op(struct request *req);

// INTERNAL GLOBAL VARIABLES:
// for thread management
pthread_mutex_t mutex_req_queue;
int req_not_copied = true;
pthread_cond_t cond_req;
mqd_t req_queue;

// mutex for elements array
pthread_mutex_t mutex_elements;
pthread_cond_t cond_elements;


// for element management
struct element *elements;
int N_elements = 0;

int main()
{
    signal(SIGINT, kill_handler);
    signal(SIGTERM, kill_handler);

    init_server_queue();

    // init mutex
    pthread_mutex_init(&mutex_req_queue, NULL);
    pthread_cond_init(&cond_req, NULL);
    pthread_mutex_init(&mutex_elements, NULL);
    pthread_cond_init(&cond_elements, NULL);

    // configure the threads
    pthread_attr_t t_attr;
    pthread_t thid;
    pthread_attr_init(&t_attr);
    pthread_attr_setdetachstate(&t_attr, PTHREAD_CREATE_DETACHED);

    struct request req;

    // printf("Server started...\n");
    while (1)
    {
        if (mq_receive(req_queue, (char *)&req, sizeof(struct request), 0) < 0)
        {
            perror("mq_receive");
            exit(-1);
        }

        if (pthread_create(&thid, &t_attr, server_thread, (void *)&req) == 0)
        {
            pthread_mutex_lock(&mutex_req_queue);
            while (req_not_copied)
            {
                pthread_cond_wait(&cond_req, &mutex_req_queue);
            }
            req_not_copied = true;
            pthread_mutex_unlock(&mutex_req_queue);
        }
        else
        {
            perror("Error creating thread");
        }
    }
    return 0;
}

// INTERNAL FUNCTIONS IMPLEMENTATIONS:
void *server_thread(void *arg)
{
    // copy the request
    struct request req;
    pthread_mutex_lock(&mutex_req_queue);
    memcpy(&req, arg, sizeof(struct request));
    req_not_copied = false;
    pthread_cond_signal(&cond_req);
    pthread_mutex_unlock(&mutex_req_queue);
    switch (req.op)
    {
    case INIT:
        server_init(&req);
        break;
    case SET_VALUE:
        server_set_value(&req);
        break;
    case GET_VALUE:
        server_get_value(&req);
        break;
    case MODIFY_VALUE:
        server_modify_value(&req);
        break;
    case DELETE_KEY:
        server_delete_key(&req);
        break;
    case EXIST:
        server_exist(&req);
        break;
    default:
        server_invalid_op(&req);
        break;
    }
    pthread_exit(NULL); // this is not necessary, but it is a good practice to include it
}

void kill_handler(int signum)
{
    if (signum != SIGINT && signum != SIGTERM)
    {
        return;
    }
    // printf("Exiting...\n");
    mq_close(req_queue);
    mq_unlink(SERVER_QUEUE);
    exit(0);
}
void init_server_queue()
{
    struct mq_attr attr;
    attr.mq_maxmsg = 10;
    // creo que lo de abajo puede dar problemas al ser el request de tamaño variable (por el V_value2)
    attr.mq_msgsize = sizeof(struct request);

    req_queue = mq_open(SERVER_QUEUE, O_CREAT | O_RDONLY, 0644, &attr);
    if (req_queue == -1)
    {
        perror("Error creating server queue");
        exit(-1);
    }
}

mqd_t open_client_queue(int queue_id)
{
    char client_queue_name[100];
    sprintf(client_queue_name, "%s%d", CLIENT_QUEUE_START, queue_id);
    mqd_t client_queue = mq_open(client_queue_name, O_WRONLY);
    return client_queue;
}

int send_response(struct response *res, int queue_id)
{
    mqd_t client_queue = open_client_queue(queue_id);
    if (client_queue == -1)
    {
        perror("Error opening client queue");
        return -1;
    }
    if (mq_send(client_queue, (char *)res, sizeof(struct response), 0) == -1)
    {
        perror("Error sending response");
        return -1;
    }
    mq_close(client_queue);
    return 0;
}

// "PUBLIC" FUNCTIONS IMPLEMENTATIONS:

void server_init(struct request *req)
{
    // printf("init\n");
    struct response res;
    // THERE ARE NO ELEMENTS IN THE SERVER
    if (N_elements == 0)
    {
        // lock the elements array
        pthread_mutex_lock(&mutex_elements);
        elements = (struct element *)malloc(sizeof(struct element));
        pthread_mutex_unlock(&mutex_elements);
        if (elements == NULL)
        {
            perror("Error allocating memory");
            res.error = -1;
            send_response(&res, req->queue_id);
            return;
        }
        // printf("init done\n");
        res.error = 0;
        send_response(&res, req->queue_id);
        return;
    }
    // IF THERE ARE ELEMENTS IN THE SERVER -> DELETE THEM AND FREE MEMORY
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
        res.error = -1;
        send_response(&res, req->queue_id);
        return;
    }
    res.error = 0;
    send_response(&res, req->queue_id);
    // printf("init done\n");
}

void server_set_value(struct request *req)
{
    struct response res;
    // printf("set_value\n");
    //  check if the key already exists
    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == req->key)
        {
            res.error = -1;
            send_response(&res, req->queue_id);
            // printf("key already exists\n");
            return;
        }
    }

    // check if the value2 size is valid
    if (req->N_value2 < V2_MIN || req->N_value2 > V2_MAX)
    {
        res.error = -1;
        send_response(&res, req->queue_id);
        return;
    }

    // create the new element
    struct element new_element;
    new_element.key = req->key;
    new_element.value1 = malloc(strlen(req->value1) + 1);

    if (new_element.value1 == NULL)
    {
        perror("Error allocating memory");
        res.error = -1;
        send_response(&res, req->queue_id);
        return;
    }
    strcpy(new_element.value1, req->value1);
    new_element.N_value2 = req->N_value2;
    new_element.V_value2 = malloc(req->N_value2 * sizeof(double));
    if (new_element.V_value2 == NULL)
    {
        perror("Error allocating memory");
        free(new_element.value1);
        res.error = -1;
        send_response(&res, req->queue_id);
        return;
    }
    memcpy(new_element.V_value2, req->V_value2, req->N_value2 * sizeof(double));

    // add the new element to the elements array
    pthread_mutex_lock(&mutex_elements);
    elements = (struct element *)realloc(elements, (N_elements + 1) * sizeof(struct element));
    if (elements == NULL)
    {
        perror("Error reallocating memory");
        free(new_element.value1);
        free(new_element.V_value2);
        res.error = -1;
        send_response(&res, req->queue_id);
        return;
    }
    elements[N_elements] = new_element;
    N_elements++;
    pthread_mutex_unlock(&mutex_elements);

    res.error = 0;
    send_response(&res, req->queue_id);
    // printf("added new element: {key: %d, value1: %s, N_value2: %d, V_value2: ", new_element.key, new_element.value1, new_element.N_value2);
    for (int i = 0; i < new_element.N_value2; i++)
    {
        // printf("%f ", new_element.V_value2[i]);
    }
    // printf("}\n");

    return;
}

void server_get_value(struct request *req)
{
    struct response res;
    // printf("get_value\n");
    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == req->key)
        {
            strcpy(res.value1, elements[i].value1);
            res.N_value2 = elements[i].N_value2;
            memcpy(res.V_value2, elements[i].V_value2, elements[i].N_value2 * sizeof(double));
            res.error = 0;
            send_response(&res, req->queue_id);
            return;
        }
    }
    res.error = -1;
    send_response(&res, req->queue_id);
    // printf("element with key %d not found\n", req->key);
}

void server_modify_value(struct request *req)
{
    struct response res;
    // printf("modify_value\n");
    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == req->key)
        {
            pthread_mutex_lock(&mutex_elements);
            // Liberar la memoria previamente asignada para value1 y V_value2 -> los valores cambiaran de tamaño
            free(elements[i].value1);
            free(elements[i].V_value2);

            // Asignar memoria para value1
            elements[i].value1 = malloc(strlen(req->value1) + 1);
            if (elements[i].value1 == NULL)
            {
                perror("Error allocating memory");
                res.error = -1;
                send_response(&res, req->queue_id);
                return;
            }
            // Copiar el valor de value1
            strcpy(elements[i].value1, req->value1);

            // Asignar memoria para V_value2 en funcion del nuevo N_value2
            elements[i].N_value2 = req->N_value2;
            elements[i].V_value2 = malloc(req->N_value2 * sizeof(double));
            if (elements[i].V_value2 == NULL)
            {
                perror("Error allocating memory");
                free(elements[i].value1);
                res.error = -1;
                send_response(&res, req->queue_id);
                return;
            }

            // Copiar el valor de V_value2
            memcpy(elements[i].V_value2, req->V_value2, req->N_value2 * sizeof(double));
            pthread_mutex_unlock(&mutex_elements);
            // Enviar la respuesta de exito
            res.error = 0;
            send_response(&res, req->queue_id);
            // printf("modified element: {key: %d, value1: %s, N_value2: %d, V_value2: ", elements[i].key, elements[i].value1, elements[i].N_value2);
            for (int j = 0; j < elements[i].N_value2; j++)
            {
                // printf("%f ", elements[i].V_value2[j]);
            }
            // printf("}\n");
            return;
        }
    }
    res.error = -1;
    send_response(&res, req->queue_id);
    // printf("element with key %d not found\n", req->key);
}

void server_delete_key(struct request *req)
{
    struct response res;
    // printf("delete_key\n");
    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == req->key)
        {
            pthread_mutex_lock(&mutex_elements);
            free(elements[i].value1);
            free(elements[i].V_value2);
            for (int j = i; j < N_elements - 1; j++)
            {
                elements[j] = elements[j + 1];
            }
            N_elements--;
            if (N_elements == 0)
            {
                free(elements);
                elements = NULL;
            }
            else
            {
                elements = (struct element *)realloc(elements, N_elements * sizeof(struct element));
                if (elements == NULL)
                {
                    perror("Error reallocating memory");
                    res.error = -1;
                    send_response(&res, req->queue_id);
                    return;
                }
            }
            pthread_mutex_unlock(&mutex_elements);
            res.error = 0;
            send_response(&res, req->queue_id);
            // printf("deleted element with key %d\n", req->key);
            return;
        }
    }
    res.error = -1;
    send_response(&res, req->queue_id);
    // printf("element with key %d not found\n", req->key);
}

void server_exist(struct request *req)
{
    struct response res;
    // printf("exist\n");
    for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == req->key)
        {
            res.error = 1;
            send_response(&res, req->queue_id);
            // printf("element with key %d exists\n", req->key);
            return;
        }
    }
    res.error = 0;
    send_response(&res, req->queue_id);
    // printf("element with key %d does not exist\n", req->key);
}

// por como es la implementacion de la libreria del cliente, nunca deberia darse este caso, pero por si acaso :D
void server_invalid_op(struct request *req)
{

    struct response res;
    res.error = -1;
    send_response(&res, req->queue_id);
}
