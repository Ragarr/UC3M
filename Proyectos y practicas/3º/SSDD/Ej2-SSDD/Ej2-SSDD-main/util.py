import os

def fusionar_archivos(root_folder, output_file):
    with open(output_file, 'w') as output:
        for root, _, files in os.walk(root_folder):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    output.write(f'{file_path}:\n')
                    output.write(f.read())
                    output.write('\n')

# Especifica la carpeta raíz y el archivo de salida
carpeta_raiz = 'tests'
archivo_salida = 'tests_fusion.txt'

fusionar_archivos(carpeta_raiz, archivo_salida)
