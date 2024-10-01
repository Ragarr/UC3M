

struct lista {
	int x;
	lista *next;
};

typedef lista *t_lista;

program LISTA {
        version LISTAVER {
                int sumar(t_lista l) = 1;
        } = 1;
} = 99;

