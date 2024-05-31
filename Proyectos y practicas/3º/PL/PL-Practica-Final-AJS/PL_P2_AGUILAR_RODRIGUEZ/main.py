"""
Autores: 
    - Raúl Aguilar Arroyo 100472050
    - Natalia Rodriguez Navarro 100471976

Módulo que coordina el lexer y el parser
"""

from modules import AJSLexer, AJSParser

def main(file_path: str, lex: bool, par: bool):
    lexer = AJSLexer()
    parser = AJSParser()
    
    if not lex and not par:
        print("usage: main.py [-h] [-lex] [-par] file")
    
    if lex:
        with open(file_path, "r") as file:
            data = file.read()
            lexer.lexer.input(data)
            
            # from the original file path replace the extension with .token
            output_file_name = file_path.split(".")[0]
            output_file_path = f"{output_file_name}.token"

            with open(output_file_path, "w") as output_file:                  
                for tok in lexer.lexer:
                    # print(f"{tok.type} {tok.value} {tok.lineno}")
                    output_file.write(f"{tok.type} {tok.value}\n")
            
    if par:
        with open(file_path, "r") as file:
            data = file.read()
            output_file_name = file_path.split(".")[0]
            output_file_path = f"{output_file_name}.symbol"
            parser.test(data, output_file_path)
    
    
    
    
def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Analizador de AJSON")
    # python ./PL_P3_{AP1}_{AP2}/main.py {input_file} -{lex| par}
    parser.add_argument("file", help="Archivo de entrada")
    parser.add_argument("-lex", action="store_true", help="Ejecutar el lexer")
    parser.add_argument("-par", action="store_true", help="Ejecutar el parser")
    return parser.parse_args()

    
if __name__ == "__main__":
    args = parse_args()
    main(args.file, args.lex, args.par)
    