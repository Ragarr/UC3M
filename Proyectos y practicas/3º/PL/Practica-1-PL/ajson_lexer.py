"""
Autores: 
    - Raúl Aguilar Arroyo 100472050
    - Natalia Rodriguez Navarro 100471976
"""

import ply.lex as lex

class AJSONLexer:

    def __init__(self):
        self.lexer = lex.lex(module=self)

    # List of token names
    tokens = (
            "NUMBER",
            "STRING",
            "KEY",
            "BOOL",
            "NULL",
            "COMPARATOR",
            "L_BRACKET",
            "R_BRACKET",
            "COMMA",
            "L_SQ_BRACKET",
            "R_SQ_BRACKET"
            )
    
    # Regular expression rules for simple tokens
    t_COMPARATOR = r'== |<= | >= | < | >'
    t_L_BRACKET = r'{'
    t_R_BRACKET = r'}'
    t_COMMA = r','
    t_L_SQ_BRACKET = r'\['
    t_R_SQ_BRACKET = r'\]'

    # Regular expression rule for key
    two_points_re = r'\s*:\s*'
    without_quotes_re = r'[a-zA-Z_][a-zA-Z0-9_]*' +  two_points_re
    with_quotes_re = r'\"[^\"\n]*\"' + two_points_re
    key_re = with_quotes_re + "|" + without_quotes_re 

    @lex.TOKEN(key_re)
    def t_KEY(self, t):
        t.value = str(t.value.replace('"', '').replace(":", "").strip())
        return t
    
    # Regular expression rule for null, change value to None
    def t_NULL(self, t):
        r'null|NULL'
        t.value = None
        return t
    
    # Regular expression rule for bool's, change value to True or False
    def t_BOOL(self, t):
        r'TR|FL|tr|fl|Tr|Fl'
        t.value = True if t.value in ["TR", "tr", "Tr"] else False
        return t
    
    # Regular expression rule for number
    exp_re = r'(-?[\d]*.?\d*(e|E)-?\d+)'
    float_re = r'(-?\d*\.\d+)'
    int_re = r'(-?[1-9][0-9]*)'
    bin_re = r'((0b|0B)[01]+)'
    hex_re = r'(0x|0X)[0-9a-fA-F]+'
    oct_re = r'(0[0-7]+)'
    num_re = exp_re + "|" + float_re + "|" + int_re + "|" + bin_re + "|" + hex_re + "|" + oct_re
    
    @lex.TOKEN(num_re)
    def t_NUMBER(self, t):
        if t.value.startswith("0") and t.value[1] in "1234567":
            t.value = int(t.value, 8)
            return t
               
        try:
            t.value = eval(t.value) 
        except:
            self.t_error(t)
        return t
    
    # Regular expression rule for string
    def t_STRING(self, t):
        r'\"[^\"\n]*\"'
        t.value = str(t.value.replace('"', ''))
        return t

    t_ignore = ' \t'

    def t_NL(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print("[LEXER][ERROR] Illegal character '{0}' at line {1}".format(t.value[0], t.lineno))
        t.lexer.skip(1)

    # Test it output
    def test(self, input):
        self.lexer.input(input)
        for token in self.lexer:
            print(token.type, token.value)
        

        
    
    
    
