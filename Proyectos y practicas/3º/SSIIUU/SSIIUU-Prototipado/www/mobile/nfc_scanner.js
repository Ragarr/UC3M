const askNfcPermission = `
    <div id="nfc-popup" class="popup" 
    style = '
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
        z-index: 1000;
        display: none;
        justify-content: center;
        align-items: center;

        '>
        <div class="popup-content" 
        style = '
            background-color: white;
            width: 50%;
            margin: auto;
            padding: 20px;
            '>
            <h1>¿Permitir acceso al NFC?</h1>
            <p>Para poder leer la información de los productos necesitamos que permitas el acceso al NFC.</p>
            <button id="allow-nfc">Permitir</button>
        </div>
    </div>
`;

// crear div, añadirle la clase y el contenido
let nfcPopup = document.createElement("div");
main = document.getElementsByTagName("main")[0];
nfcPopup.className = "popup";
nfcPopup.innerHTML = askNfcPermission;
// añadir el div al main
main.appendChild(nfcPopup);

nfcPopup = document.getElementById("nfc-popup");

// si clicas fuera del popup se cierra
nfcPopup.addEventListener("click", function(event){
    if(event.target.id === "nfc-popup"){
        nfcPopup.style.display = "none";
    }
});

try{
    var ndef = new NDEFReader(); 
}catch{
    console.log("version de navegador no compatible")
}

async function startScanning() {
    await ndef.scan();
    ndef.onreading = (event) => {
        // get the first record in the message
        const record = event.message.records[0];
        // the record is text data, show it
        if (record.recordType === "text") {
            const textDecoder = new TextDecoder(record.encoding);
            const text = textDecoder.decode(record.data);
            console.log(text);
            let product = checkProductFormat(text);
            if (product) {
                goToProductView(product);
            }
        }

    };
}


function checkProductFormat(data){
    // check if the product is in the correct format
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

function goToProductView(product) {
    let productId = product.id;
    let productViewUrl = `/mobile/pages/product-view/product_view.html?id=${productId}`;
    console.log("Go to product view", productViewUrl);
    window.open(productViewUrl, "_self");
}


async function askForPermissionAndStartScanning(){
    const nfcPermissionStatus = await navigator.permissions.query({ name: "nfc" });
    if (nfcPermissionStatus.state === "granted") {
        console.log("permissions granted");
        // NFC access was previously granted, so we can start NFC scanning now.
        startScanning();
    }else{
        console.log("permissions not granted");
        // NFC access was not granted, so we need to ask the user for permission.
        nfcPopup.style.display = "flex";
        document.getElementById("allow-nfc").addEventListener("click", async function(){
            // await navigator.permissions.request({ name: "nfc" });
            startScanning();
            nfcPopup.style.display = "none";
        });
    }
}


try {
    askForPermissionAndStartScanning();
} catch (error) {
    console.error(error);
    // alert("NFC is not supported in this device");
}
