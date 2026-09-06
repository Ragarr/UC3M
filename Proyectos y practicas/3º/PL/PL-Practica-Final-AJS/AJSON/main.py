"""
Autores: 
    - Raúl Aguilar Arroyo 100472050
    - Natalia Rodriguez Navarro 100471976
"""

from ajson_lexer import AJSONLexer
from ajson_parser import AJSONParser
import sys

def main(file_name: str, mode: str = None):

    # Archivo de entrada
    try:
        file = open(file_name, "r")
    except:
        print("File not found")
        return
    data = file.read()
    
    if not data:
        print('\nFICHERO AJSON VACÍO "{}"'.format(file_name))
        return 
    else:
        print('\nFICHERO AJSON "{}"'.format(file_name))


    if mode == "lexer":
        # ANÁLISIS LÉXICO
        lexer = AJSONLexer()
        lexer.lexer.input(data)
        lexer.test(data)
        return
    elif mode == "parser":
        # ANÁLISIS SINTÁCTICO
        parser = AJSONParser()
        parser.test(data)
        return
    
    # ANÁLISIS LÉXICO
    print("\nLEXER: \n")
    lexer = AJSONLexer()
    lexer.lexer.input(data)
    lexer.test(data)
    print("\nLEXER ENDED!\n")

    # ANÁLISIS SINTÁCTICO
    print("\nPARSER: \n")
    parser = AJSONParser()
    parser.test(data)
    print("\nPARSER ENDED!\n")


if __name__ == "__main__": 
    try:
        if len(sys.argv) < 2:
            raise Exception
    except:
        print("Usage: python main.py <file_name> [parser|lexer]")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)