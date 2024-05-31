# SSIIUU-Prototipado
# Autores
- Raúl Aguilar Arroyo - 100472050
- Alberto Penas Diaz - 100471939
- Arturo Soto Ruedas - 100472007
- Natalia Rodriguez Navarro - 100471976
## Acceso a la web
- Al acceder a ``ip_servidor`` se accede a la pagina que veria el cliente.
- Al acceder a ``ip_servidor/employee`` se accede a la pagina que veria un trabajador.

## Acceso y pruebas desde un movil
1. Asegurarse de que el movil este conectado a la misma red que la computadora.
2. En chrome del movil configurar lo siguiente:
   1. En la barra de direcciones escribir `chrome://flags/`
   2. Buscar la opcion `Insecure origins treated as secure`.
   3. Añadir la direccion `http://` seguido del IPv4 de el pc seguido de  (ejemplo: `http://192.168.1.40`)
   4. Reiniciar el navegador.
3. En el navegador del movil, acceder a la direccion `http://` seguido del IPv4 de el pc seguido de(lo mismo que se ha puesto arriba)

Esto es necesario para poder conceder permisos como la camara, ubicacion o NFC.

## Pruebas con NFC y QR

Para NFC se debe crear un registro de texto en el primer registro de la etiqueta, el registro debe contener un texto con el siguiente formato
```json
{
    "id": int,
    "name": str,
    "price": int,
    "quantity": int,
    "image": "str",
    "section": "str"
}
```
Ejemplo:
```json
{
    "id": 1,
    "name": "Pixel 7A",
    "price": 300,
    "quantity": 1,
    "image": "product1.jpeg",
    "section": "Electrónica" 
}
```
Los productos que reconoce el servidor son aquellos que estan en `data/products.json`

Para los codigos QR funciona de la misma manera, en cualquier pagina que genere codigos QR, crear un codigo basado en texto e introducir un texto en formato json con uno de los productos aceptados por el servidor.

El NFC es una funcion experimental y solo se ha probado en la ultima version de chrome para Android. 

Si se abre la web de cliente en modo debug en pc es posible que se den errores pues en todas las paginas se intenta acceder al nfc.

## Prueba de la funcion de abandono de local.

Para probar la funcion de abandono de local, se debe acceder al mapa y llamar desde la consola del navegador a la funcion `simulateExit()`

Tambien existe una funcion `simulateMovement(locations['nombre_seccion'].coords)` que simula el movimiento del usuario en el mapa desde su origen hasta la seccion dada.

Tambien se le puede mover desde las opciones d edebug del navegador modificando su latitud y longitud manualmente.



