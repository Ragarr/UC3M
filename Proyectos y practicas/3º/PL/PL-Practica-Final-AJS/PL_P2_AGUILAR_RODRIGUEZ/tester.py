import subprocess
import os

def run_command_on_files(root_directory):
    print(f"Buscando archivos en: {root_directory}")
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            # Aquí puedes filtrar por tipo de archivo si es necesario, por ejemplo:
            if file.endswith(".ajs"):
                full_path = os.path.join(root, file)
                command = f"python main.py {full_path} -par -lex"
                print(f"Ejecutando: {command}")
                subprocess.run(command, shell=True)

if __name__ == "__main__":
    directory_path = "tests/"  # Cambia esto por la ruta a la carpeta deseada
    run_command_on_files(directory_path)
