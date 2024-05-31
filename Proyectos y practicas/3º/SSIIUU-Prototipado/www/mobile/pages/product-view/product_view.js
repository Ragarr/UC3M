function obtainProductId() {
    let params = new URLSearchParams(window.location.search);
    let product_id = params.get("id");
    return product_id;
}


function displayProduct(product) {
    product_image = document.getElementById("product-image");
    product_image.src = "/product_images/" + product.image;
    product_name = document.getElementById("product-name");
    product_name.textContent = product.name;
    product_price = document.getElementById("product-price");
    product_price.textContent = product.price
} 

let cart = [];
let favs = [];
let product = null;

window.onload = function () {
    let product_id = obtainProductId();
    cart = JSON.parse(localStorage.getItem("cart"));
    if (cart == null) {
        cart = [];
    }

    favs = JSON.parse(localStorage.getItem("favs"));
    if (favs == null) {
        favs = [];
    }
    
    // get the product from the server
    socket = io();
    socket.on("product", (product_response) => {
        console.log("Producto obtenido:", product_response);
        if (product_response.error) {
            console.error(product_response.error);
            return;
        }
        product = product_response;
        displayProduct(product_response);
        checkIfProductIsInFavorites();
        
    });

    socket.emit("get-product", product_id);

}

function addProductToCart() {
    if (product == null) {
        console.error("No se ha obtenido el producto");
        return;
    }
    cart.push(product);
    localStorage.setItem("cart", JSON.stringify(cart));
    console.log("Producto añadido al carrito");
    alert("Producto añadido al carrito");
}

function addProductToFavorites() {
    if (product == null) {
        console.error("No se ha obtenido el producto");
        return;
    }
    favs.push(product);
    localStorage.setItem("favs", JSON.stringify(favs));
    console.log("Producto añadido a favoritos");
    //alert("Producto añadido a favoritos");
    add_to_favorite.style.fill = "red";
}

function removeProductFromFavorites() {
    if (product == null) {
        console.error("No se ha obtenido el producto");
        return;
    }
    favs.forEach((fav, index) => {
        if (fav.id == product.id) {
            favs.splice(index, 1);
            localStorage.setItem("favs", JSON.stringify(favs));
            console.log("Producto eliminado de favoritos");
            // alert("Producto eliminado de favoritos");
            add_to_favorite.style.fill = "none";
            return;
        }
    });
}


function toggleFavorite() {
    if (product == null) {
        console.error("No se ha obtenido el producto");
        return;
    }
    let b = false;
    favs.forEach((fav, index) => {
        if (fav.id == product.id) {
            removeProductFromFavorites();
            b = true; // por alguna razón, no se hace el return en el forEach 
            return;
        }
    });
    if (!b){
        addProductToFavorites();
    }
}     


add_to_cart_img = document.getElementById("cart");


add_to_cart_img.addEventListener("click", addProductToCart);


add_to_favorite = document.getElementById("add-to-fav");

add_to_favorite.addEventListener("click", () => {
    if (product == null) {
        console.error("No se ha obtenido el producto");
        return;
    }
    toggleFavorite();
});


go_to_map = document.getElementById("go-to-map");

go_to_map.addEventListener("click", () => {
    console.log("Redirigiendo a la página del mapa");
    mapUrl = `/mobile/pages/map/map.html?section=${product.section}`
    window.location.href = mapUrl;
});

// on double click, add to favorites, for phone
let lastTouchEnd = 0;
function doubleClickHandler(){
    let now = new Date().getTime();
    if (now - lastTouchEnd <= 300) {
        addProductToFavorites();
    }
    lastTouchEnd = now;

}


product_image = document.getElementById("product-image");
product_image.addEventListener("touchend", doubleClickHandler, false);

produc_info = document.getElementsByClassName("product-info")[0];
produc_info.addEventListener("touchend", doubleClickHandler, false);



// if product is in favorites, change the color of the favorite button
function checkIfProductIsInFavorites() {
    if (product == null) {
        console.error("No se ha obtenido el producto");
        return;
    }
    favs.forEach((fav) => {
        if (fav.id == product.id) {
            add_to_favorite.style.fill = "red";
        }
    });
}
