const express = require('express');
const app = express();
const path = require('path');
const server = require('http').Server(app); // Cambiar a 'http' en lugar de 'https'
const io = require('socket.io')(server);


let orders = [];

// read the products from data/products.json (is a JSON array)

let products = require('./data/products.json');
console.log(products);

// Definir directorio de archivos estáticos
app.use(express.static(path.join(__dirname, 'www')));


// Página web para el cliente
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'www', 'mobile', 'mobile.html'));
});

// Página web para el empleado
app.get('/employee', (req, res) => {
  res.sendFile(path.join(__dirname, 'www', 'employee', 'employee.html'));
});

// Conexión de Socket.IO
io.on('connection', (socket) => {
  console.log('Un usuario se ha conectado');

  // Ejemplo de manejo de mensajes
  socket.on('new-order', (order) => {
    orders.push(order);
    console.log('Compra realizada:', order);
    // Puedes emitir un mensaje de vuelta al cliente si es necesario
    io.emit('purchase', { mensaje: order });
  });

  socket.on('get-orders', () => {
    console.log('Enviando pedidos al empleado');
    orders.forEach((order) => {
      io.emit('purchase', { mensaje: order });
    });
  });

  // Maneja la solicitud de búsqueda de productos
  socket.on('search', (searchTerm) => {
    // Filtra los productos que coinciden con el término de búsqueda
    const matchingProducts = products.filter(product =>
      product.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    // Envía los resultados de la búsqueda de vuelta al cliente
    socket.emit('search-results', matchingProducts);
  });

  // Manejar la desconexión
  socket.on('disconnect', () => {
    console.log('Cliente desconectado');
  });

  socket.on('confirmed-by-employee', (order) => {
    console.log('Pedido confirmado por el empleado:', order);
    // eliminar el pedido de la lista
    orders.forEach((o, index) => {
      if (o.id === order.id) {
        orders.splice(index, 1);
      }
    });
    io.emit('order-confirmed', { mensaje: order });
  });

  socket.on('canceled-by-employee', (order) => {
    console.log('Pedido cancelado por el empleado:', order);
    // eliminar el pedido de la lista
    orders.forEach((o, index) => {
      if (o.id === order.id) {
        orders.splice(index, 1);
      }
    });
    io.emit('order-canceled', { mensaje: order });
  });
  
  socket.on('get-product', (product_id) => {
    
    // Aquí puedes realizar una consulta a la base de datos
    // y enviar el producto al cliente
    let product = null;
    products.forEach((p) => {
      if (p.id == product_id) {
        product = p;
      }
    });

    console.log('Obtener producto:', product_id, product);
    if (product) {
      socket.emit('product', product);
    } else {
      socket.emit('product', { error: 'Producto no encontrado' });
    }
    
  });
});








// Iniciar el servidor con HTTP
const PORT = process.env.PORT || 80;
server.listen(PORT, () => {
  console.log(`Servidor corriendo en el puerto ${PORT}`);
});
