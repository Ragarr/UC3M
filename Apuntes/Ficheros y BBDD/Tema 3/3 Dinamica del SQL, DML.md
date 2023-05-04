Las instrucciones SQL3 de manipulación pueden operar de tres modos: 
1. Interactivo (proporcionando instrucciones SQL directamente). 
2. SQL embebido: instrucciones imbuidas en lenguaje anfitrión (C, JAVA,…).
3. Módulos: llamadas explícitas a procedimientos desde procesos externos.
Operaciones de Actualización:
- Inserción de tuplas (INSERT) 
- Borrado de tuplas (DELETE) 
- Modificación de tuplas (UPDATE
Operaciones de Recuperacion
- Consulta o _Query_ (SELECT)

# Gestión transaccional en PL/SQL
**Transacción**: conjunto de instrucciones de actualización que deben ser llevadas a cabo de modo atómico (como conjunto, “o todo o nada”).

Instrucciones: COMMIT (realizar) y ROLLBACK (deshacer)
 - COMMIT \[WORK]
 - ROLLBACK \[WORK] \[TO \[SAVEPOINT] \<savepoint>] 
 - SAVEPOINT \<savepoint>

# SINTAXIS QUERY
 ```
 [WITH
	 <simbolo> AS <subquery>
	 [,simbolo AS <subquieru>...]]
	SELECT [ALL|DISTINCT] <lista de seleccion>
	FROM <clausula de origen>
	[WHERE <condicion>]
	[GROUP BY <expresion> [HAVING <condicion>]]
	[{UNION| UNION ALL|MINUS|INTERSECT} <query>]
	[ORDER BY <expresion> [ASC|DESC]];
```
lo que está entre corchetes es opcional![[Pasted image 20230312164650.png]]

## Proyeccion en el query
-  la proyección se refleja en la \<LISTA DE SELECCION>
	- Lista de datos (del workspace) separados por comas.
	- Puede ser todo el área de trabajo (\*) o bien incluir:
		- atributos del esquema de relación del área de trabajo 
		- pseudo-columnas, como ROWNUM y table.ROWID,... 
		-  constantes (como 1 o 'X') y variables ligadas (:NEW, …) 
		- funciones: aplicadas sobre lo anterior (o nularias)
			- aritméticas (+, -, …), strings (||, SUBSTR, …), codificación (CASE, NVL, …), conversión (TO_CHAR, …), sistema (SYSDATE, USER, …), … 
			- de agregación (reciben un colectivo y devuelven un solo valor) 
			- funciones compiladas (de usuario o procedentes de paquetes)
- Admite renombrado elemento AS alias

## Area de trabajo (workspace)
Es una tabla temporal (vinculada a la ubicación de los datos)
- La cláusula FROM define el área de trabajo (que es una tabla)
- Puede componerse de una tabla, o varias tablas combinadas.
- Dado que el área de trabajo es una tabla, un caso particular de tabla en la clausula FROM es otro área de trabajo, es decir, otra consulta (subquery)
- Admite renombrado (obligatorio en self-joins)
- Existen diversas combinaciones
- 
## Combinaciones
### Combinación Elemental: el Producto Cartesiano
	- FROM Gente CROSS JOIN Clientes… $\equiv$ FROM Gente, Clien
### Combinación General JOIN:
todas las columnas de ambas tablas
- FROM people \[INNER] JOIN clients \[ ON (= \[AND...] )] - sin especificación: equijoin por todos los pares de columnas que cumplan la expresion (=,!=,<,>,...)
### Combinación natural: 
no duplica las columnas incluidas en la igualdad
- FROM X NATURAL \[INNER] JOIN Y...
	- Combinación Natural por pares de columnas que se llamen igual en ambas tablas
- FROM X \[INNER] JOIN Y USING (\<columns>)...
	- Combinación Natural por pares de columnas especificados (que se llaman igual…)
		
## Consultas: otras combinaciones

### Combinación sin pérdidas, Combinación Externa (outer):
- FROM Gente {LEFT|RIGHT|FULL} \[OUTER] JOIN Clientes  \[USING <\columnas> | ON \<col_a>=\<col_b> \[AND...]]
	- Mismo uso que la (inner) JOIN; 'outer' es opcional (recomendable por claridad)... 
- FROM X LEFT OUTER JOIN Y... 
	- Combinación Externa por la izquierda (se respetan todas las tuplas de la primera tabla) 
- FROM X RIGHT JOIN Y... 
	- Combinación Externa por la derecha (se respetan todas las tuplas de la segunda tabla) 
- ... FROM X FULL OUTER JOIN Y... 
	- Combinación Externa completa (se respetan todas las tuplas de ambas tablas)

### Combinación por una union:
- FROM Gente UNION JOIN Clientes
	- Observación: ambos esquemas deben ser compatibles

## Expresión condicional WHERE
(WHERE) puede ser:
- una comparación de expresiones (=, !=, <, >, <=, >=)
- comprobación de inclusion test (en un rango): <expresión> \[NOT] BETWEEN <expresión> AND <expresión>
- comprobación de valor nulo: <expresión> IS \[NOT] NULL
- test de semejanza (patrón): <expresión_char> \[NOT] LIKE <patrón>
- expresión lógica: {NOT, AND, OR} a partir de otras expresiones condicionales
- test de existencia: EXISTS subquery
- test de inclusión (en un conjunto dado, o en una subquery): <expresión> \[NOT] IN {<expresión_list>|subquery}
SUBQUERIES en la cláusula WHERE: pueden ser ineficientes
- EXISTS se detiene en el primer encaje, pero se ejecuta anidado siempre. 
- IN puede optimizarse (no ejecutar anidado); conviene moverlo a la cl. WITH 
- NOT IN puede usarse en anti-combinaciones (si se hace de modo eficiente)

## Agrupación
La cláusula GROUP BY define el criterio de agrupación.

El área de trabajo agrupada puede incluir columnas del criterio de agrupación y funciones de agregación sobre el resto.

Algunas funciones de agregación: 
- COUNT, AVG, SUM, MIN, MAX, CONCAT (LISTAGG), ... 
- MEDIAN, VARIANCE, STDDEV, CORR, COVAR, etc.
Admiten dos tipos de condiciones: 
- condición individual (WHERE) ejercida antes de agrupar; 
- condición colectiva (HAVING) sobre la tabla ya agrupada

Ejemplos de Agrupacion y orden
![[Pasted image 20230312172141.png]]