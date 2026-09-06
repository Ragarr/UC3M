struct tuple_t {
    int key;
    string value1<256>;
    int N_value2; /*Es innecesario pero vamos a conservarlo por mantener la interfaz del enunciado*/
    double V_value2<32>;
};

struct returnGetValue{
    int result;
    tuple_t tuple_result;
};

/* Definición del programa */
program CLAVE_PROG {
    version CLAVE_VERS {
        int INIT(void) = 1; /* Numero de procedimiento*/
        int SET_VALUE(tuple_t tuple) = 2;
        returnGetValue GET_VALUE(int key) = 3;
        int MODIFY_VALUE(tuple_t tuple) = 4;
        int DELETE_KEY(int key) = 5;
        int EXIST(int key) = 6;
    } = 1; /*Numero de version */
} = 1; /* Numero de programa*/