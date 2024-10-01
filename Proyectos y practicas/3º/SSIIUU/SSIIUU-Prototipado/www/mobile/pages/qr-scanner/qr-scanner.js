const video = document.createElement("video"); // Crear un elemento de video
const canvasElement = document.getElementById("canvas"); // Obtener el canvas del overlay
const canvas = canvasElement.getContext('2d', { willReadFrequently: true }); // Obtener el contexto 2D del canvas


let canScan = true;

function drawLine(begin, end, color) {
    canvas.beginPath();
    canvas.moveTo(begin.x, begin.y);
    canvas.lineTo(end.x, end.y);
    canvas.lineWidth = 4;
    canvas.strokeStyle = color;
    canvas.stroke();
}

// Usar facingMode: environment para intentar obtener la cámara frontal en los teléfonos
navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(function(stream) {
    video.srcObject = stream;
    video.setAttribute("playsinline", true); // Requerido para decirle a iOS Safari que no queremos pantalla completa
    video.play();
    requestAnimationFrame(tick);
});

function goToProductView(product) {
    let productId = product.id;
    let productViewUrl = `/mobile/pages/product-view/product_view.html?id=${productId}`;
    console.log("Go to product view", productViewUrl);
    window.open(productViewUrl, "_self");
}


function askGoToProductView(product) {
    canScan = false;
    console.log("Nuevo codigo detectado", product);
    let askPopup = document.getElementById("ask-popup");
    askPopup.style.display = "block";
    let askPopupMessage = document.getElementById("ask-popup-message");
    askPopupMessage.innerHTML = `¿Quieres ir la vista de ${product.name}?`;
    let askPopupYes = document.getElementById("ask-popup-yes");
    askPopupYes.onclick = function () {
        // go to the product view
        goToProductView(product);
    };
    let askPopupNo = document.getElementById("ask-popup-no");
    askPopupNo.onclick = function () {
        setTimeout(allowScanner, 1000);
        askPopup.style.display = "none";
    };
}

function allowScanner() {
    canScan = true;
}

function verifyQRFormat(data) {
    /*
    {
        "id": 1,
        "name": "Pixel 7A",
        "price": 300,
        "quantity": 1,
        "image": "product1.jpeg",
        "section": "Electrónica" 
    }
    */
    try {
        let product = JSON.parse(data);
        if (typeof product.id === "number" && product.id > 0 &&
            typeof product.name === "string" &&
            typeof product.price === "number" && product.price >= 0 &&
            typeof product.quantity === "number" && product.quantity > 0 &&
            typeof product.image === "string" &&
            typeof product.section === "string")
        {
            return product;
        }
    }
    catch (error) {
        console.error(error);
    }
    return null;
}

    

function tick(){
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvasElement.hidden = false;
        // Establecer el tamaño del canvas
        canvasElement.width = canvasElement.offsetWidth;
        canvasElement.height = canvasElement.offsetHeight;
        // Escalar y dibujar el video en el canvas
        let aspectRatio = video.videoWidth / video.videoHeight;
        let scaledWidth = canvasElement.height * aspectRatio;
        let scaledHeight = canvasElement.height;
        let offsetX = (canvasElement.width - scaledWidth) / 2;
        canvas.drawImage(video, offsetX, 0, scaledWidth, scaledHeight);
        // Recortar el exceso del video que se extiende más allá del área visible del canvas
        canvas.clearRect(0, 0, offsetX, canvasElement.height);
        canvas.clearRect(offsetX + scaledWidth, 0, offsetX, canvasElement.height);
        var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
        var code = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: "dontInvert",
        });
        if (code) {
            drawLine(code.location.topLeftCorner, code.location.topRightCorner, "#FF3B58");
            drawLine(code.location.topRightCorner, code.location.bottomRightCorner, "#FF3B58");
            drawLine(code.location.bottomRightCorner, code.location.bottomLeftCorner, "#FF3B58");
            drawLine(code.location.bottomLeftCorner, code.location.topLeftCorner, "#FF3B58");
            if (canScan) {
                let product = verifyQRFormat(code.data);
            if (product) {
                askGoToProductView(product);
            }
            }
            
            // else: el qr no es de un producto válido, ignorar
        }
    }
    requestAnimationFrame(tick);
}


// si pulsas en el icono del logo ir a la pagina principal
let logo = document.getElementById("logo-block");
logo.addEventListener("click", function (event) {
    window.location.href = "/";
});
