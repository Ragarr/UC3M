/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "rpc_claves.h"
#include <stdio.h>
#include <pthread.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define V2_MIN 1
#define V1_MAX 255
#define V2_MAX 32

struct element
{
	int key;
	char *value1;
	int N_value2;
	double *V_value2;
};

struct element *elements;
int N_elements = 0;

// diseño para el uso concurrente de la tabla de elementos
pthread_mutex_t mutex_elements = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_elements = PTHREAD_COND_INITIALIZER;

bool_t
init_1_svc(int *result, struct svc_req *rqstp)
{
	bool_t retval = FALSE;
	printf("[init]\n");

	if (N_elements == 0)
	{
		printf("Already initialized\n");
		// lock the elements array
		pthread_mutex_lock(&mutex_elements);
		elements = (struct element *)malloc(sizeof(struct element));
		pthread_mutex_unlock(&mutex_elements);
		if (elements == NULL)
		{
			perror("Error allocating memory");
			*result = -1;
			retval = TRUE;
			return retval;
		}
		*result = 0;
		retval = TRUE;
		return retval;
	}
	pthread_mutex_lock(&mutex_elements);
	printf("Initializing...\n");
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
		*result = -1;
		return retval;
	}

	retval = TRUE;
	*result = 0;
	return retval;
}

bool_t
set_value_1_svc(tuple_t tuple, int *result, struct svc_req *rqstp)
{
	bool_t retval = FALSE;
	printf("[set_value]\n");
	for (int i = 0; i < N_elements; i++)
	{
		if (elements[i].key == tuple.key)
		{
			// key already exists
			*result = -1;
			retval = TRUE;
			return retval;
		}
	}

	if (tuple.N_value2 < V2_MIN || tuple.N_value2 > V2_MAX || strlen(tuple.value1) > V1_MAX)
	{
		*result = -1;
		retval = TRUE;
		return retval;
	}

	struct element new_element;
	new_element.key = tuple.key;
	new_element.value1 = (char *)malloc(strlen(tuple.value1) + 1);
	if (new_element.value1 == NULL)
	{
		perror("Error allocating memory");
		*result = -1;
		retval = TRUE;
		return retval;
	}
	strcpy(new_element.value1, tuple.value1);
	new_element.N_value2 = tuple.N_value2;
	new_element.V_value2 = (double *)malloc(tuple.N_value2 * sizeof(double));
	if (new_element.V_value2 == NULL)
	{
		perror("Error allocating memory");
		*result = -1;
		retval = TRUE;
		return retval;
	}
	memcpy(new_element.V_value2, tuple.V_value2.V_value2_val, tuple.N_value2 * sizeof(double));

	pthread_mutex_lock(&mutex_elements);
	elements = (struct element *)realloc(elements, (N_elements + 1) * sizeof(struct element));
	if (elements == NULL)
	{
		pthread_mutex_unlock(&mutex_elements);
		perror("Error allocating memory");
		*result = -1;
		retval = TRUE;
		return retval;
	}
	elements[N_elements] = new_element;
	N_elements++;
	pthread_mutex_unlock(&mutex_elements);
	
	*result = 0;
	retval = TRUE;
	return retval;
}

bool_t
get_value_1_svc(int key, returnGetValue *result, struct svc_req *rqstp)
{
	printf("[get_value] %d\n", key);
	printf("N_elements: %d\n", N_elements);

	for (int i = 0; i < N_elements; i++)
    {
		printf("Element: %d\n", elements[i].key);
        if (elements[i].key == key)
        {
			printf("Element found: %d\n", key);
			result->result = 0;
			result->tuple_result.key = elements[i].key;
			result->tuple_result.value1 = (char *)malloc(strlen(elements[i].value1) + 1);
			if (result->tuple_result.value1 == NULL)
			{
				perror("Error allocating memory");
				result->result = -1;
				return TRUE;
			}
			strcpy(result->tuple_result.value1, elements[i].value1);
			result->tuple_result.N_value2 = elements[i].N_value2;
			result->tuple_result.V_value2.V_value2_len = elements[i].N_value2;
			result->tuple_result.V_value2.V_value2_val = (double *)malloc(elements[i].N_value2 * sizeof(double));
			if (result->tuple_result.V_value2.V_value2_val == NULL)
			{
				perror("Error allocating memory");
				result->result = -1;
				return TRUE;
			}
			memcpy(result->tuple_result.V_value2.V_value2_val, elements[i].V_value2, elements[i].N_value2 * sizeof(double));
           
			printf("Element found: %d\n", key);
			printf("%s, len: %ld\n", result->tuple_result.value1, strlen(result->tuple_result.value1));
			printf("%d\n", result->tuple_result.N_value2);
			for (int j = 0; j < result->tuple_result.N_value2; j++)
			{
				printf("%f ", result->tuple_result.V_value2.V_value2_val[j]);
			}
			printf("\n");

			return TRUE;
        }
    }
	
	// si no se inicializa el resultado, durante el marshalling
	// se produce un sigsegv 
	result->result = -1;
	result ->tuple_result.key = -1;
	result->tuple_result.value1 = NULL;
	result->tuple_result.N_value2 = -1;
	result->tuple_result.V_value2.V_value2_len = -1;
	result->tuple_result.V_value2.V_value2_val = NULL;
	
	return TRUE;
}

bool_t
modify_value_1_svc(tuple_t tuple, int *result, struct svc_req *rqstp)
{
	bool_t retval = FALSE;
	printf("[modify_value]\n");
	for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == tuple.key)
        {
            pthread_mutex_lock(&mutex_elements);
            elements[i].N_value2 = tuple.N_value2;
            free(elements[i].value1);
            free(elements[i].V_value2);
            elements[i].value1 = (char *)malloc(strlen(tuple.value1) + 1);
            if (elements[i].value1 == NULL)
            {
                perror("Error allocating memory");
                pthread_mutex_unlock(&mutex_elements);
                *result = -1;
				retval = TRUE;
				return retval;
            }
            strcpy(elements[i].value1, tuple.value1);
            elements[i].V_value2 = (double *)malloc(tuple.N_value2 * sizeof(double));
            if (elements[i].V_value2 == NULL)
            {
                perror("Error allocating memory");
                pthread_mutex_unlock(&mutex_elements);
                *result = -1;
				retval = TRUE;
				return retval;
            }
            memcpy(elements[i].V_value2, tuple.V_value2.V_value2_val, tuple.N_value2 * sizeof(double));
            pthread_mutex_unlock(&mutex_elements);
			*result = 0;
			retval = TRUE;
			return retval;
        }
    }
	*result = -1;
	retval = TRUE;
	return retval;
}

bool_t
delete_key_1_svc(int key, int *result, struct svc_req *rqstp)
{
	bool_t retval;
	printf("[delete_key]\n");
	retval = FALSE;

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
            *result = 0;
			retval = TRUE;
			return retval;
        }
    }
	*result = -1;
	retval = TRUE;
	return retval;
}

bool_t
exist_1_svc(int key, int *result, struct svc_req *rqstp)
{
	bool_t retval = FALSE;
	printf("[exist]\n");

	for (int i = 0; i < N_elements; i++)
    {
        if (elements[i].key == key)
        {
            *result = 1;
			retval = TRUE;
			return retval;
        }
    }
    result = 0;
	retval = TRUE;
	return retval;
}

int clave_prog_1_freeresult(SVCXPRT *transp, xdrproc_t xdr_result, caddr_t result)
{
	xdr_free(xdr_result, result);

	/*
	 * Insert additional freeing code here, if needed
	 */

	return 1;
}
