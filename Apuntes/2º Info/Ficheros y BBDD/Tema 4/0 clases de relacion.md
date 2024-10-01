1) Persistentes: sólo se borran con una acción explícita del usuario 
	- Relaciones base: Se corresponden con el nivel lógico, tienen existencia por sí mismas y se crean de manera explícita. 
	- [[1 Vistas y usuarios]]: Se corresponden con el esquema externo, son derivadas, nominadas, no tienen datos almacenados, solo se almacena su definición en términos de otras relaciones (redundancia lógica). 
	- [[1 Vistas y usuarios|Vistas materializadas]]: Se corresponden con el nivel interno, son derivadas como las vistas, pero tienen datos almacenados (red. física). 
	- Instantáneas (snapshots): fotografía de la tabla en un momento del tiempo (almacenada físicamente); orientada al proceso atómico
2) Temporales: desaparecen al ocurrir un determinado evento (sin especificar una acción de borrado). Por ejemplo, al acabar la sesión o una transacción. Pueden ser de usuario (local temp table, cursor) o de sistema (workspace).