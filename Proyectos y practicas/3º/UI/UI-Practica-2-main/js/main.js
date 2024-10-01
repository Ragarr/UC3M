// VARIABLES GLOBALES
var current_order_step = 0; // Paso actual del pedido
var remainingTime = 600; // Tiempo restante en segundos
var interval; // Intervalo de tiempo para actualizar el temporizador
var contenido_pedido = []; // Contenido del pedido nombre_plato: cantidad
var slideIndex = {};
var interval_carrusel = {};
var startTime = null; // Hora de inicio del temporizador
// Llama a la función de inicialización para cada carrusel
var carruselIds = ["carrusel1", "carrusel2", "carrusel3", "carrusel4", "carrusel5"];
for (var i = 0; i < carruselIds.length; i++) {
    initializecarrusel(carruselIds[i]);
  }
current_user = null; // Usuario actual

document.addEventListener("DOMContentLoaded", function () {
    // Mostramos las galerías
    for (var i = 0; i < carruselIds.length; i++) {
        showSlides(1, carruselIds[i]);
      }

    // Apertura y cierre del popup de registro
    const openRegButton = document.getElementById("open_reg");
    const closeRegButton = document.getElementById("close_reg");
    openRegButton.addEventListener("click", openRegPopup);
    closeRegButton.addEventListener("click", closeRegPopup);

    // Input en los campos del formulario de registro
    const dni_input = document.getElementById("dni");
    dni_input.addEventListener("input", dniInput);
    const nombre_input = document.getElementById("nom_ap");
    nombre_input.addEventListener("input", nameInput);
    const telf_input = document.getElementById("telf");
    telf_input.addEventListener("input", telfInput);
    const email_input = document.getElementById("email");
    email_input.addEventListener("input", emailInput);

    // Apertura y cierre del popup de pedido
    const openPedidoButton = document.getElementById("open_pedido");
    const closePedidoButton = document.getElementById("close_pedido");
    openPedidoButton.addEventListener("click", openPedidoPopup);
    closePedidoButton.addEventListener("click", closePedidoPopup);

    // Cierre de los popup cuando el usuario hace click fuera de ellos
    window.addEventListener("click", function (event) {
        if (event.target === reg_popup) {
            closeRegPopup();
        } else if (event.target === pedido_popup) {
            closePedidoPopup();
        }
    });
    

    // Botones de seleccion del pedido
    const platosMenu = document.querySelectorAll('.plato_menu');
    platosMenu.forEach(plato => {
        var botonMas = plato.querySelector('.añadir_producto');
        var botonMenos = plato.querySelector('.eliminar_producto');
        botonMas.addEventListener('click', añadir_producto);
        botonMenos.addEventListener('click', quitar_producto);
    });

    // Limpiar el carrito
    const limpiarCarrito = document.getElementById("limpiar_selecciones");
    limpiarCarrito.addEventListener("click", resetProductos);

    // Botones de navegación entre pasos
    const bc_revisar = document.getElementById("bc_revisar");
    const bc_seleccionar = document.getElementById("bc_seleccionar");
    const bc_estado = document.getElementById("bc_estado");

    bc_revisar.addEventListener("click", irRevisar);
    bc_seleccionar.addEventListener("click", irSeleccionar);
    bc_estado.addEventListener("click", irEstadoBc);

    const botonIrPaso1 = document.getElementById("btn_ir_paso_1");
    const botonIrPaso2 = document.getElementById("btn_ir_paso_2");
    const botonIrPaso3 = document.getElementById("btn_ir_paso_3");

    botonIrPaso1.addEventListener("click", irSeleccionar);
    botonIrPaso2.addEventListener("click", irRevisar);
    botonIrPaso3.addEventListener("click", irEstado);

    // Boton cancelar
    const botonCancelar = document.querySelectorAll(".btn_cancelar");
    botonCancelar.forEach(boton => {boton.addEventListener("click", cancelarPedido);});
    const botonFinalizar = document.getElementById("btn_finalizar");
    botonFinalizar.addEventListener("click", closePedidoPopup);

    // Submit registro
    const botonSubmit = document.getElementById("submit_reg");
    botonSubmit.addEventListener("click", register);

    // Animación scroll
    const page2 = document.getElementById("page2");
    const page3 = document.getElementById("page3");
    const page4 = document.getElementById("page4");
    animateScroll(page2);
    window.addEventListener("scroll", function () {
        animateScroll(page2);
        animateScroll(page3);
        animateScroll(page4);
    });

    // Menú de hamburguesa
    const dropdownTitle = document.querySelector('.menu_de_hamburguesa .title');
    const dropdownOptions = document.querySelectorAll('.menu_de_hamburguesa .option');

    // Vincula listeners al menú de hamburguesa
    dropdownTitle.addEventListener('click', toggleMenuDisplay);
    dropdownOptions.forEach(option => option.addEventListener('click',handleOptionSelected));

    // Botón identíficate
    const identificate = document.getElementById("open_reg_2");
    identificate.addEventListener('click', openRegPopup2);

    // formulario de reserva
    const nombre_input2 = document.getElementById("nom_ap2");
    nombre_input2.addEventListener("input", nameInput);
    const telf_input2 = document.getElementById("telf2");
    telf_input2.addEventListener("input", telfInput);
    const fecha_input = document.getElementById("fecha");
    fecha_input.addEventListener("input", dateInput);
    const hora_input = document.getElementById("hora");
    hora_input.addEventListener("input", horaInput);

});



class Plato{
    constructor (nombre, precio, cantidad){
        this.nombre = nombre;
        this.precio = precio;
        this.cantidad = cantidad;
    }
}
class Pedido{
    constructor (usuario, contenido){
        this.usuario = usuario;
        this.contenido = contenido;
    }
}

// REGISTRO
function openRegPopup() {
    const reg_popup = document.getElementById("reg_popup");
    reg_popup.style.display = "flex";
    reg_popup.style.visibility = "visible";
    document.body.style.overflow = "hidden";
}
function openRegPopup2() {
    // Simulamos click en botón principal
    open_reg.click();
}
function closeRegPopup() {
    const reg_popup = document.getElementById("reg_popup");
    reg_popup.style.display = "none";
    document.body.style.overflow = "auto";
    const form = reg_popup.querySelector("form");
    form.reset();
}


class User{
    constructor (dni, nombre, telf, email){
        this.dni = dni;
        this.nombre = nombre;
        this.telf = telf;
        this.email = email;
    }
}


function register(event){
    // se acciona cuando se pulsa submit en el formulario de registro
    event.preventDefault();
    const dni = document.getElementById("dni").value;
    const nombre = document.getElementById("nom_ap").value;
    const telf = document.getElementById("telf").value;
    const email = document.getElementById("email").value;
    const reg_bot = document.getElementById("open_reg");
    const identificate_btn = document.getElementById("open_reg_2");
    
    var user = new User(dni, nombre, telf, email);
    
    // comprobar si el usuario ya existe
    var users = JSON.parse(localStorage.getItem("users"));
    if (users == null){
        users = [];
    }
    var index = users.findIndex(user => user.dni === dni);
    if (index != -1){
        alert("El usuario ya existe, se ha iniciado sesión automáticamente");
        reg_bot.innerText = "Ya estás registrado";
        reg_bot.disabled = true;
        identificate_btn.innerText = user.nombre;
        identificate_btn.disabled = true;
        current_user = user;
        closeRegPopup();
        return;
    }
    if (!checkRegister()){
        alert("El formulario no es válido");
        return;
    }
    users.push(user);
    localStorage.setItem("users", JSON.stringify(users));

    // change the name of the button from "Registrarse" to "Registrado"
    reg_bot.innerText = "Ya estás registrado";
    reg_bot.disabled = true;

    current_user = user;

    // cambiamos texto "Identifícate" a el nombre del ususario
    identificate_btn.innerText = current_user.nombre;
    identificate_btn.disabled = true;

    // close the popup
    closeRegPopup();
    alert("Usuario registrado correctamente");

}
function checkRegister(){
    // check all inputs are valid and return true if they are
    var valid = true;
    const dni = document.getElementById("dni").value;
    const nombre = document.getElementById("nom_ap").value;
    const telf = document.getElementById("telf").value;
    const email = document.getElementById("email").value;

    // check dni
    const DNI_pattern = /^[0-9]{8}[A-Z]{1}$/;
    // Letras que toma el DNI dependiendo del resto
    const letras = ['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B',
        'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E'];
    if (!DNI_pattern.test(dni)) {
        valid = false;
    } else {
        // Obtenemos los números
        var numDNI = parseInt(dni.substring(0, 8));
        // Obtenemos la letra
        var letraDNI = dni.substring(8, 9);
        // Calculamos la letra correspondiente al número
        var letraCorrecta = letras[numDNI % 23];
        if (letraDNI !== letraCorrecta) {
            valid = false;
        } else {
            valid = true;
        }
    }
    // check nombre
    const name_pattern = /(^[A-ZÁÉÍÓÚ]{1}([a-zñáéíóú]+){1,})(\s[A-ZÁÉÍÓÚ]{1}([a-zñáéíóú]+){1,})(\s[A-ZÁÉÍÓÚ]{1}([a-zñáéíóú]+){0,})?$/;
    if (!name_pattern.test(nombre)) {
        valid = false;
    }
    // check telf
    const telf_pattern = /^[0-9]{9}$/;
    if (!telf_pattern.test(telf)) {
        valid = false;
    }
    // check email
    const email_pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (!email_pattern.test(email)) {
        valid = false;
    }

    return valid;
}

function dniInput(event){
    const DNI_pattern = /^[0-9]{8}[A-Z]{1}$/
    // Letras que toma el DNI dependiendo del resto
    const letras = ['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 
                    'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E'];

    var dni = document.getElementById("dni").value;
    var dni_input = document.getElementById("dni");

    // Comprobamos si el DNI tiene 8 dígitos y una letra
    if (!DNI_pattern.test(dni)) {
        dni_input.setCustomValidity("El DNI debe tener 8 dígitos y 1 letra");
    } else {
        // Obtenemos los números
        var numDNI = parseInt(dni.substring(0, 8));
        // Obtenemos la letra
        var letraDNI = dni.substring(8, 9);
        // Calculamos la letra correspondiente al número
        var letraCorrecta = letras[numDNI % 23];

        if (letraDNI !== letraCorrecta) {
            dni_input.setCustomValidity("El DNI no es correcto");
        } else {
            dni_input.setCustomValidity(""); // La entrada es válida
        }
    }
    dni_input.reportValidity();
}

function nameInput(event){
    // patron: Nombre Apellido1 
    const name_pattern = /(^[A-ZÁÉÍÓÚ]{1}([a-zñáéíóú]+){1,})(\s[A-ZÁÉÍÓÚ]{1}([a-zñáéíóú]+){1,})(\s[A-ZÁÉÍÓÚ]{1}([a-zñáéíóú]+){0,})?$/;
    
    var input = event.target;
    var nombre = input.value;

    if (!name_pattern.test(nombre)){
        input.setCustomValidity("El nombre no es válido, debe empezar por una mayúscula y estar acompañado\
                                        de al menos una minúscula. Debe facilitar al menos un apellido \
                                        empezando por mayúscula y acompañado como mínimo de una minúscula.\
                                        El nombre y los apellidos deben separarse con un espacio.");
    } else {
        input.setCustomValidity("");
        console.log("nombre válido");
    }
    input.reportValidity();
}


function telfInput(event){
    // patron: 9 dígitos
    const telf_pattern = /[9,8]{1}[1-8]{1}[0-9]{7}/;

    var input = event.target;
    var telf = input.value;

    if (!telf_pattern.test(telf)){
        input.setCustomValidity("El teléfono no es válido, los télefonos fijos \
                                    empiezan por 9 u 8 siguiendo el formato 9AX XX XX XX o \
                                    8AX XX XX XX, siendo A una cifra distinta de 0 o de 9.");
    } else {
        input.setCustomValidity("");
    }
    input.reportValidity();
}


function dateInput(event){
    // revisar que la fecha es válida
    var input = event.target;
    var fecha = input.value;

    if (fecha == ""){
        input.setCustomValidity("Debe introducir una fecha");
    } else {
        input.setCustomValidity("");
    }
    // comprobar que la fecha es posterior a la actual
    var fecha_actual = new Date();
    var fecha_seleccionada = new Date(fecha);
    if (fecha_seleccionada < fecha_actual){
        input.setCustomValidity("La fecha debe ser posterior a la actual");
    } else {
        input.setCustomValidity("");
    }
    input.reportValidity();
}

function horaInput(event){
    // revisar que la hora es válida
    var input = event.target;
    var hora = input.value;
    console.log(hora);
    // formato hora HH:MM
    // comprobar que es posterior a las 12 y anterior a las 23
    if (hora == ""){
        input.setCustomValidity("Debe introducir una hora");
    }
    var hora_actual = new Date().getHours();
    var hora_seleccionada = parseInt(hora.split(":")[0]);
    if (hora_seleccionada < 12 || hora_seleccionada > 23){
        input.setCustomValidity("El restaurante no se encuentra abierto en la hora seleccionada.\
                                La hora debe ser posterior a las 12h y anterior a las 23h");
    } else {
        input.setCustomValidity("");
    }
    input.reportValidity();
}


function emailInput(event){
    // patron: email
    const email_pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    var email = document.getElementById("email").value;
    var email_input = document.getElementById("email");

    if (!email_pattern.test(email)){
        email_input.setCustomValidity("El email no es válido, debe seguir un patrón como el\
                                     del ejemplo. Nombre, seguido de @, seguido del dominio, \
                                     seguido de ., seguido de la extensión");
    } else {
        email_input.setCustomValidity("");
    }
    email_input.reportValidity();
}

// RELIZAR PEDIDO
function openPedidoPopup() {

    if (current_user == null){
        alert("Debes iniciar sesión para realizar un pedido");
        return;
    }

    const pedido_popup = document.getElementById("pedido_popup");
    pedido_popup.style.display = "flex";
    pedido_popup.style.visibility = "visible";
    document.body.style.overflow = "hidden";
}
function closePedidoPopup() {
    const pedido_popup = document.getElementById("pedido_popup");
    pedido_popup.style.display = "none";
    pedido_popup.style.overflow = "none"; // Restablece el desplazamiento de la página principal
    document.body.style.overflow = "auto"; // Restablece el desplazamiento de la página principal
}
function resetProductos() {
    var platosMenu = document.querySelectorAll('.plato_menu');
    try{
        platosMenu.forEach(plato => {
            var contador = plato.querySelector('.contador');
            if (contador){
                contador.innerText = "0";
            }
        });
    }catch (error){
        console.log("No se ha podido restablecer el contador de los productos: " + error);
    }
    contenido_pedido = [];
    actualizarContadorCarrito(); // Restablecer el contador del carrito
}
// botones de seleccion del pedido
function añadir_producto(event) {
    // añadir producto y cantidad al diccionario
    var contador = event.target.parentNode.querySelector('.contador');
    var platoMenu = event.target.closest('.plato_menu');
    var nombre_plato = platoMenu.querySelector('.nombre_plato').innerText;
    var precio_plato = platoMenu.querySelector('.precio').innerText;
    var cantidad = parseInt(contador.innerText);

    // find the index of the element
    var index = contenido_pedido.findIndex(plato => plato.nombre === nombre_plato);

    if (index == -1) {
        contenido_pedido.push(new Plato(nombre_plato, precio_plato, ++cantidad));
    }
    else {
        contenido_pedido[index].cantidad += 1;
    }
    
    contador.innerText = parseInt(contador.innerText) + 1;
    actualizarContadorCarrito();
}
function quitar_producto(event) {
    var contador = event.target.parentNode.querySelector('.contador');
    var platoMenu = event.target.closest('.plato_menu');
    var nombre_plato = platoMenu.querySelector('.nombre_plato').innerText;
    
    // find the index of the element
    var index = contenido_pedido.findIndex(plato => plato.nombre === nombre_plato);
    if (index == -1) {
        return; // No se ha encontrado el elemento
    }
    if (contenido_pedido[index].cantidad <= 1) {
        contenido_pedido.splice(index, 1);
        contador.innerText = "0";
    }
    else {
        contenido_pedido[index].cantidad -= 1;
        contador.innerText = parseInt(contador.innerText) - 1;
    }
    actualizarContadorCarrito();
}

function actualizarContadorCarrito() {
    var carrito = document.getElementById("carrito");
    var contador = 0;
    for (var i = 0; i < contenido_pedido.length; i++) {
        contador += contenido_pedido[i].cantidad;
    }
    carrito.innerText = contador;
}

// funciones de navegación en los pasos del pedido
// ir al paso 1
function irSeleccionar() {
    if (current_order_step == 3) {
        alert("No puedes editar un pedido ya realizado");
        return; // No se puede volver al paso 1 si no se ha pasado por el paso 2
    }
    const Paso1 = document.getElementById("seleccionar_productos");
    const Paso2 = document.getElementById("revision_pedido");
    const miga_paso_2 = document.getElementById("bc_revisar");
    const carrito = document.getElementById("carrito_container");
    Paso2.style.visibility = "hidden";
    Paso2.style.display = "none";
    Paso1.style.visibility = "visible";
    Paso1.style.display = "flex";
    carrito.style.visibility = "visible";
    carrito.style.display = "flex";
    current_order_step = 1; // Paso actual del pedido
}
// ir al paso 2
function irRevisar() {
    const Paso1 = document.getElementById("seleccionar_productos");
    const Paso2 = document.getElementById("revision_pedido");
    const Paso3 = document.getElementById("estado_pedido");
    const miga_paso_1 = document.getElementById("bc_seleccionar");
    const miga_paso_2 = document.getElementById("bc_revisar");
    const miga_paso_3 = document.getElementById("bc_estado");

    const carrito = document.getElementById("carrito_container");

    Paso1.style.visibility = "hidden";
    Paso1.style.display = "none";
    Paso3.style.visibility = "hidden";
    Paso3.style.display = "none";
    carrito.style.visibility = "hidden";
    carrito.style.display = "none";
    Paso2.style.visibility = "visible";
    Paso2.style.display = "flex";
    miga_paso_2.style.color = "#01447e";
    if (current_order_step != 3) {
        miga_paso_3.style.color = "#b3bec9";
    }
    if (current_order_step == 1) {
        current_order_step = 2; // Paso actual del pedido
    }
    actualizar_lista_pedido();
}
function actualizar_lista_pedido() {
    const lista_pedido = document.getElementById("lista_pedido");
    lista_pedido.innerHTML = "";
    for (i = 0; i < contenido_pedido.length; i++) {
        var plato = contenido_pedido[i];
        var nombre = plato.nombre;
        var precio = plato.precio;
        var cantidad = plato.cantidad;
        var platoHTML = `
        <div class="plato_menu">
            <p class="nombre_plato">${nombre}</p>
            <p class="precio">${precio} - x${cantidad}</p>
        </div>`;
        lista_pedido.innerHTML += platoHTML;
    }
    actualizar_total_pedido();
}
function actualizar_total_pedido() {
    const total_pedido = document.getElementById("precio_total");
    var total = 0;
    for (i = 0; i < contenido_pedido.length; i++) {
        var plato = contenido_pedido[i];
        var precioTexto = plato.precio;
        var precioNumero = parseFloat(precioTexto.replace('$', ''));
        var cantidad = plato.cantidad;
        console.log(precioNumero, cantidad);
        total += precioNumero * cantidad;
    }
    total_pedido.innerText = "Total: $" + total.toFixed(2);
}

// ir al paso 3
function irEstado() {
    const Paso2 = document.getElementById("revision_pedido");
    const Paso3 = document.getElementById("estado_pedido");
    const miga_paso_1 = document.getElementById("bc_seleccionar");
    const miga_paso_2 = document.getElementById("bc_revisar");
    const miga_paso_3 = document.getElementById("bc_estado");


    // comprobar si hay elementos en el pedido
    if (contenido_pedido.length == 0) {
        alert("No hay elementos en el pedido");
        return;
    }

    
    Paso2.style.visibility = "hidden";
    Paso2.style.display = "none";
    Paso3.style.visibility = "visible";
    Paso3.style.display = "flex";
    miga_paso_2.style.color = "#01447e";
    miga_paso_3.style.color = "#01447e";
    current_order_step = 3; // Paso actual del pedido
    // Iniciamos el contador inmediatamente para evitar el delay
    updateTimer();
    if (!interval) {
        interval = setInterval(updateTimer, 1000);
    }
    miga_paso_2.innerText = "Revisar pedido";
    miga_paso_1.style.textDecoration = "line-through";
    miga_paso_1.style.color = "#b3bec9";

    // guardar el pedido en el local storage
    var pedidos = JSON.parse(localStorage.getItem("pedidos"));
    if (pedidos == null){
        pedidos = [];
    }
    var pedido = new Pedido(current_user, contenido_pedido);
    pedidos.push(pedido);
    localStorage.setItem("pedidos", JSON.stringify(pedidos));

}

function irEstadoBc() {
    if (current_order_step != 3) {
        return; // No se puede ir al paso 3 si no se ha pagado ya
    }
    irEstado();
}

function cancelarPedido() {
    console.log("cancelar pedido");
    current_order_step = 0;
    resetProductos();
    resetPedidoPopup();
    // reestablecer migas, temporizador y visibilidad de los pasos
    const Paso1 = document.getElementById("seleccionar_productos");
    const Paso2 = document.getElementById("revision_pedido");
    const Paso3 = document.getElementById("estado_pedido");
    const miga_paso_1 = document.getElementById("bc_seleccionar");
    const miga_paso_2 = document.getElementById("bc_revisar");
    const miga_paso_3 = document.getElementById("bc_estado");
    const carrito = document.getElementById("carrito_container");
    Paso1.style.visibility = "visible";

    Paso1.style.display = "flex";
    Paso2.style.visibility = "hidden";
    Paso2.style.display = "none";
    Paso3.style.visibility = "hidden";

    Paso3.style.display = "none";
    carrito.style.visibility = "visible";
    carrito.style.display = "flex";
    miga_paso_1.style.color = "#01447e";
    miga_paso_2.style.color = "#b3bec9";
    miga_paso_3.style.color = "#b3bec9";

    miga_paso_1.style.textDecoration = "none";
    miga_paso_2.innerText = "Revisar pedido";
    // reestablecer el temporizador
    clearInterval(interval);
    remainingTime = 600;
    interval = null;
    const timer = document.getElementById("timer");
    timer.textContent = "10:00";
    const barra_progreso = document.getElementById("barra_progreso");
    barra_progreso.style.width = "100%";

    closePedidoPopup();
}

function resetPedidoPopup() {
    // reestablecer los colores de las migas de pan
    const miga_paso_1 = document.getElementById("bc_seleccionar");
    const miga_paso_2 = document.getElementById("bc_revisar");
    const miga_paso_3 = document.getElementById("bc_estado");
    miga_paso_1.style.color = "#01447e";
    miga_paso_2.style.color = "#b3bec9";
    miga_paso_3.style.color = "#b3bec9";
    miga_paso_1.style.textDecoration = "none";
    miga_paso_2.innerText = "Revisar pedido";
    // reestablecer el temporizador
    clearInterval(interval);
    remainingTime = 600;
    interval = null;
    const timer = document.getElementById("timer");
    timer.textContent = "10:00";
    const barra_progreso = document.getElementById("barra_progreso");
    barra_progreso.style.width = "100%";
}

function updateTimer() {
    
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;
    timer.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

    if (remainingTime <= 0) {
        clearInterval(interval);
        timer.textContent = "0:00";
    } else {
        remainingTime--;
    }
    // actualizar barra de progreso
    const barra_progreso = document.getElementById("barra_progreso");
    const porcentaje = (remainingTime / 600) * 100;
    // Usamos requestAnimationFrame para sincronizar las actualizaciones
    requestAnimationFrame(() => {
        barra_progreso.style.width = porcentaje + "%";
    });
}


// Carrusel de imagenes

// Agrega una función para inicializar los índices de cada carrusel
function initializecarrusel(carruselId) {
    slideIndex[carruselId] = 1;
    // Iniciamos el carrusel automático
    interval_carrusel[carruselId] = startAutocarrusel(carruselId);
}
function plusSlides(n, carruselId) {
    showSlides(slideIndex[carruselId] += n, carruselId);
}

function currentSlide(n, carruselId) {
    showSlides(slideIndex[carruselId] = n, carruselId);
}

function showSlides(n, carruselId) {
    let i;
    let slides = document.getElementById(carruselId).getElementsByClassName("img_con_desc");

    if (n > 3) {
        slideIndex[carruselId] = 1;
    }
    if (n < 1) {
        slideIndex[carruselId] = 3;
    }

    for (i = 0; i < 3; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex[carruselId] - 1].style.display = "block";
}


function startAutocarrusel(carruselId) {
    // Devuelve el identificador del temporizador
    return setInterval(function () {
        plusSlides(1, carruselId);
        startTime = Date.now();
    }, 3000); // Cambia cada wait = 3000ms = 3 segundos.
}

function pauseAutocarrusel(carruselId){
    clearInterval(interval_carrusel[carruselId])
}

function resumeAutocarrusel(carruselId){
    // Los coordinamos haciendo que se esperen entre ellos
    if (startTime == null) {
        startTime = Date.now();
    }
    
    wait = Math.max(0, 3000 - (Date.now() - startTime));
    setTimeout(function(){
        interval_carrusel[carruselId] = startAutocarrusel(carruselId);
    }, wait)     
}

function showNavigation(carruselId) {
    // Pausamos el desplaamiento automático
    pauseAutocarrusel(carruselId)
    // Mostrar las flechas "prev" y "next" y el número "numbertext"
    const carrusel = document.getElementById(carruselId);
    const prevButton = carrusel.querySelector('.prev');
    const nextButton = carrusel.querySelector('.next');
    const numbertext = carrusel.querySelectorAll('.numbertext');
  
    if (prevButton) {
      prevButton.style.display = 'block';
    }
    if (nextButton) {
      nextButton.style.display = 'block';
    }
    if (numbertext.length > 0) {
      numbertext.forEach((text) => {
        text.style.display = 'block';
      });
    }
  }
  
  function hideNavigation(carruselId) {
    // Ocultar las flechas "prev" y "next" y el número "numbertext"
    const carrusel = document.getElementById(carruselId);
    const prevButton = carrusel.querySelector('.prev');
    const nextButton = carrusel.querySelector('.next');
    const numbertext = carrusel.querySelectorAll('.numbertext');
  
    if (prevButton) {
      prevButton.style.display = 'none';
    }
    if (nextButton) {
      nextButton.style.display = 'none';
    }
    if (numbertext.length > 0) {
      numbertext.forEach((text) => {
        text.style.display = 'none';
      });
    }

    // Reanudamos el desplazamiento automático
    resumeAutocarrusel(carruselId)
  }
  
  
// Animación scroll
function getPositionOfPage(page) {
    const position = page.getBoundingClientRect();
    return position.top;
}

function animateScroll(page) {
    if (getPositionOfPage(page) - window.innerHeight * 0.8 < 0 && page.style.opacity == 0) {
        // console.log("Posicion de " + page.id + ": " + getPositionOfPage(page));
        $(page).animate({ opacity: 1 }, 500);
    }
    else if (getPositionOfPage(page) - window.innerHeight * 1 > 0 && page.style.opacity == 1) {
        // console.log("Posicion de " + page.id + ": " + getPositionOfPage(page));
        page.style.opacity = 0;
    }
}


// Desplegar menu de hamburguesa
function toggleClass(elem,className){
	if (elem.className.indexOf(className) !== -1){
		elem.className = elem.className.replace(className,'');     
	}
	else{
		elem.className = elem.className.replace(/\s+/g,' ') + 	' ' + className;
	}
	
	return elem;
}

function toggleDisplay(elem){
	const curDisplayStyle = elem.style.display;			
				
	if (curDisplayStyle === 'none' || curDisplayStyle === ''){
		elem.style.display = 'block';
	}
	else{
		elem.style.display = 'none';
	}
}


function toggleMenuDisplay(e){
	const dropdown = e.currentTarget.parentNode;
	const menu = dropdown.querySelector('.opciones_menu');
	const icon = dropdown.querySelector('.fa-angle-right');

	toggleClass(menu,'hide');
	toggleClass(icon,'rotate-90');
}

function handleOptionSelected(e){
	toggleClass(e.target.parentNode, 'hide');			
	const icon = document.querySelector('.menu_de_hamburguesa .title .fa');

    // Simulamos un click en el menú de ordenador para poder
    // reutilizar el comportamiento
    if(e.target.textContent == "Inicio"){
        btn_inicio.click();
    }
    else if(e.target.textContent == "Menú"){
        btn_menu.click();
    }
	else if(e.target.textContent == "Nuestros chefs"){
        btn_chefs.click();
    }
    else if(e.target.textContent == "Sobre nosotros"){
        btn_nosotros.click();
    }
    else if(e.target.textContent == "Registro"){
        open_reg.click();
    }
    else if(e.target.textContent == "Realizar pedido"){
        open_pedido.click();
    }
	//setTimeout se usa para que la transición se muestre correctamente
	setTimeout(() => toggleClass(icon,'rotate-90',0));
}
