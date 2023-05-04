product = {"bitcoin": [300, 200, 100, 0, -50],
           "microsoft": [100, 100, 100, 100, 100],
           "apple": [-30, -10, 200, 300, 200]}
interes = [0.02, 0.03, 0.035, 0.04, 0.03]
valores_actuales = {"bitcoin": 0,
                    "microsoft": 0,
                    "apple": 0}
for k in product.keys():
    valor_actual = 0
    for n in range(len(product[k])):
        valor_actual += product[k][n] / (1 + interes[n]) ** n
    valores_actuales[k] = valor_actual
mayor = 0
key_mayor = str()
for k in valores_actuales.keys():
    if valores_actuales[k] > mayor:
        mayor = valores_actuales[k]
        key_mayor = k
print(key_mayor)
