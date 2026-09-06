import os
import subprocess

valid_tests = "valid_test_files/"
invalid_tests = "invalid_test_files/"

print("\n Casos de éxito: \n")
for file_name in os.listdir(valid_tests):
    file_path = os.path.join(valid_tests, file_name)

    output = subprocess.run(["python", "main.py", file_path, "parser"], capture_output=True, text=True)
    print(output.stdout)

    if output.stderr:
        print(output.stderr)
        break

print("Casos de éxito terminados\n\n")

print("\n Casos de error: \n")

for file_name in os.listdir(invalid_tests):
    file_path = os.path.join(invalid_tests, file_name)

    output = subprocess.run(["python", "main.py", file_path, "parser"], capture_output=True, text=True)
    print(output.stdout)


print("Casos de error terminados\n")
print("Revisa la salida del programa para ver los resultados de las pruebas\n\n")
