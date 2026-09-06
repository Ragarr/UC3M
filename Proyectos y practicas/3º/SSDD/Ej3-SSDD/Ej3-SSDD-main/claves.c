/*
 * Esta libreria llama a las funciones de la libreria rpc_claves.h
 * y se encarga de inicializar el cliente.
 */

#include "rpc_claves.h"
#include "claves.h"

CLIENT* clnt = NULL;



/*
struct tuple_t {
	int key;
	char *value1;
	int N_value2;
	struct {
		u_int V_value2_len;
		double *V_value2_val;
	} V_value2;
};
typedef struct tuple_t tuple_t;


struct returnGetValue {
	int result;
	tuple_t tuple_result;
};
*/

int init_clnt()
{
	if (clnt == NULL)
	{	// se obtiene el host del entorno para conservar la interfaz especificada en el enunciado
		char *host = getenv("IP_TUPLAS");
		clnt = clnt_create(host, CLAVE_PROG, CLAVE_VERS, "tcp");
		if (clnt == NULL)
		{
			clnt_pcreateerror(host);
			return -1;
		}
	}
	return 0;
}

int init()
{
	if (init_clnt() == -1) { return -1; }
	enum clnt_stat retval_1;
	int result_1;
	retval_1 = init_1(&result_1, clnt);
	if (retval_1 != RPC_SUCCESS)
	{
		// vamos a no printear los errores para 
		// que el rpc sea transparente al usuario
		// clnt_perror(clnt, "call failed");
		return -1;
	}
	return result_1;
}

int set_value(int key, char *value1, int N_value2, double *V_value2){
	if (init_clnt() == -1) { return -1; }
	enum clnt_stat retval_1;
	int result_1;
	tuple_t tuple;
	tuple.key = key;
	tuple.value1 = value1;
	tuple.N_value2 = N_value2; // este valor es innecesario devido a que V_value2.V_value2_len se genera solo al usar el tipo de dato array
	tuple.V_value2.V_value2_len = N_value2; // esto se genera automaticamente por rpcgen al usar el tipo de dato array
	tuple.V_value2.V_value2_val = V_value2;
	retval_1 = set_value_1(tuple, &result_1, clnt);
	if (retval_1 != RPC_SUCCESS)
	{
		// clnt_perror(clnt, "call failed");
		return -1;
	}
	return result_1;
}

int get_value(int key, char *value1, int *N_value2, double *V_value2){
	if (init_clnt() == -1) { return -1; }
	enum clnt_stat retval_1;
	int result_1 ;
	returnGetValue output;
	output.tuple_result.value1 = malloc(255);
	output.tuple_result.V_value2.V_value2_val = malloc(255 * sizeof(double));
	retval_1 = get_value_1(key, &output, clnt);
	if (retval_1 != RPC_SUCCESS)
	{
		// clnt_perror(clnt, "call failed");
		return -1;
	}
	for (int i = 0; i < output.tuple_result.N_value2; i++)
	{
		printf("%f ", output.tuple_result.V_value2.V_value2_val[i]);
	}
	printf("\n");
	
	// copiar a los punteros de salida
	strcpy(value1, output.tuple_result.value1);
	*N_value2 = output.tuple_result.N_value2;
	memcpy(V_value2, output.tuple_result.V_value2.V_value2_val, output.tuple_result.N_value2 * sizeof(double));

	return result_1;
}

int modify_value(int key, char *value1, int N_value2, double *V_value2){
	if (init_clnt() == -1) { return -1; }
	enum clnt_stat retval;
	int result;

	tuple_t tuple;
	tuple.key = key;
	tuple.value1 = malloc(strlen(value1) + 1);
	strcpy(tuple.value1, value1);
	tuple.N_value2 = N_value2;
	tuple.V_value2.V_value2_len = N_value2;
	tuple.V_value2.V_value2_val = malloc(N_value2 * sizeof(double));
	memcpy(tuple.V_value2.V_value2_val, V_value2, N_value2 * sizeof(double));
	

	retval = modify_value_1(tuple, &result, clnt);
	if (retval != RPC_SUCCESS)
	{
		// clnt_perror(clnt, "call failed");
		return -1;
	}
	return result;
}

int delete_key(int key){
	if (init_clnt() == -1) { return -1; }
	enum clnt_stat retval_1;
	int result_1;
	retval_1 = delete_key_1(key, &result_1, clnt);
	if (retval_1 != RPC_SUCCESS)
	{
		// clnt_perror(clnt, "call failed");
		return -1;
	}
	return result_1;
}

int exist(int key){
	if (init_clnt() == -1) { return -1; }
	enum clnt_stat retval_1;
	int result_1;
	retval_1 = exist_1(key, &result_1, clnt);
	if (retval_1 != RPC_SUCCESS)
	{
		// clnt_perror(clnt, "call failed");
		return -1;
	}
	return result_1;
}

/* ESTA FUNCION NO SE IMPLEMENTA PARA NO MODIFICAR LA INTERFAZ DE LA LIBRERIA
// Y CONSERVARLA TAL Y COMO SE PIDE EN EL ENUNCIADO

int end_clnt()
{
	if (clnt != NULL)
	{
		clnt_destroy(clnt);
		clnt = NULL;
	}
	return 0;
}
*/