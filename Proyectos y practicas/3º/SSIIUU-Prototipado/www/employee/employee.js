document.addEventListener("DOMContentLoaded", () => {
    const socket = io();


    socket.emit("get-orders");

    socket.on("purchase", (order) => {
        order = order.mensaje;
        
        console.log("Datos recibidos:", order); // Esta línea te ayudará a ver exactamente lo que estás recibiendo del servidor
        // Verificar si data es un arreglo como esperamos

        let payment_method = order.payment.payment;
        let delivery_method = order.delivery.delivery;
        let cart = order.cart; // cart es un arreglo de productos

        const container = document.getElementById("peticiones-container");
        const petition_template = document.querySelector(".peticion-template");
        const product_template = document.querySelector(".product");

        // duplicar la plantilla para cada producto
        const clone = petition_template.cloneNode(true);

        // borrar el contenido de la plantilla
        clone.querySelector(".product").textContent = "";

        // borrar el petition footer
        clone.querySelector(".petition-footer").textContent = "";

        // obtener la información del pedido
        clone.querySelector(".payment-method").textContent = payment_method;
        clone.querySelector(".delivery-method").textContent = delivery_method;
        // obtener la información del producto
        total = 0;
        // añadir un h2 productos
        const h2 = document.createElement("h3");
        h2.textContent = "Productos: ";
        clone.appendChild(h2);

        cart.forEach((product) => {
            // Clonamos la template de cada producto
            const product_clone = product_template.cloneNode(true);
            product_clone.querySelector(".product-name").textContent =
                product.name;
            product_clone.querySelector(".product-price").textContent =
                product.price;
            product_clone.querySelector(".product-quantity").textContent =
                product.quantity;
            clone.appendChild(product_clone);
            total += product.price * product.quantity;
        });
        clone.querySelector(".total-price").textContent = total;
        container.appendChild(clone);
        clone.style.display = "block";

        // agregar el petition footer
        const petition_footer = document.createElement("div");
        petition_footer.classList.add("petition-footer");
        petition_footer.innerHTML = `
            <button class="btn-confirmar">Confirmar</button>
            <button class="btn-cancelar">Cancelar</button>
        `;
        clone.appendChild(petition_footer);

        // añadir eventos a los botones
        const confirm_button = clone.querySelector(".btn-confirmar");
        const cancel_button = clone.querySelector(".btn-cancelar");

        confirm_button.addEventListener("click", () => {
            console.log("Confirmado:", order);
            socket.emit("confirmed-by-employee", order);
            location.reload();
        });
        
        cancel_button.addEventListener("click", () => {
            console.log("Cancelado:", order);
            socket.emit("canceled-by-employee", order);
            location.reload();
        });
    });
});
