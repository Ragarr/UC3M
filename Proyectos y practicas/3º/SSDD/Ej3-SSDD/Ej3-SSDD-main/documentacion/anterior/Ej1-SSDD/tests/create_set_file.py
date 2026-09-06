import random

GENERAR = 100000 # NUMERO MUY GRANDE PARA PROGAR LA CONCURRENCIA
set_path = "sets.txt"

def generar_conjunto(clave, texto, num_floats):
  """Genera un conjunto de datos en formato 'set'."""
  floats = [random.uniform(0, 100) for _ in range(num_floats)]
  return f"set {clave:03} \"{texto}\" {num_floats} {' '.join(map(str, floats))}"

def main():
  """Genera y escribe conjuntos de datos en un archivo."""
  
  with open(set_path, "w") as archivo:
    # write init in the first line
    archivo.write("init\n")

    for i in range(1, GENERAR):
      clave = f"{i:03}"
      texto = f'Texto al azar {i}'
      num_floats = random.randint(1, 31)
      conjunto = generar_conjunto(clave, texto, num_floats)
      archivo.write(f"{conjunto}\n")

if __name__ == "__main__":
  main()
