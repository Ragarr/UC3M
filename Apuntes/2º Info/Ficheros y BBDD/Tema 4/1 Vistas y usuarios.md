Un solo objeto (tabla) admite varias definiciones para distintos tipos de usuario. El esquema global (o relacion base) es el esquema logico global. Aparte se define una version especifica del esquema para cada usuario. Existen varios esquemas externos y un unico esquema global.
La vista puede reducir el grado y/o la cardinalidad de la relación base, e incluso fusionar varias relaciones en una sola.

# Creación de vistas
```sql
CREATE [MATERIALIZED] VIEW <nombre de tabla> 
	[(<nombre de columna> [,<nombre de columna>]…)
	AS <expresión de consulta> [WITH CHECK OPTION]
```
- Las inserciones y las **modificaciones solicitadas** sobre la vista se **realizarán sobre las tablas fuente** (involucradas en la [[3 Dinamica del SQL, DML#SINTAXIS QUERY|consulta]]).
- Las columnas obligatorias omitidas deberán adquirir un valor por otros medios (valor por defecto, o por disparador).
- La vista materializada tiene datos almacenados (conveniente si las tablas fuente son remotas, o la consulta es compleja).
- WITH CHECK OPTION comprueba en actualizaciones que ningún elemento modificado sea excluido de la vista (eoc, cancela). -> no permite meter nada que modifique la commposición de la vista (no modificar el atributo que determina si algo esta en la vista o no).
Ejemplo, en una tabla en la que haya algun tipo de registro de documentos con fecha inicio (cuando se crea el documento), fecha final (cuando se termina el documento), se pueden crear las vistas borrador y histórico  para ver los documentos no terminados y los terminados.

```sql
CREATE TABLE doc(…, fecha_ini DATE, fecha_fin DATE,…);

CREATE VIEW borrador AS 
	SELECT * FROM doc WHERE fecha_ini IS NULL;

CREATE VIEW historico AS 
	SELECT * FROM doc WHERE fecha_fin IS NOT NULL;
```

### Fusion de relaciones y atributos de tablas en vistas

```sql
CREATE TABLE refs(
	ref NUMBER(8) PRIMARY KEY,
	nombre VARCHAR2(25) NOT NULL,
	tipo VARCHAR2(5),
	coste NUMBER (8,2) NOT NULL
);
CREATE TABLE vats(
	tipo VARCHAR2(5) PRIMARY KEY,
	iva NUMBER(2,2) NOT NULL
);
CREATE VIEW productos(nombre, ref, precio) AS 
	SELECT a.nombre, a.ref, a.coste*(1+b.iva)
		FROM refs a NATURAL JOIN vats b;
```
Donde la tabla refs son  productos con sus precios, referencias y tipo de producto y la tabla vats son los impuestos que aplica a cada producto.
Creas la vista productos que te va a sacar el nombre=refs.nombre, el ref=refs.ref y el precio=refs.coste*(1+vats.iva). 
Nota: en la creación de vista en vez de refs.columna y vats.columna usan a.columna y b.columna ya que en la ultima lina ```FROM refs a NATURAL JOIN vats b;``` renombran vats y refs como b y a.

## Ejemplo de uso
en la siguiente base de datos:
```sql
CREATE TABLE empleados_ALL(
	DNI NUMBER(8) PRIMARY KEY,
	nombre VARCHAR2(25) NOT NULL,
	tlf NUMBER(9) UNIQUE,
	salario NUMBER (8,2)
);
CREATE VIEW empleados(nombre, telefono) AS 
	SELECT nombre, tlf FROM empleados_ALL;

CREATE MATERIALIZED VIEW asalariados AS 
	SELECT nombre, DNI, salario FROM empleados_ALL;
```
Diseño Externo: existen **dos perfiles de usuario: oficina y de RRHH**. los empleados deverian ver la vista empleados y RRHH deberia ver la vista materializada asalariados.

# Usuarios
## Creacion de usuarios
```sql

CREATE USER <username> IDENTIFIED BY <password>
	[DEFAULT TABLESPACE <tablespace>]
	[QUOTA <size> ON <tablespace>]
	[PROFILE <profilename>]
	[PASSWORD EXPIRE]
	[ACCOUNT {LOCK|UNLOCK}] ;

CREATE PROFILE <profilename> LIMIT <resources>; 

CREATE ROLE <rolename> 
	{NOT IDENTIFIED| IDENTIFIED BY <password>};
```
user es un usuario local.
resources es el numero de sesiones, tiempo de conexion, accesos, cpu, ram,etc que ese perfil esta autorizado a usar

## Gestion de privilegios
se pueden  GRANT (conceder) y REVOKE (revocar):
```sql
GRANT { <rolename> | <sys_privileges> | ALL PRIVILEGES } 
	TO <users/roles> [WITH ADMIN OPTION];

GRANT { <object_privileges> | ALL PRIVILEGES }
	[(column [, …])] ON [schema.]<object> TO <users/roles> 
	[WITH HIERARCHY OPTION] [WITH GRANT OPTION];

REVOKE <privileges> [ON <object>] FROM <users/roles>; 
```

