#define _POSIX_C_SOURCE 200112L // for the timespec struct and mq_timedreceive
#include <mqueue.h> 

#include "claves.h"
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>  // for the timeout

#define SERVER_QUEUE "/SERVER_QUEUE_100472050"
#define CLIENT_QUEUE_START "/CLIENT_QUEUE_100472050_" // + PID

#define INIT 0
#define SET_VALUE 1
#define GET_VALUE 2
#define MODIFY_VALUE 3
#define DELETE_KEY 4
#define EXIST 5

#define TIMEOUT 5

mqd_t client_queue = -1;

struct request
{
    int queue_id;     // id of the client queue to send the response
    int op;           //  0: init, 1: set_value, 2: get_value, 3: modify_value, 4: delete_key, 5: exist
    int key;          // key of the element
    char value1[255]; // FIXME make size variable
    int N_value2;     // size of the vector V_value2
    double V_value2[31]; // FIXME make size variable
};
struct response
{
    char value1[255]; // FIXME make size variable
    int N_value2;
    double V_value2[31]; // FIXME make size variable
    int error;
};
// INTERNAL FUNCTIONS:


// creates (if it dosent exist) and opens the client queue
int init_client_queue(){
    struct mq_attr attr;
    attr.mq_flags = 0;
    attr.mq_maxmsg = 10;
    attr.mq_msgsize = sizeof(struct response);
    attr.mq_curmsgs = 0;

    char client_queue_name[100];
    sprintf(client_queue_name, "%s%d", CLIENT_QUEUE_START, getpid());

    // printf("Initialized client queue: %s\n", client_queue_name);
    client_queue = mq_open(client_queue_name, O_CREAT | O_RDONLY, 0644, &attr);
    if(client_queue == -1){
        perror("Error creating client queue");
        return -1;
    }
    return 0;
}

// closes and unlinks the client queue
int close_n_unlink_client_queue(){
    char client_queue_name[100];
    // if queue is open, close it
    if (client_queue != -1){
        mq_close(client_queue);
        client_queue = -1;
    }

    sprintf(client_queue_name, "%s%d", CLIENT_QUEUE_START, getpid());
    int result = mq_unlink(client_queue_name);
    if (result == -1){
        perror("Error unlinking client queue");
        return -1;
    }
    return 0;
}

// send a request to the server and wait for the response in the client queue
struct response send_and_await_response(struct request req){
    struct  response res;
    // open the server queue
    mqd_t server_queue = mq_open(SERVER_QUEUE, O_WRONLY);
    if(server_queue < 0){
        perror("Error opening server queue, is the server running?");
        res.error = -1;
        return res;
    }
    // before sending the request, check if the client queue is initialized
    if (client_queue == -1){
        if (init_client_queue() == -1){
            res.error = -1;
            return res;
        }
    }
    // send the request
    req.queue_id = getpid();
    int send_result = mq_send(server_queue, (char*)&req, sizeof(struct request), 0); 
    mq_close(server_queue);
    if (send_result == -1){
        perror("Error sending message");
        res.error = -1;
        return res;
    }

    // wait for the response
    struct timespec timeout;
    clock_gettime(CLOCK_REALTIME, &timeout);
    timeout.tv_sec += TIMEOUT; 
    int result = mq_timedreceive(client_queue, (char*)&res, sizeof(struct response), NULL, &timeout);
    if (result == -1){
        perror("Error receiving message");
        res.error = -1;
    }
    if (close_n_unlink_client_queue() == -1){
        printf("[WARN] Error unlinking client queue\n");
    }
    return res;
}


// LIBRARY FUNCTIONS:

int init(){
    struct request req;
    req.queue_id = getpid();
    req.op = INIT;
    struct response res = send_and_await_response(req);
    return res.error;
}

int set_value(int key, char *value1, int N_value2, double *V_value2){
    
    if (value1 == NULL || V_value2 == NULL){
        return -1;
    }
    // check for errors
    if (N_value2 < 1 || N_value2 > 32){
        return -1;
    }
    if (strlen(value1) > 255){
        return -1;
    }

    struct request req;
    req.queue_id = getpid();
    req.op = SET_VALUE;
    req.key = key;
    strcpy(req.value1, value1);
    req.N_value2 = N_value2;
    memcpy(req.V_value2, V_value2, N_value2 * sizeof(double));
    struct response res = send_and_await_response(req);
    return res.error;
}

int get_value(int key, char *value1, int *N_value2, double *V_value2){
    // check for errors
    if (N_value2 == NULL || V_value2 == NULL || value1 == NULL ){
        return -1;
    }
    struct request req;
    req.queue_id = getpid();
    req.op = GET_VALUE;
    req.key = key;
    struct response res = send_and_await_response(req);
    if (res.error == -1){
        return -1;
    }
    strcpy(value1, res.value1);
    memcpy(N_value2, &res.N_value2, sizeof(int));
    memcpy(V_value2, res.V_value2, res.N_value2 * sizeof(double));
    return res.error;
}

int modify_value(int key, char *value1, int N_value2, double *V_value2){
    // check for errors
    if (value1 == NULL || V_value2 == NULL){
        return -1;
    }
    if (N_value2 < 1 || N_value2 > 32){
        return -1;
    }
    if (strlen(value1) > 255){
        return -1;
    }
    struct request req;
    req.queue_id = getpid();
    req.op = MODIFY_VALUE;
    req.key = key;
    strcpy(req.value1, value1);
    req.N_value2 = N_value2;
    memcpy(req.V_value2, V_value2, N_value2 * sizeof(double));
    struct response res = send_and_await_response(req);
    return res.error;
}

int delete_key(int key){
    
    struct request req;
    req.queue_id = getpid();
    req.op = DELETE_KEY;
    req.key = key;
    struct response res = send_and_await_response(req);
    return res.error;
}

int exist(int key){
    struct request req;
    req.queue_id = getpid();
    req.op = EXIST;
    req.key = key;
    struct response res = send_and_await_response(req);
    return res.error;
}