get_path = "gets.txt"
set_path = "sets.txt"


def leer_conjunto(linea):
  """Extracts the key and text from a set, handling unexpected formats."""
  elementos = linea.split()  # Split the line
  clave = elementos[1]  # Get the first element (clave)
  texto = ' '.join(elementos[2:-1])  # Combine remaining elements for text
  

  return clave, texto

def generar_get(clave):
  """Generates a 'get' command line for a key."""
  return f"get {clave}"

def main():
  """Generates and writes 'get' commands in a file, handling potential errors."""
  with open(set_path, "r") as archivo_conjuntos:
    with open(get_path, "w") as archivo_gets:
      for linea in archivo_conjuntos:
        if "init" in linea:
          continue
        try:
          clave, texto = leer_conjunto(linea)
          comando_get = generar_get(clave)
          archivo_gets.write(f"{comando_get}\n")
        except IndexError:  # Handle cases with less than 4 elements
          print(f"Error: Line '{linea}' has less than expected elements.")

if __name__ == "__main__":
  main()
