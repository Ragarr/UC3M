typedef int  t_vector_int<>;
typedef char t_vector_char<>;

program VECTOR {
        version VECTORVER {
                int setInt(t_vector_int v) = 1;
		int setChat(t_vector_char v) =2;
        } = 1;
} = 99;

