disparador (trigger en inglés) es un objeto de base de datos que se utiliza para activar automáticamente un conjunto de acciones o instrucciones cuando se produce un evento específico en una tabla o vista de la base de datos.
Los disparadores se utilizan comúnmente para mantener la integridad de los datos.
## Declaración de disparadores
Los disparadores se definen en una tabla o vista y se activan automáticamente cuando se produce un evento específico en la tabla o vista, como una inserción, actualización o eliminación de datos. Cuando se activa el disparador, se ejecutan las acciones o instrucciones que se han definido para el evento específico.

Ejemplo1:
```sql
CREATE TRIGGER tr_actualizar_stock
AFTER INSERT ON pedidos_detalle
FOR EACH ROW
BEGIN
  UPDATE productos
  SET stock = stock - NEW.cantidad
  WHERE id = NEW.producto_id;
END;
/
```
Ejemplo2:
```sql
CREATE OR REPLACE TRIGGER presupuesto_departamento
	AFTER INSERT ON EMPLEADO
	FOR EACH ROW
	BEGIN
		UPDATE DEPARTAMENTO
			SET presupuesto = presupuesto + :NEW.sueldo
			WHERE cod_dep = :NEW.dep ;
		INSERT INTO tabla_control
			VALUES(:NEW.cod_emp,USER,SYSDATE);
END;
/
```
### Sintaxis general:
```sql
CREATE TRIGGER nombre_del_disparador
{BEFORE | AFTER} {INSERT | UPDATE | DELETE} ON nombre_de_la_tabla
[FOR EACH ROW]
BEGIN
  -- acciones a realizar cuando se activa el disparador
/
```
-   `nombre_del_disparador`: el nombre del disparador que se va a crear.
-   `BEFORE`,  `AFTER` o`INSTEAD OF`: indica si el disparador se activará antes o después del evento de inserción, actualización o eliminación. "INSTEAD OF" : debe ejecutar el bloque de acciones del disparador en lugar de la operación que activó el disparador.
-   `INSERT`, `UPDATE` o `DELETE`: indica el tipo de evento que activará el disparador.
-   `nombre_de_la_tabla`: el nombre de la tabla o vista en la que se activará el disparador.
-   `FOR EACH ROW` (opcional): si no se pone la accion se ejecutara una sola vez después de la actualización, independientemente del número de filas actualizadas. Pero si se incluye la cláusula "FOR EACH ROW", se ejecutará una vez por cada fila actualizada.
	Es importante tener en cuenta que el uso de la cláusula "FOR EACH ROW" puede afectar el rendimiento de la base de datos si se usa incorrectamente, ya que puede hacer que el disparador se ejecute muchas veces para operaciones que afectan a muchas filas. Por lo tanto, es importante usar la cláusula con precaución y solo cuando sea necesario para lograr los objetivos deseados del disparador.
-   `BEGIN` y `END`: encierran el bloque de acciones que se ejecutarán cuando se active el disparador.

## notita
En el instead of
:NEW en un trigger referencia a "la tabla" que se va a insertar en la tabla x
:OLD lo mismo pero referencia a los valores viejos

# Insercion en vistas
Si quiero controlar como se inserta en una vista puedo restringir la insercion en la vista y añadir el control sobre como quiero que se haga la insercion mediante triggers.
