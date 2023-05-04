# Diseño Relacional
- Para toda interrelación se debe especificar que regla ha de aplicarse en cada acción que haga peligrar la integridad (on Delete/ on Update)
- El conjunto de todos los esquemas de relación de una BDR, con sus interrelaciones y RI que aplican, se denomina Esquema Relacional. El diagrama que utilizamos para describirlo se llama Grafo Relacional. 
- Este diseño básico y universal se puede completar añadiendo semántica mediante diversos mecanismos ([[1 Vistas y usuarios]], [[4 Disparadores|disparadores]], [[3 Bloques y paquetes]]…)

# Documentación del diseño
- Debe completarse el grafo relacional con comentarios acerca de la cobertura semántica de la solución propuesta.
- Los supuestos semánticos explícitos son toda porción de metainformación aportada por el cliente/usuario (requisitos)
- Se debe enumerar y explicar todos los supuestos **semánticos explícitos no contemplados** (que no ha sido posible observar en el diseño propuesto (opcionalmente, se puede proponer una solución para ellos).
- El diseño suele requerir más información que la facilitada por el cliente/usuario. Los supuestos semánticos implícitos son toda porción de metainformación que incluya el diseño y afecte su cobertura (el sistema final queda limitado por ellos).
## Supuestos semánticos implícitos
Ejemplo: modela clientes con nombre y apellido(s) identificados por DNI, que poseen coche(s) (al menos uno) con matrícula, marca, modelo y color.
```
Clientes (_DNI_, Nombre, Apellido1, Apellido2*)
^                                     DC/UC
-------------------------------------------
										   ^
Coche (Matrícula, Marca, Modelo, Color, Dueño*)
```

|MAL|BIEN|
|-|-|
|No pueden existir dos clientes con el mismo DNI|Los coches se identifican por su matrícula
|El segundo apellido del cliente es opcional|Si un cliente se borra, se eliminan en cascada sus coches|
|No pueden existir dos clientes con el mismo DNI||
|Todo coche tiene un dueño||
|Todos los coches tienen marca y modelo (obligatoriamente)||
|Los DNI son cadenas alfanuméricas de 9 caracteres||

