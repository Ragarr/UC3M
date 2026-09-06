// si pulsas en el icono del logo ir a la pagina principal
let logo = document.getElementById("logo-block");
logo.addEventListener("click", function (event) {
    window.location.href = "/";
});


// cargar el carrito de la compra del local storage
let cart_list = document.getElementById("cart-list");
let cart = JSON.parse(localStorage.getItem("cart"));
let total = 0;
let total_items = 0;

let pending_order = null;

if (cart === null) {
    cart = [];
}

// si hay duplicados en la lista de productos, combinarlos
// sumando las cantidades
let cart_no_duplicates = [];

cart.forEach(function (item) {
    let is_duplicate = false;
    cart_no_duplicates.forEach(function (cart_no_duplicate) {
        if (cart_no_duplicate.id === item.id) {
            is_duplicate = true;
            cart_no_duplicate.quantity += item.quantity;
        }
    });
    if (!is_duplicate) {
        cart_no_duplicates.push(item);
    }
});
cart = cart_no_duplicates;

// actualizar el carrito en el localStorage
localStorage.setItem("cart", JSON.stringify(cart));


cart.forEach(function (item) {
    let cart_item = document.createElement("div");
    cart_item.classList.add("cart-item");
    cart_item.setAttribute('data-id', item.id); 
    product_url = '/mobile/pages/product-view/product_view.html?id=' + item.id;
    cart_item.innerHTML = `
        <div class="icon-favourite"></div>
        <div class="item-left-side">
            <a  href = ${product_url}><h2 class = product-link >${item.name}</h2></a>
            <p>Precio/Ud: ${item.price}€</p>
        </div>
        <div class="item-right-side">
           <div class="cart-item-quantity">
                <img src="/mobile/media/minus-button.svg" class = cart-item-remove-button>
                <p class="cart-item-quantity-value">${item.quantity}</p>
                <img src="/mobile/media/add-button.svg" class = cart-item-add-button>
            </div>
            <div class = product-total>
                <p>Total:</p>
                <p>${Math.round(item.price * item.quantity * 100)/100}€</p>
            </div>
        </div>
        <div class="icon-trash"></div>
    `;

    cart_list.appendChild(cart_item);
    total += item.price * item.quantity;
    total_items += item.quantity;

    // Agregar event listeners a los botones de "Agregar" y "Eliminar"
    const addButton = cart_item.querySelectorAll('.cart-item-add-button');
    const removeButton = cart_item.querySelectorAll('.cart-item-remove-button');

    addButton.forEach(button => {
        button.addEventListener('click', () => {
            updateQuantity('add', item, cart_item);
        });
    });

    removeButton.forEach(button => {
        button.addEventListener('click', () => {
            updateQuantity('remove', item, cart_item);
        });
    });

    product_link = cart_item.querySelectorAll('.product-link');
    

    /* --------- DESLIZAMIENTOS ----------------- */

    let pressTimer;
    let isSwipeAction = false; 

    // Función handleLongPress verifica si se ha deslizado antes de marcar como done
    const handleLongPress = () => {
      isSwipeAction = false; // Restablecer la detección de deslizamiento
    };

    // Hold en móvil
    cart_item.addEventListener("touchstart", (e) => {
      if (Array.from(addButton).includes(e.target) || Array.from(removeButton).includes(e.target) || Array.from(product_link).includes(e.target)){
        return;
      }

        e.preventDefault();

      cart_item.classList.add('cart-item-pressing');
      isSwipeAction = false; // Restablecer al comenzar una nueva interacción
      pressTimer = window.setTimeout(handleLongPress, 2000);
    });

    cart_item.addEventListener("touchmove", (e) => {
      isSwipeAction = true; // Indicar que se ha detectado un deslizamiento
    });

    // Hold en ordenador
    cart_item.addEventListener("mousedown", (e) => {
      e.preventDefault();
      cart_item.classList.add('cart-item-pressing');
      isSwipeAction = false; // Restablecer al comenzar una nueva interacción
      pressTimer = window.setTimeout(handleLongPress, 2000);
    });

    document.addEventListener("mousemove", (e) => {
      if (e.movementX !== 0 || e.movementY !== 0) {
        isSwipeAction = true; // Indicar que se ha detectado un movimiento con el ratón
      }
    });

    // Eventos para finalizar la interacción
    const endInteraction = () => {
      clearTimeout(pressTimer);
      cart_item.classList.remove('cart-item-pressing');
      cart_item.querySelector('.icon-favourite').style.right = '100%';
      cart_item.querySelector('.icon-trash').style.left = '100%';
    };

    cart_item.addEventListener("touchend", endInteraction);
    cart_item.addEventListener("mouseup", endInteraction);
    cart_item.addEventListener("mouseleave", endInteraction);

    // Variables para manejar el inicio y el fin del deslizamiento
    // Deslizamiento en móvil
    let originalX = 0;
    let moveX = 0;
    let isTouchMoving = false;
    let startTime = 0;

    cart_item.addEventListener("touchstart", (e) => {
      if (Array.from(addButton).includes(e.target) || Array.from(removeButton).includes(e.target) || Array.from(product_link).includes(e.target)) return;
      originalX = e.touches[0].clientX;
      isTouchMoving = true;
      startTime = new Date().getTime(); // Capturar el tiempo de inicio del deslizamiento
      cart_item.style.position = 'relative';
      cart_item.style.transition = 'box-shadow 0.3s';
      cart_item.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
      e.preventDefault();
    }, {passive: false})

    cart_item.addEventListener("touchmove", (e) => {
      if (isTouchMoving) {
        moveX = e.touches[0].clientX - originalX;
        cart_item.style.left = `${moveX}px`;
      }
    }, {passive: true});

    cart_item.addEventListener("touchend", (e) => {
        isTouchMoving = false;
        cart_item.style.position = '';
        cart_item.style.left = '';
        cart_item.style.boxShadow = '';
        let endTime = new Date().getTime();
        let timeTaken = endTime - startTime;
        let speed = Math.abs(moveX) / timeTaken;
    
        if (moveX > 50 && speed > 0.5) { // Umbral de velocidad para deslizamiento a la derecha
            addToFavourites(item);
            // alert("Producto añadido a favoritos");
        } else if (moveX < -50 && speed > 0.5) { // Umbral de velocidad para deslizamiento a la izquierda
            removeFromCart(item, cart_item);
        }
    });
    


    // Deslizamiento en ordenador
    let isDragging = false;
    let originalPosition = 0;
    let newPosition = 0;
    let mouseStartTime = 0; 

    cart_item.addEventListener("mousedown", (e) => {
      if (e.target === addButton || e.target === removeButton) return;
      originalPosition = e.clientX;
      isDragging = true;
      mouseStartTime = new Date().getTime(); // Capturar el tiempo de inicio del deslizamiento
      cart_item.style.position = 'relative';
      cart_item.style.transition = 'box-shadow 0.3s';
      cart_item.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
      e.preventDefault();
    });

    document.addEventListener("mousemove", (e) => {
      if (isDragging) {
        newPosition = e.clientX - originalPosition;
        cart_item.style.left = `${newPosition}px`; // Mover horizontalmente
      }
    });

    document.addEventListener("mouseup", (e) => {
        if (isDragging) {
            isDragging = false;
            cart_item.style.position = '';
            cart_item.style.left = '';
            cart_item.style.boxShadow = '';
            let mouseEndTime = new Date().getTime();
            let timeTaken = mouseEndTime - mouseStartTime;
            let speed = Math.abs(newPosition) / timeTaken;
    
            if (newPosition > 50 && speed > 0.5) { // Umbral de velocidad para deslizamiento a la derecha
                addToFavourites(item);
                alert("Producto añadido a favoritos");
            } else if (newPosition < -50 && speed > 0.5) { // Umbral de velocidad para deslizamiento a la izquierda
                removeFromCart(item, cart_item);
            }
        }
    });
    
    /* ------------- FIN DESLIZAMIENTOS ---------------------- */

});


let cart_total_price = document.getElementById("total-price"); // es un parrafo

cart_total_price.innerHTML = `Total: ${Math.round(total*100)/100} €`;

let cart_total_items = document.getElementById("total-items"); // es un parrafo

cart_total_items.innerHTML = `Productos en el carrito: ${total_items}`;

// Función para actualizar la cantidad de un producto en el carrito
function updateQuantity(operation, item, cart_item) {
    const quantityElement = cart_item.querySelector('.cart-item-quantity-value');
    if (operation === 'add') {
      item.quantity++;
    } else if (operation === 'remove') {
      item.quantity--;
    }
    quantityElement.textContent = item.quantity;

    // Actualizar el total y el total de artículos
    total = 0;
    total_items = 0;
    cart.forEach(item=> {
      total += item.price * item.quantity;
      total_items += item.quantity;
    });
    
    if (item.quantity === 0) {
      // Eliminar el producto del carrito si la cantidad llega a 0
      const index = cart.findIndex(i => i.id === item.id);
      cart.splice(index, 1);
      cart_item.remove();
    }
  
    // Actualizar el carrito en el localStorage
    localStorage.setItem("cart", JSON.stringify(cart));

    // Actualizar los totales en la página
    cart_total_price.innerHTML = `Total: ${Math.round(total*100)/100} €`;
    cart_total_items.innerHTML = `Productos en el carrito: ${total_items}`;
}


// Funcion para eliminar producto del carrito
function removeFromCart(item, cart_item) {

    const index = cart.findIndex(i => i.id === item.id);
    cart.splice(index, 1);
    cart_item.remove();
    
    item.quantity = 0;

    // Actualizar el total y el total de artículos
    total = 0;
    total_items = 0;
    cart.forEach(item=> {
      total += item.price * item.quantity;
      total_items += item.quantity;
    });
    
    // Actualizar el carrito en el localStorage
    localStorage.setItem("cart", JSON.stringify(cart));

    // Actualizar los totales en la página
    cart_total_price.innerHTML = `Total: ${Math.round(total*100)/100} €`;
    cart_total_items.innerHTML = `Productos en el carrito: ${total_items}`;
}


// Función para añadir un producto a favoritos
function addToFavourites(item) {
    let favourites = JSON.parse(localStorage.getItem("favs"));
    if (favourites === null) {  
        favourites = [];
    }
    favourites.push(item);
    localStorage.setItem("favs", JSON.stringify(favourites));
}


buy_button = document.getElementById("buy-button");
const socket = io();


buy_button.addEventListener("click", function (event) {
    if (cart === null || cart.length === 0) {
        alert("No hay productos en el carrito");
        return;
    }
    // mostrar popup
    let popup = document.getElementById("tramitar-pedido-popup");
    popup.style.display = "flex";

});
// si pulsas fuera 


let select_payment = document.getElementById("payment-method");

if (select_payment.value === "pay-at-cashier") {
    document.getElementById("payment-form").style.display = "none";
}
else {
    document.getElementById("payment-form").style.display = "flex";
}


select_payment.addEventListener("change", function (event) {
    console.log("cambio");
    let payment = select_payment.value;
    let payment_form = document.getElementById("payment-form");
    if (payment === "pay-at-cashier") {
        payment_form.style.display = "none";        
    }
    else {
        payment_form.style.display = "flex";
    }
});


select_delivery = document.getElementById("delivery-method");

if (select_delivery.value === "home-delivery") {
    document.getElementById("delivery-form").style.display = "flex";
}
else {
    document.getElementById("delivery-form").style.display = "none";
}


select_delivery.addEventListener("change", function (event) {
    let delivery = select_delivery.value;
    let delivery_form = document.getElementById("delivery-form");
    if (delivery === "home-delivery") {
        delivery_form.style.display = "flex";        
    }
    else {
        delivery_form.style.display = "none";
    }
});



cancel_button = document.getElementById("cancel-button");

cancel_button.addEventListener("click", function (event) {
    let popup = document.getElementById("tramitar-pedido-popup");
    popup.style.display = "none";
});


// if you click outside the popup, close it
window.addEventListener("click", function (event) {
    let popup = document.getElementById("tramitar-pedido-popup");
    if (event.target === popup) {
        popup.style.display = "none";
    }
});


confirm_button = document.getElementById("confirm-button");

confirm_button.addEventListener("click", function (event) {
    let payment = select_payment.value;
    let delivery = select_delivery.value;
    
    let order_id = Math.floor(Math.random() * 100000000);
    

    let payment_data = {};
    let delivery_data = {};

    if (payment === "pay-at-cashier") {
        payment_data = {
            payment: "pay-at-cashier"
        };
    }
    else {
        let card_number = document.getElementById("card-number").value;
        let card_expiration = document.getElementById("card-expiration").value;
        let card_cvv = document.getElementById("card-cvc").value;

            payment_data = {
            payment: "credit-card",
            card_number: card_number,
            card_expiration: card_expiration,
            card_cvv: card_cvv

        };
        // NO HACER NADA, ES UNA SIMULACION
    }

    if (delivery === "home-delivery") {
        let delivery_address = document.getElementById("delivery-address").value;
        let delivery_number = document.getElementById("delivery-number").value;
        let delivery_city_code = document.getElementById("delivery-city-code").value;
        let delivery_city = document.getElementById("delivery-city").value;
        delivery_data = {
            delivery: "home-delivery",
            address: delivery_address,
            number: delivery_number,
            city_code: delivery_city_code,
            city: delivery_city

        };
    }
    else {
        delivery_data = {
            delivery: "store-pickup"
        };

    }
    let order = {
        payment: payment_data,
        delivery: delivery_data,
        cart: cart,
        id: order_id
    };
    pending_order = order;
    console.log("pedido realizado", order);
    socket.emit("new-order", order);

    // esperar respuesta del servidor, mostrar pantalla de espera mientras

    let popup = document.getElementById("tramitar-pedido-popup");
    popup.style.display = "none";

    let loading_popup = document.getElementById("loading-popup");
    loading_popup.style.display = "flex";
    
});

socket.on("order-confirmed", function (data) {
    // ocultar pantalla de espera

    // comprobar que si el pedido pendiente era para recogida en tienda
    if (pending_order.delivery.delivery === "store-pickup" || pending_order.delivery.delivery === "store-pickup") {
        // generar codigo qr para la recogida en tienda
        popup_width = document.getElementById("loading-popup").offsetWidth;

        let qr_code = new QRious({
            element: document.getElementById("qr-code"),
            value: JSON.stringify(pending_order),
            size: 500
        });
        // get the span qr-code-text
        let qr_code_text = document.getElementById("qr-code-text");
        qr_code_text.innerHTML = "Escanea el codigo QR en la tienda para recoger tu pedido";
        
    }

    let loading_popup = document.getElementById("loading-popup");
    loading_popup.style.display = "none";
    // mostrar pantalla de confirmacion
    let confirmation_popup = document.getElementById("confirmation-popup");
    confirmation_popup.style.display = "flex";
    // limpiar el carrito
    localStorage.removeItem("cart");
    cart_list.innerHTML = "";
    cart_total_price.innerHTML = `Total: 0 €`;
    cart_total_items.innerHTML = `Productos en el carrito: 0`;
    pending_order = null;
});

socket.on("order-canceled", function (data) {
    // ocultar pantalla de espera
    let loading_popup = document.getElementById("loading-popup");
    loading_popup.style.display = "none";
    // mostrar pantalla de cancelacion
    let cancel_popup = document.getElementById("cancel-popup");
    cancel_popup.style.display = "flex";
    // limpiar el carrito
    localStorage.removeItem("cart");
    cart_list.innerHTML = "";
    cart_total_price.innerHTML = `Total: 0 €`;
    cart_total_items.innerHTML = `Productos en el carrito: 0`;
    pending_order = null;
});


error_button = document.getElementById("error-button");

error_button.addEventListener("click", function (event) {
    let cancel_popup = document.getElementById("cancel-popup");
    cancel_popup.style.display = "none";
});

confirmation_button = document.getElementById("confirmation-button");

confirmation_button.addEventListener("click", function (event) {
    let confirmation_popup = document.getElementById("confirmation-popup");
    confirmation_popup.style.display = "none";
});



