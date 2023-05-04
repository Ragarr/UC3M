# Funciones que nos dan:
## Read command
Es la funcion encargada de pedir el comando al usuario, luego lo analiza y te lo da chopeadito por argvv y alguna info util.
```
int read_command(char ***argvv, char **filev, int *bg);
```
### Parametros
####  char \*\*\*argvv

Es una estructura que contiene los mandatos introducidos por el
usuario (osea el usuario hace lo siguiente:`char ***argvv = NULL`, y nos pasan `&argvv` para que los escribamos nosotros) . Por ejemplo el primer mandato es `argvv[0][0]`, el segundo es `argvv[1][0]`, luego cada elemento se accede con el segundo indice: `argvv[i][0]` es el primer elemento del mandato i, `argvv[i][1]` es el segundo elemento del mandato i.
#### char \*\*filev
Es una estructura que contiene los nombres de los ficheros usados  
en las redirecciones o, si no existe, cadena con un cero (“0”).  

- `filev[0]` Cadena que contiene el nombre del fichero usado  
para la redirección de entrada (<)  
- `filev[1]` Cadena que contiene el nombre del fichero usado para  
la redirección de salida (>)  
- `filev[2]` Cadena que contiene el nombre del fichero usado para  
la redirección de salida de error (! >)  

#### int \*in_background
Es una variable que indica si se ejecutan los mandatos en  
background .

Sus valores son:  
- in_background = 0 −→Si no se ejecuta en background  
- in_background = 1 −→Si se ejecuta en background (&)  

### Devuelve:
- 0 →En caso de EOF (CTRL + C).
- -1 →En caso de error.
- n →Número de mandatos introducidos.
### Ejemplos:
- ls | sort →Devuelve 2.
- s | sort > fich →Devuelve 2.
- ls | sort & →Devuelve 2.
- cat <input_file →Devuelve 1.

