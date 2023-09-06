#ifndef HEADER_FILE
#define HEADER_FILE


# define CREAR 0
# define INGRESAR 1
# define RETIRAR 2
# define SALDO 3
# define TRASPASAR 4


typedef struct element {
	/*Node of the queue*/
	char * str; // tipo de operacion: {CREAR, INGRESAR, RETIRAR, SALDO, TRASPASAR}
	int tipo_op; // tipo de operacion: {CREAR, INGRESAR, RETIRAR, SALDO, TRASPASAR}
	int cuenta_origen; // indice de la cuenta origen
	int cuenta_destino; // solo se usa en el caso de que la operacion sea TRASPASAR
						// en ese caso, cuenta_traspaso es el indice de la cuenta destino
	int cantidad; // cantidad de dinero a ingresar, retirar o traspasar
	int numop; // numero de operacion
	
	struct element *next;
}element;

typedef struct queue {
	/* Cola de operaciones*/
	element *head;
	element *tail;
	int max_size;
	int size;
}queue;

queue* queue_init (int size);
int queue_destroy (queue *q);
int queue_put (queue *q, struct element* elem);
struct element *queue_get(queue *q);
int queue_empty (queue *q);
int queue_full(queue *q);
#endif
