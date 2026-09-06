//SSOO-P3 2022-2023

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include "queue.h"



//To create a queue
queue * queue_init(int size){
	queue * q = (queue *)malloc(sizeof(queue));
	q->head = NULL;
	q->tail = NULL;
	q->max_size = size;
	q->size = 0;
	return q;
}


// To Enqueue an element
int queue_put(queue *q, element *x) {
	if (q->size == q->max_size+1) {
		// cola llena
		return -1;
	}
	element *elem = (element *)malloc(sizeof(element)); // reservar memoria para el elemento
	memcpy(elem, x, sizeof(element));	// copiar el elemento en la memoria reservada
	elem->next = NULL;
	if (q->head == NULL) {	// si la cola está vacía
		// el elemento es el primero
		q->head = elem;
		q->tail = elem;
	} else {	// si la cola no está vacía
		// el elemento es el último
		q->tail->next = elem;
		q->tail = elem;
	}
	q->size++;	// se aumenta el tamaño de la cola
	return 0;
}


// To Dequeue an element.
struct element *queue_get(queue *q) {
	// localizar el elemento a extraer
	// guardar una copia del elemento
	// liberar el elemento
	// devolver la copia
	if (q->head == NULL) {
		return NULL;
	}
	element *elem = (element *)malloc(sizeof(element));	// reservar memoria para el elemento
	memcpy(elem, q->head, sizeof(element)); // copiar el elemento en la memoria reservada
	element *aux = q->head;
	q->head = q->head->next;
	free(aux);	// liberar el elemento
	q->size--;	// se reduce el tamaño de la cola
	return elem;
}


//To check queue state
int queue_empty(queue *q){
	if (q->head == NULL) {
		return 1;
	}
	return 0;
}

int queue_full(queue *q){
	if (q->size == q->max_size+1) {
		// cola llena
		return 1;
	}
	// cola no llena;
	return 0;
}

//To destroy the queue and free the resources
int queue_destroy(queue *q){
	if (q->head == NULL) {
		free(q);
		return 0;
	}
	element *aux;
	while (q->head != NULL) {
		aux = q->head;
		q->head = q->head->next;
		free(aux);
	}
	free(q);
	return 0;
}
