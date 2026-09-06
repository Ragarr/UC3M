# Clave Ajena
Atributo (o conjunto de atributos)  de una relación (**relación referenciante**)  que se asocia con otro atributo (u otros tantos atributos)  de otra relación (**relación referenciada**) y su valuación se restringe a **valores existentes en el atributo referenciado** valor nulo.

## Tipos de Integridad: (con FK multiatributo) 
- **Completa** (match full): todo es nulo, o nada lo es 
- **Parcial** (match partial): lo no nulo debe existir (en una fila, al menos) 
- **Débil** (match simple): si hay nulos, no comprueba (def. en Oracle DB)
## Restricciones

- Elección de **clave primaria** (PRIMARY KEY) 
- Elección de **clave(s) alternativa**(s) (UNIQUE) 
- **Obligatoriedad** (NOT NULL) 
- **[[1 Asociacion Entre Relaciones#Reglas de integridad referencial|Reglas de integridad referencial]]**: regla a aplicar cuando exista el riesgo de romper la integridad referencial, tanto en operaciones de borrado como de modificación. 
- **[[1 Asociacion Entre Relaciones#Semántica de rechazo|Restricciones Semánticas de Rechazo]]**

## Reglas de integridad referencial
Acciones de rechazo o de corrección automática aplicadas para evitar que se pierda la integridad referencial (valores de las claves ajenas no válidos)
- **Restrict** (operación restringida): R si la operación **involucra padres con hijos**, **no se lleva a cabo** 
- **No Action** (operación cancelada): NA si la operación **rompe la integridad referencial, no se lleva a cabo **
- **Cascade** (propagación en cascada): C los valores **no validos serán actualizados también en la clave ajena** 
- **Set Null** (puesta a nulo): SN los valores **no válidos serán sustituidos por el valor nulo** 
- **Set Default** (valor por defecto): SD los valores **no válidos serán sustituidos por un valor por defecto**

## Semántica de rechazo
Son expresiones condicionales que siempre debe cumplir la BD. Ante una operación de actualización (inserción/modificación/borrado) se comprueba la condición, y si no la cumple se rechaza la operación.

Se distinguen dos tipos: **Simple** y **Aserción** (restricción general)

### Simple
Se aplica a un solo elemento relacional (dominio/relación/tupla) 
Sintaxis: 
```
CHECK <condicion>
```
En particular, en una tabla se aplica sólo a la fila que está siendo operada. Es parte de la implementación del elemento. Ejemplo:
```
CREATE TABLE ALUMNO ( 
	NIA CHAR(9), 
	NOTA NUMBER(2,0),
	... 
	CONSTRAINT ck_nota_num CHECK (nota BETWEEN 0 AND 10));
```

### Aserción (no existe en Oracle DB)
Es una restricción general (se impone sobre la BD). Afecta a distintos elementos relacionales (varias tablas, varias filas, …). 
Es en sí misma un elemento independiente (debe tener un nombre asignado). 
Se ejecutan después de toda operación de actualización sobre la BD.
**¡Alto coste computacional!** -> casi ningún SGBDR las implementa
En su lugar, se utilizan los [[4 Disparadores| Disparadores]]
Sintaxis (en sql generico, en **oracle no existe**):
```
CREATE ASSERTION  <nombre> CHECK <Condición>

CREATE ASSERTION SUELDO_INFORMATICO_MES CHECK NOT EXISTS 
	(SELECT ‘X’ FROM EMPLEADOS A JOIN DEPARTAMENTO B 
		ON (A.dep= B.cod_dep) 
		WHERE B.puesto=‘Informatico’ and A.sueldo<3000);
```

# Dominios y tipos de dato
- El concepto de dominio es útil para completar la definición del modelo, pero suele quedarse en el plano teórico. 
- En la mayoría de las implementaciones, se cuenta con el concepto de tipo de datos: conjunto de datos de la misma naturaleza y que tiene una operabilidad definida. 
- Los tipos de datos se pueden clasificar por su: 
	- Naturaleza: Numéricos, Alfanuméricos, Fechas y Binarios 
	- Implementación: Nativos; de Usuario (derivados); y Externos (paq.) 
	- Operabilidad: comparables, aritmética, agregables, … 
- El concepto de dominio se asemeja al de tipo de datos derivado, definido como un tipo nativo (restringido por implementación) con una, ninguna o varias restricciones semánticas de rechazo.