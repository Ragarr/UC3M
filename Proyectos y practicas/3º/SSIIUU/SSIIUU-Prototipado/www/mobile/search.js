let search_bar_input = document.getElementById("search-bar-input");

search_bar_input.addEventListener("focus", function (event) {
    let search_popup = document.getElementsByClassName("search-popup")[0];
    let main_content = document.getElementById("main-content");
    let results = document.querySelector(".results");
    if (event.target.value === "") {
        results.style.display = "none";
    } else {
        results.style.display = "block";
    }
    search_popup.style.display = "block";
    main_content.style.display = "none";
    console.log("menu selected");
});

// cuando pulses escape se cierra el menu de busqueda y se deselecciona el input
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        let search_popup = document.getElementsByClassName("search-popup")[0];
        let main_content = document.getElementById("main-content");
        let results = document.querySelector(".results");
        results.style.display = "none";
        search_popup.style.display = "none";
        main_content.style.display = "block";
        search_bar_input.blur();
    }
});

// si pulsas el boton atras en el movil se cierra el menu de busqueda y se deselecciona el input
window.addEventListener("popstate", function (event) {
    let search_popup = document.getElementsByClassName("search-popup")[0];
    let main_content = document.getElementById("main-content");
    let results = document.querySelector(".results");
    results.style.display = "none";
    search_popup.style.display = "none";
    main_content.style.display = "block";
    search_bar_input.blur();
});

// si pulsas en el icono del logo se reinicia la pagina
let logo = document.getElementById("logo-block");
logo.addEventListener("click", function (event) {
    window.location.reload();
});

// crear un local storage para guardar el carrito
let cart = [];

// si existe un carrito en el local storage lo cargamos
if (localStorage.getItem("cart")) {
    cart = JSON.parse(localStorage.getItem("cart"));
} else {
    localStorage.setItem("cart", JSON.stringify(cart));
}

// Obtén una referencia al input de búsqueda y a la sección de sugerencias
const searchInput = document.getElementById("search-bar-input");
const searchResults = document.querySelector(".search-results");
const results = document.querySelector(".results");

// Inicializa una conexión con Socket.IO
const socket = io();

// Agrega un event listener al input de búsqueda
searchInput.addEventListener("input", function (event) {
    // Emite un evento al servidor a través de Socket.IO
    if (event.target.value !== "") {
        socket.emit("search", event.target.value);
    } else {
        results.style.display = "none";
    }
});

// Escucha el evento 'search-results' del servidor
socket.on("search-results", (products) => {
    // Limpia las sugerencias de búsqueda existentes
    console.log(products);
    searchResults.innerHTML = "";

    if (products.length === 0) {
        // Mostrar mensaje de "No se ha encontrado ningún producto"
        const noResultsMessage = document.createElement("li");
        noResultsMessage.textContent = "No se ha encontrado ningún producto";
        searchResults.appendChild(noResultsMessage);
    } else {
        // Agrega las nuevas sugerencias de búsqueda
        products.forEach((product) => {
            const suggestion = document.createElement("li");
            const link = document.createElement("a");
            link.classList.add("search-suggestion");
            link.href =
                "/mobile/pages/product-view/product_view.html?id=" + product.id;
            link.textContent = product.name;
            console.log("Link", link.href);
            suggestion.appendChild(link);
            searchResults.appendChild(suggestion);
        });
    }

    // Muestra la sección de sugerencias de búsqueda
    searchResults.style.display = "block";
    results.style.display = "block";
});

// Obtén una referencia a los enlaces de categoría
const searchSuggestions = document.querySelectorAll('.search-suggestion');

// Agrega un event listener a cada enlace de categoría
searchSuggestions.forEach(suggestion => {
  suggestion.addEventListener('click', (event) => {
    event.preventDefault(); // Evita que se siga el enlace por defecto
    const categoryName = event.target.textContent;
    redirectToMapPage(categoryName);
  });
});

// Función para redirigir al usuario a la página map.html
function redirectToMapPage(categoryName) {
  window.location.href = `/mobile/pages/map/map.html?section=${encodeURIComponent(categoryName)}`;
}
