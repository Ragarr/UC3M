"""
Autores: 
    - Raúl Aguilar Arroyo 100472050
    - Natalia Rodriguez Navarro 100471976

Módulo que implementa el parser
"""
import ply.yacc as yacc
from .ajs_lexer import AJSLexer
from .Symbol import *
from .SymbolTable import SymbolTable





class AJSParser:
    tokens = AJSLexer.tokens
    
    def __init__(self) -> None:
        self.parser = yacc.yacc(module=self)
        self.lexer = AJSLexer().lexer
        self.st = SymbolTable()
        self.consider_if = False    
    """Gramatica:
    
    program: statement_list 

    statement_list: statement statement_list
                    | empty

    statement: expression SEMICOLON
                | variable_declaration SEMICOLON
                | variable_assignment SEMICOLON
                | type_declaration SEMICOLON
                | function_declaration
                | if_statement
                | while_statement

    expression:  L_PARENTHESIS expression R_PARENTHESIS
                | binary_expression
                | unary_expression
                value

    binary_expression : expression PLUS expression  %prec PLUS
                    | expression MINUS expression %prec MINUS
                    | expression MULTIPLY expression %prec MULTIPLY
                    | expression DIVIDE expression %prec DIVIDE
                    | expression AND expression %prec AND
                    | expression OR expression %prec OR
                    | expression EQUALS expression %prec EQUALS
                    | expression GREATER_THAN expression %prec GREATER_THAN
                    | expression LESS_THAN expression %prec LESS_THAN
                    | expression GREATER_EQUAL expression %prec GREATER_EQUAL
                    | expression LESS_EQUAL expression %prec LESS_EQUAL

    unary_expression: : unary_operator L_PARENTHESIS expression R_PARENTHESIS
                        | unary_operator value
    
    unary_operator : MINUS %prec UMINUS
                    | NOT
                    | PLUS %prec UPLUS


    value: NUMBER_VALUE 
            | CHAR_VALUE 
            | BOOL_VALUE
            | ID 
            | NULL
            | ID L_PARENTHESIS argument_list R_PARENTHESIS
            | ID DOT ID recursive_atribute_access
            | ID L_SQ_BRACKET QUOTED_ID R_SQ_BRACKET recursive_atribute_access



    argument_list: expression 
                    | expression COMMA argument_list
                    | empty

    atribute_access: ID recursive_atribute_access

    recursive_atribute_access:  DOT ID recursive_atribute_access
                            | L_SQ_BRACKET QUOTED_ID R_SQ_BRACKET recursive_atribute_access
                            | empty

    variable_declaration: LET ID recursive_variable_declaration
                        | LET ID TWO_POINTS ID recursive_variable_declaration
                        | LET ID TWO_POINTS type recursive_variable_declaration
                        
    recursive_variable_declaration: COMMA ID recursive_variable_declaration
                                    | COMMA ID TWO_POINTS ID recursive_variable_declaration
                                    | empty

    variable_assignment : basic_var_assignment
                        | object_var_assignment


    basic_var_assignment: ID ASSIGN expression
                            | variable_declaration ASSIGN expression

    object_var_assignment: variable_declaration ASSIGN object_body 
                            | ID ASSIGN object_body 
                            | atribute_access ASSIGN expression
                            | atribute_access ASSIGN object_body

    object_body: L_BRACKET object_body_content R_BRACKET

    object_body_content: ID TWO_POINTS expression recursive_obejct_body_content
                            | QUOTED_ID TWO_POINTS expression recursive_obejct_body_content
                            | ID TWO_POINTS object_body recursive_obejct_body_content
                            | QUOTED_ID TWO_POINTS object_body recursive_obejct_body_content

    recursive_obejct_body_content: COMMA ID TWO_POINTS expression recursive_obejct_body_content
                                    | COMMA QUOTED_ID TWO_POINTS expression recursive_obejct_body_content
                                    | COMMA ID TWO_POINTS object_body recursive_obejct_body_content
                                    | COMMA QUOTED_ID TWO_POINTS object_body recursive_obejct_body_content
                                    | empty
                                    | COMMA empty

    type_declaration: TYPE ID ASSIGN type_body

    type_body: L_BRACKET type_body_content R_BRACKET

    type_body_content: ID TWO_POINTS type type_body_content_recursive
                     | QUOTED_ID TWO_POINTS type type_body_content_recursive
                     | ID TWO_POINTS ID type_body_content_recursive
                     | QUOTED_ID TWO_POINTS ID type_body_content_recursive
                     | ID TWO_POINTS type_body type_body_content_recursive
                     | QUOTED_ID TWO_POINTS type_body type_body_content_recursive
                     
                     
    type_body_content_recursive : COMMA ID TWO_POINTS type type_body_content_recursive
                                | COMMA QUOTED_ID TWO_POINTS type type_body_content_recursive
                                | COMMA ID TWO_POINTS ID type_body_content_recursive
                                | COMMA QUOTED_ID TWO_POINTS ID type_body_content_recursive
                                | COMMA ID TWO_POINTS type_body type_body_content_recursive
                                | COMMA QUOTED_ID TWO_POINTS type_body type_body_content_recursive
                                | empty
                                | COMMA empty

    type: INT | FLOAT | CHARACTER | BOOLEAN

    function_declaration : function_header function_body 

    function_header : FUNCTION ID L_PARENTHESIS function_params R_PARENTHESIS TWO_POINTS return_type

    function_body : L_BRACKET statement_list RETURN return_statement R_BRACKET

    function_params : ID TWO_POINTS type COMMA function_params
                | ID TWO_POINTS type 
                | ID TWO_POINTS ID COMMA function_params
                | ID TWO_POINTS ID
                | empty

    return_type: type | ID

    return_statement: expression SEMICOLON
                    | object_body SEMICOLON

    if_statement : IF if_evaluation if_statements else_statement %prec IF

    if_evaluation : L_PARENTHESIS expression R_PARENTHESIS

    if_statements : L_BRACKET statement statement_list R_BRACKET

    else_statement : ELSE L_BRACKET statement statement_list R_BRACKET
                       | empty

    while_statement : while_header while_statements

    while_header : WHILE L_PARENTHESIS expression R_PARENTHESIS

    while_statements : L_BRACKET statement statement_list R_BRACKET
    
    """
    
    start = 'program'
    
    """
    precedencia: (1 es la mayor precedencia, 5 la menor)
    1. UNARIOS
    2. MULTIPLICATIVOS
    3. ADITIVOS
    4. RELACIONALES
    5. LOGICOS
    """
    precedence = (
        ('left', 'OR'), # LOGICOS
        ('left', 'AND'),
        ('left', 'EQUALS', # RELACIONALES
                'GREATER_THAN', 
                'LESS_THAN', 
                'GREATER_EQUAL', 
                'LESS_EQUAL'),
        ('left', 'PLUS', 'MINUS'), # ADITIVOS
        ('left', 'MULTIPLY', 'DIVIDE'), # MULTIPLICATIVOS
        ('right', 'NOT'), # UNARIOS
        ('right', 'UMINUS'),
        ('right', 'UPLUS'),
        ('left', 'IF', 'ELSE', 'WHILE')
    )
    
    def p_empty(self, p):
        '''
        empty : 
        '''
        p[0] = None
        
    def p_program(self, p):
        '''
        program : statement_list
        '''
        p[0] = p[1]
        
    
    def p_statement_list(self, p):
        '''
        statement_list : statement statement_list
                        | empty
        '''
        p[0] = [p[1]] + p[2] if len(p) == 3 else []
    
    def p_statement(self, p):
        '''
         statement : expression SEMICOLON
                | variable_declaration SEMICOLON
                | variable_assignment SEMICOLON
                | type_declaration SEMICOLON
                | function_declaration
                | if_statement
                | while_statement
        '''
        p[0] = p[1]
    
    def p_expression(self, p):
        '''
        expression :  L_PARENTHESIS expression R_PARENTHESIS
                | binary_expression
                | unary_expression
                | value
        '''
        # if the value of the expression is None return a Symbol with None value
        if len(p) == 2 and p[1] is None:
            p[0] = Symbol(None, None)
            return
        elif len(p) == 3 and p[2] is None:
            p[0] = Symbol(None, None)
            return
            
        
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]
            
        
    def p_binary_expression(self, p):
        '''
        binary_expression : expression PLUS expression  %prec PLUS
                        | expression MINUS expression %prec MINUS
                        | expression MULTIPLY expression %prec MULTIPLY
                        | expression DIVIDE expression %prec DIVIDE
                        | expression AND expression %prec AND
                        | expression OR expression %prec OR
                        | expression EQUALS expression %prec EQUALS
                        | expression GREATER_THAN expression %prec GREATER_THAN
                        | expression LESS_THAN expression %prec LESS_THAN
                        | expression GREATER_EQUAL expression %prec GREATER_EQUAL
                        | expression LESS_EQUAL expression %prec LESS_EQUAL
        '''
        # comprobar que los operandos son compatibles con el operador
        # number value es el tipo que tienen los valores instanciados sin declarar ej: a+ 2 a-> tipo con el que se declaro, 2 -> NUMBER_VALUE
        
        compatible_types = {
            "+": {"int", "float", "character", "NUMBER_VALUE"},
            "-": {"int", "float", "character", "NUMBER_VALUE"},
            "*": {"int", "float", "character", "NUMBER_VALUE"},
            "/": {"int", "float", "character", "NUMBER_VALUE"},
            "&&": {"BOOL_VALUE"},
            "||": {"BOOL_VALUE"},
            "==": {"int", "float", "character", "BOOL_VALUE", "NUMBER_VALUE"},
            ">": {"int", "float", "character", "NUMBER_VALUE"},
            "<": {"int", "float", "character", "NUMBER_VALUE"},
            ">=": {"int", "float", "character", "NUMBER_VALUE"},
            "<=": {"int", "float", "character", "NUMBER_VALUE"}
        }
        restrictiveness = ["NUMBER_VALUE", "float", "character", "int",  "BOOL_VALUE"]
            
        if p[1].type not in compatible_types[p[2]] or p[3].type not in compatible_types[p[2]]:
            print(f"Error: Operands of type {p[1].type} and {p[3].type} are not compatible with operator {p[2]}")
            p[0] = Symbol(None, None)
            return
        # convert to next less restrictive type if necessary
        if p[1].type != p[3].type:
            if PrimitiveTypes.get_less_restrictive(p[1].type, p[3].type) == p[1].type:
                if p[3].type != "NUMBER_VALUE" and p[3].type != "BOOL_VALUE":
                    print(f"Warn: Implicit conversion of {p[3].name} from {p[3].type} to {p[1].type}")
                p[3].type = p[1].type
            else:
                if p[1].type != "NUMBER_VALUE" and p[1].type != "BOOL_VALUE":
                    print(f"Warn: Implicit conversion of {p[1].name} from {p[1].type} to {p[3].type}")
                p[1].type = p[3].type
        # if the operator is a logical operator, the result is a boolean 
        
        # if both symbols have value, calculate the result
        if p[1].value is not None and p[3].value is not None:
            if p[2] == "+":
                p[0] = Symbol(None, p[1].type, p[1].value + p[3].value)
            elif p[2] == "-":
                p[0] = Symbol(None, p[1].type, p[1].value - p[3].value)
            elif p[2] == "*":
                p[0] = Symbol(None, p[1].type, p[1].value * p[3].value)
            elif p[2] == "/":
                p[0] = Symbol(None, p[1].type, p[1].value / p[3].value)
            elif p[2] == "&&":
                p[0] = Symbol(None, "BOOL_VALUE", p[1].value and p[3].value)
            elif p[2] == "||":
                p[0] = Symbol(None, "BOOL_VALUE", p[1].value or p[3].value)
            elif p[2] == "==":
                p[0] = Symbol(None, "BOOL_VALUE", p[1].value == p[3].value)
            elif p[2] == ">":
                p[0] = Symbol(None, "BOOL_VALUE", p[1].value > p[3].value)
            elif p[2] == "<":
                p[0] = Symbol(None, "BOOL_VALUE", p[1].value < p[3].value)
            elif p[2] == ">=":
                p[0] = Symbol(None, "BOOL_VALUE", p[1].value >= p[3].value)
            elif p[2] == "<=":
                p[0] = Symbol(None, "BOOL_VALUE", p[1].value <= p[3].value)
        else:
            if p[2] in ["&&", "||", "==", ">", "<", ">=", "<="]:
                p[0] = Symbol(None, "BOOL_VALUE")
            else:
                p[0] = Symbol(None, p[1].type)
        return
        
        
    def p_unary_expression(self, p):
        '''
        unary_expression : unary_operator L_PARENTHESIS expression R_PARENTHESIS
                        | unary_operator value
        '''
        compatible_types = {
            "-": {"int", "float", "character", "NUMBER_VALUE"},
            "+": {"int", "float", "character", "NUMBER_VALUE"},
            "!": {"BOOL_VALUE"}
        }
        if p.slice[2].type == "L_PARENTHESIS":
            sym = p[3]
            if sym.type not in compatible_types[p[1]]:
                print(f"Operand {sym} is not compatible with operator {p[1]}")
        else:
            sym = p[2]
            if sym.type not in compatible_types[p[1]]:
                print(f"Operand {sym} is not compatible with operator {p[1]}")
        
        # if symbol has value, calculate the result
        if sym is not None:
            if p[1] == "-":
                p[0] = Symbol(None, sym.type, -sym.value)
            elif p[1] == "+":
                p[0] = Symbol(None, sym.type, +sym.value)
            elif p[1] == "!":
                p[0] = Symbol(None, sym.type, not sym.value)
        else:
            p[0] = Symbol(None, sym.type)
            
        
        
            
    def p_unary_operator(self, p):
        '''
        unary_operator : MINUS %prec UMINUS
                    | NOT
                    | PLUS %prec UPLUS
        '''
        p[0] = p[1]
    
    def p_value(self, p):
        '''
        value : NUMBER_VALUE 
                | CHAR_VALUE 
                | BOOL_VALUE
                | ID 
                | NULL
                | ID L_PARENTHESIS argument_list R_PARENTHESIS
                | ID DOT ID recursive_atribute_access
                | ID L_SQ_BRACKET QUOTED_ID R_SQ_BRACKET recursive_atribute_access
        '''
        # valores primitivos e ids
        if len(p) == 2:
            # si es un ID comprobar si esta en la tabla de simbolos
            if p.slice[1].type == "ID":
                if self.st.get(p.slice[1].value) is None:
                    print(f"Error: Variable {p.slice[1].value} not declared in scope {self.st.scope}")
                else: # si esta en la tabla de simbolos
                    p[0] = self.st.get(p.slice[1].value)
                    if p[0] is None: # si no se encontro la variable
                        print(f"Error: Variable {p.slice[1].value} not declared in scope {self.st.scope}")
            else:
                # en otro caso es un valor primitivo
                p[0] = Symbol(None, p.slice[1].type, p.slice[1].value)
            return

        # llamadas a funciones y acceso a atributos
        if len(p) == 5 and p.slice[4].type == "recursive_atribute_access":
            atr = [p[1], p[3]] + p[4] if p[4] is not None else [p[1], p[3]]
            symbol = self.st.get(atr)
            if symbol is None: # comprobar si el objeto existe
                print(f"Error: Variable {p[1]} not declared in scope {self.st.scope}")
                return
            p[0] = symbol
            return
            
            
        elif len(p)==5 and p.slice[3].type == "argument_list":
            
            func_name = p[1]
            func_symbol = self.st.get(func_name)
            if func_symbol is None or not isinstance(func_symbol, Function):
                print(f"Error: '{func_name}' is not a function or is not declared")
                return
            
            # Comprobar que la cantidad de argumentos y tipos coincidan
            given_args = p[3]
            expected_args = func_symbol.parameters
            if len(given_args) != len(expected_args):
                print(f"Incorrect number of arguments for function '{func_name}'")

            for given_arg, expected_arg in zip(given_args, expected_args):
                if not PrimitiveTypes.is_compatible(given_arg.type, expected_arg.type):
                    print(f"Argument type mismatch in function '{func_name}': expected {expected_arg.type}, got {given_arg.type}")

            p[0] = Symbol(None, func_symbol.type)  # Asignar el tipo de retorno de la función


        if len(p) == 6: # acceso a atributos
            atr = [p[1], p[3]] + p[5] if p[5] is not None else [p[1], p[3]]
            symbol = self.st.get(atr)
            if symbol is None:
                print(f"Error: Variable {p[1]} not declared in scope {self.st.scope}")
                return
            p[0] = symbol
    
    def p_argument_list(self, p):
        '''
        argument_list : expression 
                        | expression COMMA argument_list
                        | empty
        '''
        if len(p) == 1:  # Caso empty
            p[0] = []
        elif len(p) == 2:  # Un solo argumento
            p[0] = [p[1]]
        else:  # Varios argumentos
            p[0] = [p[1]] + p[3]
        
    def p_atribute_access(self, p):
        '''
        atribute_access : ID recursive_atribute_access
        '''
        # comprobar que el atributo existe en el objeto
        var = self.st.get(p.slice[1].value)
        if var is None:
            print(f"Error: Variable {p.slice[1].value} not declared")
        if not isinstance(var, Object):
            print(f"Error: {p.slice[1].value} is not an object")
        
        p[0] = [p[1]] + p[2] if p[2] is not None else [p[1]]
         
        
    def p_recursive_atribute_access(self, p):
        '''
        recursive_atribute_access :  DOT ID recursive_atribute_access
                            | L_SQ_BRACKET QUOTED_ID R_SQ_BRACKET recursive_atribute_access
                            | empty
        '''
        if len(p) == 2:
            p[0] = None
            return
        elif len(p) == 4:
            post = p[3]
        elif len(p) == 5:
            post = p[4]
        p[0] = [p[2]] + post if post is not None else [p[2]]
        

    def p_variable_declaration(self, p):
        '''
        variable_declaration : LET ID recursive_variable_declaration
                             | LET ID TWO_POINTS ID recursive_variable_declaration
                             | LET ID TWO_POINTS type recursive_variable_declaration
        '''
        # copmprobar si es una variable con o sin tipo
        if len(p) == 4:
            self.st.add(Symbol(p.slice[2].value, None)) # variable sin tipo
        else: # variable con tipo
            # comprobar si es un tipo primitivo o definido
            if p.slice[4].type == "ID":
                # comprobar que el tipo existe en la tabla de simbolos
                type_symbol = self.st.get(p.slice[4].value)
                if type_symbol is None:
                    print(f"Error: Type {p.slice[4].value} not declared")
                    return
                if not isinstance(type_symbol, Type):
                    print(f"Error: {p.slice[4].value} is not a type")
                    return
                self.st.add(Object(p.slice[2].value, type_symbol.type, type_symbol.atributes))
            else: # es un tipo primitivo
                self.st.add(Symbol(p.slice[2].value, p.slice[4].value))

        p[0] = p[2]
        
    
    def p_recursive_variable_declaration(self, p):
        '''
        recursive_variable_declaration : COMMA ID recursive_variable_declaration
                                    | COMMA ID TWO_POINTS ID recursive_variable_declaration
                                    | empty
        '''
        if len(p) == 2:
            p[0] = None
            return
        elif len(p) == 4:
            self.st.add(Symbol(p.slice[2].value, None)) # variable sin tipo
        else:
            self.st.add(Symbol(p.slice[2].value, p.slice[4].value))
        p[0] = p[2]
        
    
    def p_variable_assignment(self, p):
        '''
        variable_assignment : basic_var_assignment
                            | object_var_assignment
        '''
        p[0] = p[1]
        
    def p_basic_var_assignment(self, p):
        '''
        basic_var_assignment : ID ASSIGN expression
                            | variable_declaration ASSIGN expression
        '''
        compatible_types = {
            "int": {"int", "NUMBER_VALUE"},
            "float": {"float", "NUMBER_VALUE", "int"},
            "character": {"character", "NUMBER_VALUE", "int"},
            "BOOL_VALUE": {"BOOL_VALUE"}
        }
        
        # comprobar que la variable a asignar existe
        var_symbol = self.st.get(p.slice[1].value)
        if var_symbol is None:
            print(f"Error: Variable {p.slice[1].value} not declared")
            return
        # si los tipos son distintos mostrar un warning
        if var_symbol.type != p[3].type and not PrimitiveTypes.is_compatible(var_symbol.type, p[3].type):
            print(f"Warn: Implicit conversion of {var_symbol.name} from {var_symbol.type} to {p[3].type}")
        # como el lenguaje es debilmente tipado y dinamico, se puede asignar cualquier tipo a una variable
        self.st.update(name=p.slice[1].value, new_symbol=Symbol(p.slice[1].value, p[3].type, p[3].value))


    def p_object_var_assignment(self, p):
        '''
        object_var_assignment : variable_declaration ASSIGN object_body 
                            | ID ASSIGN object_body 
                            | atribute_access ASSIGN expression
                            | atribute_access ASSIGN object_body
        '''
        # comprobar el tipo de la variable a asignar
        var_symbol = self.st.get(p.slice[1].value)
        if var_symbol is None:
            print(f"Error: Variable {p.slice[1].value} not declared")
            return
        # comprobar si el type existe en la tabla de simbolos
        
        var_type = var_symbol.type
        if isinstance(var_type, Type) or isinstance(var_type, Object):
            var_symbol.atributes = p[3].atributes
        elif var_type is not None: # variable con tipo asignar objeto
            if p.slice[3].type == "expression":
                if var_type != p[3].type and not PrimitiveTypes.is_compatible(var_type, p[3].type) :
                    print(f"Warn: Implicit conversion of {var_symbol.name} from {var_symbol.type} to {p[3].type}")
                    self.st.update(name=p.slice[1].value, new_symbol=Symbol(var_symbol.name, p[3].type, p[3].value))
                else:
                    self.st.update(name=p.slice[1].value, new_symbol=Symbol(var_symbol.name, var_type, p[3].value))
            else: # object_body
                self.st.update(name=p.slice[1].value, new_symbol=Object(var_symbol.name, var_type, p[3]))
        
        else: # variable sin tipo asignar objeto
            self.st.update(name=p.slice[1].value, new_symbol=Object(p.slice[1].value, None, p[3]))
        
            

    def p_object_body(self, p):
        '''
        object_body : L_BRACKET object_body_content R_BRACKET
        '''
        # va tener que ser un Object
        p[0] = p[2]
        
    def p_object_body_content(self, p):
        '''
        object_body_content : ID TWO_POINTS expression recursive_obejct_body_content
                            | QUOTED_ID TWO_POINTS expression recursive_obejct_body_content
                            | ID TWO_POINTS object_body recursive_obejct_body_content
                            | QUOTED_ID TWO_POINTS object_body recursive_obejct_body_content
        '''
        atributes = []
        if p.slice[3].type == "expression":
            p[3].name = p[1]
            atributes.append(p[3])
        else: # object_body
            atributes.append(Object(p[1], p[3], p[4]))
        
        p[0] = atributes + p[4]
    
    def p_recursive_obejct_body_content(self, p):
        '''
        recursive_obejct_body_content : COMMA ID TWO_POINTS expression recursive_obejct_body_content
                                    | COMMA QUOTED_ID TWO_POINTS expression recursive_obejct_body_content
                                    | COMMA ID TWO_POINTS object_body recursive_obejct_body_content
                                    | COMMA QUOTED_ID TWO_POINTS object_body recursive_obejct_body_content
                                    | empty
                                    | COMMA empty
        '''
        atributes = []
        if len(p) == 2 or len(p) == 3: # empty or COMMA empty
            p[0] = atributes
        else: # hay uno o mas atributos
            if p.slice[4].type == "expression":
                p[4].name = p[2]
                atributes.append(p[4])
            else: # object_body
                atributes.append(Object(p[2], None, p[4]))
            p[0] = atributes + p[5]
            
    
    def p_type_declaration(self, p):
        '''
        type_declaration : TYPE ID ASSIGN type_body
        '''
        atributes = p[4]
        self.st.add(Type(p[2], atributes))
        p[0] = p[2]
    
    def p_type_body(self, p):
        '''
        type_body : L_BRACKET type_body_content R_BRACKET
        '''
        p[0] = p[2]
        
    def p_type_body_content(self, p):
        '''
        type_body_content : ID TWO_POINTS type type_body_content_recursive
                        | QUOTED_ID TWO_POINTS type type_body_content_recursive
                        | ID TWO_POINTS ID type_body_content_recursive
                        | QUOTED_ID TWO_POINTS ID type_body_content_recursive
                        | ID TWO_POINTS type_body type_body_content_recursive
                        | QUOTED_ID TWO_POINTS type_body type_body_content_recursive
        '''
        atributes = []
        # comprobar si es tipo primitivo, definido o inmediato
        if p.slice[3].type == "ID":
            # comprobar que existe en la tabla de simbolos
            id_symbol = self.st.get(p.slice[3].value)
            if id_symbol is None:
                print(f"Error: Type {p.slice[3].value} not declared")
            if not isinstance(id_symbol, Type):
                print(f"Error: {p.slice[3].value} is not a type")
            atributes.append(Symbol(p[1], id_symbol.type))
        elif p.slice[3].type == "type":
            atributes.append(Symbol(p[1], p[3]))
        else: # type_body
            atributes.append(Type(p[1], p[3]))
        p[0] = atributes + p[4]
         
    
    def p_type_body_content_recursive(self, p):
        '''
        type_body_content_recursive : COMMA ID TWO_POINTS type type_body_content_recursive
                                    | COMMA QUOTED_ID TWO_POINTS type type_body_content_recursive
                                    | COMMA ID TWO_POINTS ID type_body_content_recursive
                                    | COMMA QUOTED_ID TWO_POINTS ID type_body_content_recursive
                                    | COMMA ID TWO_POINTS type_body type_body_content_recursive
                                    | COMMA QUOTED_ID TWO_POINTS type_body type_body_content_recursive
                                    | empty
                                    | COMMA empty
        '''
        atributes = []
        # comprobar si es tipo primitivo, definido o inmediato
        if len(p) == 2 or len(p) == 3: # empty or COMMA empty
            p[0] = atributes
        else: # hay uno o mas atributos
            if p.slice[4].type == "ID":
                # comprobar que existe en la tabla de simbolos
                id_symbol = self.st.get(p.slice[4].value)
                if id_symbol is None:
                    print(f"Error: Type {p.slice[4].value} not declared")
                if not isinstance(id_symbol, Type):
                    print(f"Error: {p.slice[4].value} is not a type")
                atributes.append(Symbol(p[2], id_symbol))
            elif p.slice[4].type == "type":
                atributes.append(Symbol(p[2], p[4]))
            else: # type_body
                atributes.append(Type(p[2], p[4]))
            p[0] = atributes + p[5]

    def p_type(self, p):
        '''
        type : INT 
             | FLOAT 
             | CHARACTER 
             | BOOLEAN
        '''
        p[0] = p[1]
    
    def p_function_declaration(self, p):
        '''
        function_declaration : function_header function_body 
        '''
        # comprobar que el tipo de function header y de function body coincidan
        if p[1].type != p[1].type  and PrimitiveTypes.is_compatible(p[1].type, p[2].type) is False:
            print(f"Return type mismatch in function declaration of {p[1].name}")
    
    def p_function_header(self, p):
        '''
        function_header : FUNCTION ID L_PARENTHESIS function_params R_PARENTHESIS TWO_POINTS return_type
        '''
        # comprobar que el tipo de retorno es valido
        if p[7] not in {"int", "float", "character", "boolean"} and self.st.get(p[7]) is None:
            print(f"Invalid return type {p[7]}")
        # añadir funcion a la tabla de simbolos
        fun = Function(name=p[2], type=p[7], parameters=p[4])
        self.st.add(fun)
        self.st.enter_scope(p[2])
        p[0] = fun
        
        
    
    def p_function_body(self, p):
        '''
        function_body : L_BRACKET statement_list RETURN return_statement R_BRACKET
        '''
        self.st.exit_scope()
        p[0] = p[4]
        
    def p_function_params(self, p):
        '''
        function_params : ID TWO_POINTS type COMMA function_params
                    | ID TWO_POINTS type 
                    | ID TWO_POINTS ID COMMA function_params
                    | ID TWO_POINTS ID
                    | empty
        '''
        if len(p) == 2:
            p[0] = None
            return []
        
        if p.slice[3].type == "ID":
            # comprobar que el tipo existe en la tabla de simbolos
            type_symbol = self.st.get(p[3])
            if type_symbol is None:
                print(f"Error: Type {p[3]} not declared")
            if not isinstance(type_symbol, Type):
                print(f"Error: {p[3]} is not a type ")
        else: # es un tipo primitivo
            if p[3] not in {"int", "float", "character", "BOOL_VALUE"} :
                print(f"Invalid parameter type {p[3]}")
        
        p[0] = [Symbol(p[1], p[3])] + p[5] if len(p) == 6 else [Symbol(p[1], p[3])]
        
    
    def p_return_type(self, p):
        '''
        return_type : type 
                    | ID
        '''
        p[0] = p[1]
        
    
    def p_return_statement(self, p):
        '''
        return_statement : expression SEMICOLON
                    | object_body SEMICOLON
        '''
        if p.slice[1].type == "expression":
            p[0] = p[1]
        else:
            p[0] = Object(None, None, p[1])
    
    
    def p_if_statement(self, p):
        '''
        if_statement : IF if_evaluation if_statements else_statement %prec IF
        '''
    
    
    def p_if_evaluation(self, p):	
        '''
        if_evaluation : L_PARENTHESIS expression R_PARENTHESIS
        '''
        self.st.enter_fc_scope()
        if p[2].type != "BOOL_VALUE" and p[2].type != "boolean":
            print("If condition must be a boolean expression")
            return
        if p[2].value is not None:
            self.consider_if = p[2].value
        p[0] = p[2]

   
    def p_if_statements(self, p):
        '''
        if_statements : L_BRACKET statement statement_list R_BRACKET
        '''
        if self.consider_if:
            self.st.merge_fc_scope()
        else:
            self.st.discard_fc_scope()
        self.st.enter_fc_scope()
            
        
        
    def p_else_statement(self, p):
        '''
        else_statement : ELSE L_BRACKET statement statement_list R_BRACKET
                       | empty
        '''
        if self.consider_if:
            self.st.discard_fc_scope()
        else:
            self.st.merge_fc_scope()
    
    def p_while_statement(self, p):
        '''
        while_statement : while_header while_statements
        '''

    def p_while_header(self, p):
        '''
        while_header : WHILE L_PARENTHESIS expression R_PARENTHESIS
        '''
        if not p[3] or (p[3].type != "BOOL_VALUE" and p[3].type != "boolean"):
            print(f"Error: While condition must be a boolean expression")
        self.st.enter_fc_scope()
        
        
    def p_while_statements(self, p):
        '''
        while_statements : L_BRACKET statement statement_list R_BRACKET
        '''
        # no vamos a considerar las variables de la condicion del while
        self.st.merge_fc_scope_as_unknwon()
        
    def p_error(self, p):
        if p:
            print(f"Syntax error : {p.type}:'{p.value}' at line {p.lineno}")
        else:
            print("Unexpected EoF")     
    
    def test(self, data, output_file):
        self.parser.parse(data, lexer=self.lexer)
        with open(output_file, "w") as f:
            f.write(str(self.st))
        print(self.st)
        