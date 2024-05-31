"""
Autores: 
    - Raúl Aguilar Arroyo 100472050
    - Natalia Rodriguez Navarro 100471976
"""

import ply.yacc as yacc
from ajson_lexer import AJSONLexer
from pprint import pprint

class AJSONParser:

    tokens = AJSONLexer.tokens

    def __init__(self):
        self.parser = yacc.yacc(module=self)
        self.lexer = AJSONLexer().lexer

    """
    GRAMATICA:
    
    file -> object | lambda
    object -> {content}
    content -> KEY value | KEY value , content | lambda
    value -> object | expr | list | STRING | BOOL | NULL | NUMBER 
    expr -> NUMBER COMPARATOR NUMBER
    list -> L_SQ_BRACKET list_content R_SQ_BRACKET
    list_content -> object | object , list_content | lambda
    """

    def p_file(self, p):
        '''
        file : object
             | lambda
        '''
        if p[1] == None:
            # Caso de archivo vacío
            p[0] = {} 
        else:
            p[0] = p[1] 

    def p_lambda(self, p):
        '''
        lambda :
        '''
        pass

    def p_object(self, p):
        '''
        object : L_BRACKET content R_BRACKET
        '''
        p[0] = p[2]
    
    def p_content(self, p):
        '''
        content : KEY value
                | KEY value COMMA content
                | lambda
        '''
        if len(p) == 3:
            # Caso de un solo par clave-valor en el objeto
            p[0] = {p[1]: p[2]}
        elif len(p) == 5:
            # Caso de varios pares clave-valor en el objeto
            p[0] = {p[1]: p[2]}
            # Actualizar el diccionario con los pares restantes
            if p[4] != None:
                p[0].update(p[4])

    def p_value(self, p):
        '''
        value : object
              | expr
              | list
              | STRING
              | BOOL
              | NULL
              | NUMBER
        '''
        p[0] = p[1]

    def p_expr(self, p):
        '''
        expr : NUMBER COMPARATOR NUMBER
        '''
        # Evaluar la expresión y guardar el resultado
        if p[2] == "==":
            p[0] = p[1] == p[3]
        elif p[2] == "<=":
            p[0] = p[1] <= p[3]
        elif p[2] == ">=":
            p[0] = p[1] >= p[3]
        elif p[2] == "<":
            p[0] = p[1] < p[3]
        elif p[2] == ">":
            p[0] = p[1] > p[3]

    def p_list(self, p):
        '''
        list : L_SQ_BRACKET list_content R_SQ_BRACKET
        '''
        p[0] = p[2]

    def p_list_content(self, p):
        '''
        list_content : object
                     | object COMMA list_content
                     | lambda
        '''
        if len(p) == 2:
            # Caso de un solo objeto en la lista
            p[0] = [p[1]] 
        elif len(p) == 4:
            # Caso de varios objetos en la lista
            p[0] = [p[1]]
            # Agregar los objetos restantes a la lista
            if p[3] != None:
                p[0].extend(p[3])


    def imprimir_objeto(self, diccionario, prefijo=""):
        """
        Imprime un objeto de manera recursiva para mostrar su estructura
        tal y como se ejemplifica en el enunciado del proyecto
        """
        for clave, valor in diccionario.items():
            if isinstance(valor, dict):
                self.imprimir_objeto(valor, prefijo + clave + ".")
            else:
                if isinstance(valor, list):
                    self.imprimir_array(valor, prefijo + clave + ".")
                else:
                    print("{", prefijo + clave + ":", valor, "}")

    def imprimir_array(self, lista, prefijo):
        """
        Imprime el contenido de un array de manera recursiva para poder 
        mantener el formato especificado en el enunciado del proyecto
        """
        for i in range(len(lista)):
            if isinstance(lista[i], dict):
                self.imprimir_objeto(lista[i], prefijo + str(i) + ".")
            else: 
                # Caso de objetos vacios
                print("{", prefijo + str(i) + ":", lista[i], "}")
    
    
    def p_error(self, p):
        if p:
            print("[PARSER][ERROR] Syntax Error at line {0}: {1}".format(p.lineno, p.type))
        else:
            print("[PARSER][ERROR] Unexpected EoF")
        exit(1)

    
    def test(self, data):
        self.imprimir_objeto(self.parser.parse(data, lexer=self.lexer))