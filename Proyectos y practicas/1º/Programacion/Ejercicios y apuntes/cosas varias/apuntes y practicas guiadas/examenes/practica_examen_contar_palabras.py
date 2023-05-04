texto = "a hola me llamo  raul "
espacios = 0
texto = texto.strip()
for i in range(len(texto)):
    if i > 0 and texto[i] == " " and texto[i - 1] != " ":
        espacios+=1
palabras = espacios + 1
print(palabras)
