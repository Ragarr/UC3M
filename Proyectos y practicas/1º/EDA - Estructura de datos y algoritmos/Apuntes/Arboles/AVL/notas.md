un arbol AVL esta ddiseñado para equilibrar arboles.

se puede equilibrar un arbol en tamaño(no entra) y en altura .

es bueno   comprobar si se ha desequilibrado y equilibrar el arbol despues de cada insercion o eliminacion
## rotaciones
### rotacion simple derecha
es cuando tienes la pata larga a la izquierda y todos los hijos estan a la izquierda rotamos el nodo desequilibramos, ej:
```  
                25     20
              20|     25|15
            15|
```
### rotacion simple izquierda
lo mismo pero al reves

### rotacion doble izquierda derecha

```
          30          30         20
        10|   ->    20|   ->    10|30
         |20      10|
```
