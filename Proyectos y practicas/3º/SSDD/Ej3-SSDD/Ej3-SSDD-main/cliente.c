#include "claves.h"
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char *functions[] = {"init", "set", "get", "modify", "delete", "exist"};
    printf("CLIENTE\n");

    if (argc != 2)
    {
        printf("Usage: %s <commands_file>\n", argv[0]);
        return -1;
    }

    FILE *script_file = fopen(argv[1], "r");
    if (script_file == NULL)
    {
        printf("Error opening script file: %s\n", argv[1]);
        return -1;
    }
    printf("SCRIPT FILE OPENED: %s\n", argv[1]);
    char line[1024];
    while (fgets(line, sizeof(line), script_file))
    {
        if (line[0] == '\n')
        {
            continue;
        }
        // ignorar comentarios de linea
        if (line[0] == '#')
        {
            printf("COMMENT: %s", line);
            continue;
        }
        char *token = strtok(line, " ");
        if (token == NULL)
        {
            continue;
        }
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
        // here we have the arguments in the array and the number of arguments in i
        // GET THE FUNCTION
        int function = -1;
        for (int j = 0; j < 7; j++)
        {
            if (strcmp(arguments[0], functions[j]) == 0)
            {
                function = j;
                break;
            }
        }
        if (function == -1)
        {
            printf("Invalid function: %s\n", arguments[0]);
            continue;
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

        // CALL THE FUNCTION
        int key;
        char *value1;
        int N_value2;
        double *V_value2;
        printf("INPUT: %s \n", arguments[0]);
        for (int j = 1; j < i; j++)
        {
            printf("%s ", arguments[j]);
        }

        switch (function)
        {
        case 0: // INIT
            if (i != 1)
            {
                printf("Invalid number of arguments for init\n");
                break;
            }
            printf("\n\tOUTPUT: %d\n", init());
            break;
        case 1: // SET
            // CHECK THERE ARE ENOUGH ARGUMENTS
            if (i < 5)
            {
                printf("Invalid number of arguments for set\n");
                break;
            }
            key = atoi(arguments[1]);
            value1 = arguments[2];
            N_value2 = atoi(arguments[3]);
            V_value2 = (double *)malloc(N_value2 * sizeof(double));
            for (int j = 0; j < N_value2; j++)
            {
                V_value2[j] = atof(arguments[4 + j]);
            }
            printf("\n\tOUTPUT: %d\n", set_value(key, value1, N_value2, V_value2));
            break;
        case 2: // GET
            // CHECK THERE ARE ENOUGH ARGUMENTS
            if (i != 2)
            {
                printf("Invalid number of arguments for get\n");
                break;
            }

            key = atoi(arguments[1]);
            value1 = (char *)malloc(256);
            N_value2 = 0;
            V_value2 = (double *)malloc(32 * sizeof(double));
            printf("\n\tOUTPUT: %d - ", get_value(key, value1, &N_value2, V_value2));
            printf("%s ", value1);
            for (int j = 0; j < N_value2; j++)
            {
                printf("%lf ", V_value2[j]);
            }
            printf("\n");
            break;
        case 3: // MODIFY
            // CHECK THERE ARE ENOUGH ARGUMENTS
            if (i < 5)
            {
                printf("Invalid number of arguments for modify\n");
                break;
            }

            key = atoi(arguments[1]);
            value1 = arguments[2];
            N_value2 = atoi(arguments[3]);
            V_value2 = (double *)malloc(N_value2 * sizeof(double));
            for (int j = 0; j < N_value2; j++)
            {
                V_value2[j] = atof(arguments[4 + j]);
            }
            printf("\n\tOUTPUT: %d\n", modify_value(key, value1, N_value2, V_value2));
            break;
        case 4: // DELETE
            // CHECK THERE ARE ENOUGH ARGUMENTS
            if (i != 2)
            {
                printf("Invalid number of arguments for delete\n");
                break;
            }
            key = atoi(arguments[1]);
            printf("\n\tOUTPUT: %d\n", delete_key(key));
            break;
        case 5: // EXIST
            // CHECK THERE ARE ENOUGH ARGUMENTSq
            if (i != 2)
            {
                printf("Invalid number of arguments for exist\n");
                break;
            }
            key = atoi(arguments[1]);
            printf("\n\tOUTPUT: %d\n", exist(key));
            break;
        }
        for (int j = 0; j < i; j++)
        {
            free(arguments[j]);
        }
        free(arguments);
    }
    printf("SCRIPT FILE ENDED\n");
    fclose(script_file);
    return 0;
}
