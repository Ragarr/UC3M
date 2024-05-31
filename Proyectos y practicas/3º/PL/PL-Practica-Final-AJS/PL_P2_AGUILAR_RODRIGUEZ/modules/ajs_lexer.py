"""
Autores: 
    - Raúl Aguilar Arroyo 100472050
    - Natalia Rodriguez Navarro 100471976

Módulo que implementa el lexer
"""

import ply.lex as lex


class AJSLexer:
    def __init__(self) -> None:
        self.lexer = lex.lex(module=self)
        

    # List of token names    
    reserved = (
        'LET',
        'INT',
        'FLOAT',
        'CHARACTER',
        'WHILE',
        'BOOLEAN',
        'FUNCTION',
        'RETURN',
        'TYPE',
        'IF',
        'ELSE',
        'NULL'        
    )
    
    reserved_map = {t.lower(): t for t in reserved}
    

    tokens = (
        "NUMBER_VALUE",
        "CHAR_VALUE",
        "BOOL_VALUE",
        "L_BRACKET",
        "R_BRACKET",
        "COMMA",
        "SEMICOLON",
        "ASSIGN",
        "TWO_POINTS",
        "PLUS", 
        "MINUS",
        "MULTIPLY",
        "DIVIDE",
        "AND",
        "OR",
        "NOT",
        "EQUALS",
        "GREATER_THAN",
        "LESS_THAN",
        "GREATER_EQUAL",
        "LESS_EQUAL",
        "ID",
        "DOT",
        "L_SQ_BRACKET",
        "R_SQ_BRACKET",
        "QUOTED_ID", # referencia a un key con comillas
        "L_PARENTHESIS",
        "R_PARENTHESIS",        
    ) + reserved
    
    # Regular expression rules for simple tokens
    t_DOT =             r'\.'
    t_L_BRACKET =       r'{'
    t_R_BRACKET =       r'}'
    t_COMMA =           r','
    t_SEMICOLON =       r';'
    t_EQUALS =          r'=='
    t_GREATER_EQUAL =   r'>='
    t_LESS_EQUAL =      r'<='
    t_GREATER_THAN =    r'>'
    t_LESS_THAN =       r'<'
    t_ASSIGN =          r'='
    t_TWO_POINTS =      r':'
    t_PLUS =            r'\+'
    t_MINUS =           r'-'
    t_MULTIPLY =        r'\*'
    t_DIVIDE =          r'/'
    t_NOT =             r'!'
    t_AND =             r'&&'
    t_OR =              r'\|\|'
    t_L_SQ_BRACKET =    r'\['
    t_R_SQ_BRACKET =    r'\]'
    t_L_PARENTHESIS =   r'\('
    t_R_PARENTHESIS =   r'\)'

    
    bool_re = r'(tr|fl(?!oat))'
    @lex.TOKEN(bool_re)
    def t_BOOL_VALUE(self, t):
        if t.value == "tr":
            t.value = True
        else:
            t.value = False
        return t
    
    char_re = r'\'[\x00-\xFF]\'' # cualquier caracter ascii extendido
    
    @lex.TOKEN(char_re)
    def t_CHAR_VALUE(self, t):
        t.value = str(t.value.replace("'", "").strip())
        t.value = str(t.value.replace('"', "").strip())
        return t
    
    # string sin comillas
    without_quotes_re = r'[a-zA-Z_][a-zA-Z0-9_]*'
    # string con comillas
    with_quotes_re = r'\"[^\"\n]*\"'
    key_re = with_quotes_re + "|" + without_quotes_re
    

    
    # Regular expression rule for key    
    @lex.TOKEN(without_quotes_re)
    def t_ID(self, t):
        if t.value in self.reserved_map:
            t.type = self.reserved_map[t.value]
        t.value = str(t.value.replace('"', '').strip())
        t.value = str(t.value.replace("'", "").strip())
        return t
    
    @lex.TOKEN(with_quotes_re)
    def t_QUOTED_ID(self, t):
        
        t.value = str(t.value.replace('"', '').strip())
        t.value = str(t.value.replace("'", "").strip())
        return t
    
    # line comment
    def t_LINE_COMMENT(self, t):
        r'//.*'
        # add line number
        t.lexer.lineno += t.value.count('\n')
        pass
        
    
    # block comment
    def t_BLOCK_COMMENT(self, t):
        r'/\*(.|\n)*?\*/'
        # add line number
        t.lexer.lineno += t.value.count('\n')
        pass
        
    
    # number value
    # Regular expression rule for number
    exp_re = r'([\d]*.?\d*(e|E)-?\d+)'
    float_re = r'(\d*\.\d+) | (\d+\.\d*)'
    bin_re = r'((0b|0B)[01]+)'
    hex_re = r'(0x|0X)[0-9a-fA-F]+'
    oct_re = r'(0[0-7]+)'
    int_re = r'([1-9][0-9]*) | 0'
    num_re = exp_re + "|" + float_re + "|" + bin_re + "|" + hex_re + "|" + oct_re + "|" + int_re
    
    @lex.TOKEN(num_re)
    def t_NUMBER_VALUE(self, t):
        if t.value.startswith("0") and (len(t.value) > 1) and t.value[1] in "1234567":
            t.value = int(t.value, 8)
            return t
               
        try:
            t.value = eval(t.value) 
        except:
            self.t_error(t)
        return t
    
    
    
    
    t_ignore = ' \t'
    def t_NL(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
    
    def t_error(self, t):
        print(f"Illegal character at line {t.lineno} '{t.value[0]}'")
        t.lexer.skip(1)
        
    def test(self, data):
        self.lexer.input(data)
        # for token in self.lexer:
            # print("{" + f"T: {str(token.type).ljust(13)} V: {f"'{token.value}'".ljust(7)} L: {token.lineno}" + "}")
