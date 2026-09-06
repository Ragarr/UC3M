// si pulsas en el icono del logo ir a la pagina principal
let logo = document.getElementById("logo-block");
logo.addEventListener("click", function (event) {
    window.location.href = "/";
});

// cargar la lista de favoritos del local storage
let fav_list = document.getElementById("fav-list");
let favs = JSON.parse(localStorage.getItem("favs"));

if (favs === null) {
    favs = [];
}

// si hay duplicados en la lista de favoritos, eliminarlos
let favs_no_duplicates = [];
favs.forEach(function (fav) {
    let is_duplicate = false;
    favs_no_duplicates.forEach(function (fav_no_duplicate) {
        if (fav_no_duplicate.id === fav.id) {
            is_duplicate = true;
        }
    });
    if (!is_duplicate) {
        favs_no_duplicates.push(fav);
    }
});
favs = favs_no_duplicates;

// guardar la lista de favoritos sin duplicados
localStorage.setItem("favs", JSON.stringify(favs));



cart = JSON.parse(localStorage.getItem("cart"));
if (cart === null) {
    cart = [];
}


favs.forEach(function (item) {
    let fav_item = document.createElement("div");
    fav_item.classList.add("fav-item");
    product_url = '/mobile/pages/product-view/product_view.html?id=' + item.id;
    fav_item.innerHTML = `
        <div class="fav-item-left">
           <a href = ${product_url}><h2>${item.name}</h2></a>
        </div>
        <div class="fav-item-right">
        <p>${item.price}€</p>
        <button class = "add-to-cart-button">Añadir al Carrito</button>
        </div>
        <div class="icon-trash"></div>
    `;
    let add_to_cart_button = fav_item.querySelector(".add-to-cart-button");
    add_to_cart_button.addEventListener("click", function (event) {
        cart.push(item);
        localStorage.setItem("cart", JSON.stringify(cart));
        alert("Producto añadido al carrito");
    });
    fav_list.appendChild(fav_item);

    let pressTimer;
    let isSwipeAction = false; 

    // Función handleLongPress verifica si se ha deslizado antes de marcar como done
    const handleLongPress = () => {
      isSwipeAction = false; // Restablecer la detección de deslizamiento
    };

    // Hold en móvil
    fav_item.addEventListener("touchstart", (e) => {
      if (e.target === add_to_cart_button) return;
      e.preventDefault();
      fav_item.querySelector('.icon-trash').style.display = 'block';
      fav_item.classList.add('cart-item-pressing');
      isSwipeAction = false; // Restablecer al comenzar una nueva interacción
      pressTimer = window.setTimeout(handleLongPress, 2000);
    });

    fav_item.addEventListener("touchmove", (e) => {
      isSwipeAction = true; // Indicar que se ha detectado un deslizamiento
    });

    // Hold en ordenador
    fav_item.addEventListener("mousedown", (e) => {
      if (e.target === add_to_cart_button) return;
      e.preventDefault();
      fav_item.querySelector('.icon-trash').style.display = 'block';
      fav_item.classList.add('fav-item-pressing');
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
        fav_item.classList.remove('fav-item-pressing');
        fav_item.querySelector('.icon-trash').style.left = '100%';
      };
  
      fav_item.addEventListener("touchend", endInteraction);
      fav_item.addEventListener("mouseup", endInteraction);
      fav_item.addEventListener("mouseleave", endInteraction);
  
      // Variables para manejar el inicio y el fin del deslizamiento
      // Deslizamiento en móvil
      let originalX = 0;
      let moveX = 0;
      let isTouchMoving = false;
      let startTime = 0;

      fav_item.addEventListener("touchstart", (e) => {
        if (e.target === add_to_cart_button) return;
        originalX = e.touches[0].clientX;
        isTouchMoving = true;
        startTime = new Date().getTime(); // Capturar el tiempo de inicio del deslizamiento
        fav_item.style.position = 'relative';
        fav_item.style.transition = 'box-shadow 0.3s';
        fav_item.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
        e.preventDefault();
      }, {passive: false})
  
      fav_item.addEventListener("touchmove", (e) => {
        if (isTouchMoving) {
          moveX = e.touches[0].clientX - originalX;
          if (moveX < 0) {
            fav_item.style.left = `${moveX}px`;
          }
        }
      }, {passive: true});
  
      fav_item.addEventListener("touchend", (e) => {
          fav_item.querySelector('.icon-trash').style.display = 'none';
          isTouchMoving = false;
          fav_item.style.position = '';
          fav_item.style.left = '';
          fav_item.style.boxShadow = '';
          let endTime = new Date().getTime();
          let timeTaken = endTime - startTime;
          let speed = Math.abs(moveX) / timeTaken;
      
          if (moveX < -50 && speed > 0.5) { // Umbral de velocidad para deslizamiento a la izquierda
            // Eliminamos el producto de la lista de favoritos
            favs = favs.filter((fav) => fav.id !== item.id);
            localStorage.setItem("favs", JSON.stringify(favs));
            fav_item.style.transition = 'left 0.3s';
            fav_item.style.left = '-100%';
            fav_item.remove();
            // alert("Producto eliminado de favoritos");
          }
      });

      // Deslizamiento en ordenador
    let isDragging = false;
    let originalPosition = 0;
    let newPosition = 0;
    let mouseStartTime = 0; 

    fav_item.addEventListener("mousedown", (e) => {
      originalPosition = e.clientX;
      isDragging = true;
      mouseStartTime = new Date().getTime(); // Capturar el tiempo de inicio del deslizamiento
      fav_item.style.position = 'relative';
      fav_item.style.transition = 'box-shadow 0.3s';
      fav_item.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
      e.preventDefault();
    });

    document.addEventListener("mousemove", (e) => {
      if (isDragging) {
        newPosition = e.clientX - originalPosition;
        fav_item.style.left = `${newPosition}px`; // Mover horizontalmente
      }
    });

    document.addEventListener("mouseup", (e) => {
        if (isDragging) {
            fav_item.querySelector('.icon-trash').style.display = 'none';
            isDragging = false;
            fav_item.style.position = '';
            fav_item.style.left = '';
            fav_item.style.boxShadow = '';
            let mouseEndTime = new Date().getTime();
            let timeTaken = mouseEndTime - mouseStartTime;
            let speed = Math.abs(newPosition) / timeTaken;
    
            if (moveX < -50 && speed > 0.5) { // Umbral de velocidad para deslizamiento a la izquierda
                // Eliminamos el producto de la lista de favoritos
                favs = favs.filter((fav) => fav.id !== item.id);
                localStorage.setItem("favs", JSON.stringify(favs));
                fav_item.style.transition = 'left 0.3s';
                fav_item.style.left = '-100%';
                fav_item.remove();
                // alert("Producto eliminado de favoritos");
              }
        }
    });
});


