# SSIIUU-Prototipado

Al acceder a localhost:3000 se muestra la pagina que veria el cliente.
Al acceder a localhost:3000/employee se muestra la pagina que veria un trabajador.


Tener en cuenta que el contenido estatico se sirve a traves de la carpeta www, por lo que las rutas de los archivos estaticos deben ser relativas a esta carpeta.
(imagenes, css, js, etc.)

## Para poder hacer pruebas desde el movil
1. Asegurarse de que el movil este conectado a la misma red que la computadora.
2. En la terminal de la computadora, ejecutar el comando `ipconfig` y buscar la direccion IPv4 de la red a la que esta conectada.
3. En chrome del movil configurar lo siguiente:
   1. En la barra de direcciones escribir `chrome://flags/`
   2. Buscar la opcion `Insecure origins treated as secure`.
   3. Añadir la direccion `http://` seguido del IPv4 de el pc seguido de `:3000` (ejemplo: `http://192.168.1.40:3000`)
   4. Reiniciar el navegador.
4. En el navegador del movil, acceder a la direccion `http://` seguido del IPv4 de el pc seguido de `:3000` (lo mismo que se ha puesto arriba)

Si estas pensando que solucionar esto seria buena idea, el problema es que para poder usar un protocolo seguro (https) se necesita un certificado SSL, y para obtener uno se necesita primero un dominio y luego pagar por el certificado. Por lo que jajano.

## Formato de los elementos en el carrito:

Nota: los elementos del carrito deben tener el siguiente formato:
Por favor asegurarse de que no haya mas de 512 caracteres en total en el objeto ya que
las etiquetas NFC que tenemos solo tienen 512 bytes de capacidad.

```json
{
    "id": 1,
    "name": "Producto 1",
    "price": 100,
    "quantity": 1,
    "image": "producto1.png"
}
```

los codigos qr y nfc deben contener la informacion en el formato especificado para que no explote todo.


## Formato de un pedido

```json

{
  payment: {
    payment: 'credit-card',
    card_number: '13123',
    card_expiration: '123',
    card_cvv: '2313'
  },
  delivery: { delivery: 'store-pickup' },
  cart: [ { id: 1, name: 'Producto 1', price: 100, quantity: 5 } ]
}
```


# TODO


- Poder mover de carrito a favoritos deslizando
- Poder eliminar productos del carrito deslizando
- Implementar el mapa
  - Implementar ir al mapa desde el buscador
  - Implementar ir al mapa desde la vista de producto
  - Poder mover de favoritos a carrito deslizando y con boton
- Poder eliminar productos de favoritos deslizando
- Implementar el abandono de la tienda (ir a la vista de carrito y confirmar pedido) -> mira en figma

- (Opcional)Implementar la lectura de QRS en la web del empleado confirmar la entrega y pago de pedidos.
**Para comprobar el diseño de cualquier caracteristica mirarlo en figma.**


[FIGMA PROTOTIPO](https://www.figma.com/proto/vo7b7Sc3BehGrQRPY6Fei3/Corte-Ingles?node-id=1-90&scaling=scale-down&page-id=0%3A1&starting-point-node-id=1%3A90&mode=design&t=QhwPaj25K3U17OXc-1)