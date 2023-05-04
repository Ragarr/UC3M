un bloque se refiere a un conjunto de instrucciones SQL que se ejecutan juntas como una unidad lógica de trabajo. 
En general, los bloques se utilizan para realizar operaciones complejas que involucran múltiples pasos.

# Declaración de un bloque
# Tipos de bloque
Existen los bloques nominados, de la forma:

```sql
CREATE FUNCTION|PROCEDURE suma_numeros (@numero1 INT, @numero2 INT)
RETURNS INT
AS
BEGIN
    DECLARE @resultado INT;
    
    SET @resultado = @numero1 + @numero2;
    
    RETURN @resultado;
END;
```
y los bloques no nominados

## Bloques no nominados 
los bloques no nominados se ejecutan al instante y no se almacenan en la base de datos.
Un bloque  no nominado consta de tres partes:
1.  **Declaraciones:** En la sección de declaraciones se definen todas las variables que se utilizarán en el bloque. Cada variable se declara utilizando la sintaxis "varname type;", donde "varname" es el nombre de la variable y "type" es el tipo de datos que se almacenará en la variable.
2.  **Cuerpo:** En la sección del cuerpo del bloque se escribe el código que realiza las operaciones deseadas. Aquí es donde se incluyen las instrucciones SQL y las estructuras de control (como bucles y condicionales) necesarias para ejecutar la lógica del bloque.
3.  **Excepciones:** La sección de excepciones del bloque se utiliza para manejar errores que puedan ocurrir durante la ejecución del código. Aquí se especifican las acciones a realizar si se produce una excepción, como la emisión de un mensaje de error o la ejecución de una serie de instrucciones para resolver el problema.
```sql
DECLARE 
    @total INT;
BEGIN
    SET @total = 0;

    SELECT @total = @total + cantidad
    FROM ventas
    WHERE fecha_venta >= '2022-01-01';

    PRINT 'El total de ventas desde el 1 de enero de 2022 es: ' + CONVERT(VARCHAR(10), @total);
EXCEPTION
    WHEN OTHERS THEN
        PRINT 'Se ha producido un error: ' + ERROR_MESSAGE();
END;
```
Dentro del bloque, se declaró una variable llamada "@total" y se inicializó en cero. Luego, se realizó una consulta SELECT para obtener el total de ventas desde el 1 de enero de 2022 y se almacenó en la variable "@total". Cantidad es una columna de la tabla ventas

## Bloques nominados
Los bloques nominados se almacenan en la base de datos y no necesitan DECLARE.
Existen dos tipos las function y los procedure

### funciones
Las funciones son bloques de código que se definen para realizar una tarea específica y **devolver un valor**. Una función puede tener cero o más parámetros de entrada, y siempre devuelve un valor. Las funciones se utilizan comúnmente para realizar cálculos complejos o procesamiento de datos.
```sql
CREATE FUNCTION calcular_area_circulo (@radio FLOAT)
RETURNS FLOAT
AS
BEGIN
    DECLARE @pi FLOAT;
    DECLARE @area FLOAT;
    
    SET @pi = 3.14159265;
    SET @area = @pi * @radio * @radio;
    
    RETURN @area;
END;
```
### Procedimientos
Los procedimientos almacenados son bloques de código que se definen para realizar una tarea específica, **pero no devuelven un valor**. En lugar de ello, los procedimientos pueden modificar los datos de la base de datos, generar resultados intermedios o realizar acciones que no requieren una respuesta de la base de datos.
```sql
CREATE PROCEDURE insertar_nuevo_registro (@nombre VARCHAR(50), @edad INT, @email VARCHAR(100))
AS
BEGIN
    INSERT INTO tabla_usuarios (nombre, edad, email)
    VALUES (@nombre, @edad, @email);
END;
```

# Paquetes
Es una colección de variables, funciones y procedimientos almacenados.
Se utilizan para organizar y agrupar la lógica relacionada en un solo lugar, lo que hace que sea más fácil de mantener y administrar.
## Declaracion de paquetes
Un paquete consta de dos partes: la especificación y el cuerpo. La especificación es una declaración de los objetos que el paquete contiene, como funciones y procedimientos almacenados, y define los parámetros y tipos de datos que se utilizan en el paquete. El cuerpo es el código real que implementa la lógica definida en la especificación.  (algo asi como que la especificacion son los prototipos de C y el cuerpo las funciones como tal).

Los paquetes pueden ser creados utilizando el comando CREATE PACKAGE y pueden ser modificados utilizando el comando ALTER PACKAGE. Los paquetes también pueden ser eliminados utilizando el comando DROP PACKAGE.
Tambien se puede reemplazar completamente un paquete con REPLACE PACKAGE
Ejemplo:
```sql
CREATE PACKAGE mi_paquete AS
    PROCEDURE saludar(nombre VARCHAR(50));
    FUNCTION sumar(numero1 INT, numero2 INT) RETURN INT;
END mi_paquete;

CREATE PACKAGE BODY mi_paquete AS
    PROCEDURE saludar(nombre VARCHAR(50)) IS
    BEGIN
        DBMS_OUTPUT.PUT_LINE('Hola ' || nombre || '!');
    END saludar;
    
    FUNCTION sumar(numero1 INT, numero2 INT) RETURN INT IS
        resultado INT;
    BEGIN
        resultado := numero1 + numero2;
        RETURN resultado;
    END sumar;
END mi_paquete;
```
En este ejemplo, se crea un paquete llamado "mi_paquete" que contiene una función llamada "sumar" y un procedimiento llamado "saludar". La especificación del paquete se define en la primera parte del código, mientras que el cuerpo del paquete se define en la segunda parte del código.