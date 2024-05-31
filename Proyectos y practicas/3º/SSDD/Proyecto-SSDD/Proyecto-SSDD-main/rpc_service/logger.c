#include "rpc_logger.h"
#include "logger.h"
#include <stdio.h>

CLIENT* clnt = NULL;

int init_clnt()
{
	if (clnt == NULL)
	{	// se obtiene el host del entorno para conservar la interfaz especificada en el enunciado
		char *host = getenv("LOGGER_HOST");
		if (host == NULL)
		{
			printf("No se ha especificado el host del servidor\n");
			return -1;
		}

		clnt = clnt_create(host, LOGGER_PROG, LOGGER_VERS, "tcp");
		if (clnt == NULL)
		{
			clnt_pcreateerror(host);
			return -1;
		}
	}
	return 0;
}

int log_msg(char *message) {
    if (init_clnt() == -1)
    {
		printf("Error al inicializar el cliente de logger rpc\n");
        return -1;
    }
    enum clnt_stat retval = log_1(message, NULL,clnt);
    if (retval != RPC_SUCCESS)
    {
		printf("Error al llamar a la función remota de logger rpc\n");
        clnt_perror(clnt, "call failed");
        return -1;
    }
	return 0;
}