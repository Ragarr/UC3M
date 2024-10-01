const UserIcon = L.icon({
    iconUrl: "../../media/user-icon.png",
    iconSize: [20, 20],
    popupAnchor: [0, 0],
});

function obtainProductSection() {
    let params = new URLSearchParams(window.location.search);
    let section = params.get("section");
    return section;
}

function moveUserTo(newPosition) {
    userMarker.setLatLng(newPosition);
    map.panTo(newPosition);
}

let map = L.map('map', {
  crs: L.CRS.Simple,
  maxBounds: [[-100, -200], [600, 600]],  
  maxBoundsViscosity: 0.9, 
  minZoom: 0,  
  zoomSnap: 0.5,  
  zoomDelta: 0.5, 
  wheelPxPerZoomLevel: 100  
});

let bounds = [[0, 0], [500, 400]];

let image = L.imageOverlay('https://upload.wikimedia.org/wikipedia/commons/6/6d/First_Floor_Bramshill_House_drawing.svg', bounds).addTo(map);

map.fitBounds(bounds);

// Opcionalmente, ajusta la configuración de zoom después de cargar el mapa
map.whenReady(function() {
  map.setMinZoom(map.getZoom());
});

let userMarker = L.marker(map.getCenter(), { icon: UserIcon }).addTo(map);
userMarker.bindPopup("Ud. está aquí").openPopup();

const LAT_RANGE = [6.0, 116.0];
const LNG_RANGE = [20.0, 120.0];

// Función para transformar latitud y longitud en coordenadas x, y
function latLngToXY(lat, lng) {
  // Utiliza aritmética modular para "envolver" las coordenadas
  let modLat = ((lat - LAT_RANGE[0]) % (LAT_RANGE[1] - LAT_RANGE[0]));
  let modLng = ((lng - LNG_RANGE[0]) % (LNG_RANGE[1] - LNG_RANGE[0]));
  
  let y = (modLat / (LAT_RANGE[1] - LAT_RANGE[0])) * 500;
  let x = (modLng / (LNG_RANGE[1] - LNG_RANGE[0])) * 400;
  return [x, y];
}

function onLocationFound(e) {
  let latlng = e.latlng;
  let xy = latLngToXY(latlng.lat, latlng.lng);
  /*
  Si el usuario está en el rango de coordenadas:
  - [212, 50](correspondiente a los valores [17, 173]-latitud longitud- en los sensores de chrome)
  - [232, 31](correspondiente a los valores [13, 178]-latitud longitud- en los sensores de chrome)
  se simulará la salida del usuario de la tienda.
  */
  if (xy[0] >= 212 && xy[0] <= 232 && xy[1] >= 31 && xy[1] <= 50){
    simulateExit();
    return;
  }
  userMarker.setLatLng([xy[1], xy[0]]);
  userMarker.bindPopup("Ud. está aquí").openPopup();
  map.panTo([xy[1], xy[0]]);
}

function onLocationError(e) {
  alert("Error al obtener la ubicación: " + e.message);
}

map.on('locationfound', onLocationFound);
//map.on('locationerror', onLocationError);

map.locate({watch: true, setView: false, maxZoom: 1});

function calculateDistance(lat1, lng1, lat2, lng2) {
  return Math.sqrt(Math.pow(lat2 - lat1, 2) + Math.pow(lng2 - lng1, 2));
}

function simulateMovement(destination) {
  if (destination === "Exit"){
    simulateExit();
    return;
  }
  let currentPosition = userMarker.getLatLng();
  let destinationLatLng = new L.LatLng(destination[0], destination[1]);
  let errorMargin = 5; // Define el margen de error como 5 unidades en el mapa
  let intervalId = setInterval(() => {
      if (calculateDistance(currentPosition.lat, currentPosition.lng, destinationLatLng.lat, destinationLatLng.lng) > errorMargin) {
          let stepLat = (destinationLatLng.lat - currentPosition.lat) / 20;
          let stepLng = (destinationLatLng.lng - currentPosition.lng) / 20;
          let newX = currentPosition.lat + stepLat;
          let newY = currentPosition.lng + stepLng;
          currentPosition = new L.LatLng(newX, newY);
          userMarker.setLatLng(new L.LatLng(newX, newY));
          map.panTo(new L.LatLng(newX, newY));
      } else {
          console.log("Destino alcanzado");
          clearInterval(intervalId);
      }
  }, 100);
}

function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] === value);
}

document.addEventListener("DOMContentLoaded", function() {
  var keepCartBtn = document.getElementById('keep-cart');
  var payCartBtn = document.getElementById('pay-cart');

  // Función para redirigir a la página del carrito
  function redirectToCart() {
      window.open('../cart/cart.html', "_self");
  }

  keepCartBtn.addEventListener('click', redirectToCart);
  payCartBtn.addEventListener('click', redirectToCart);
});

function simulateExit(){
  /*
  Para simular la salida del local, primero se debe obtener el carrito del usuario para
  comprobar si tiene productos. Si el carrito está vacío, el usuario puede salir del local y listo,
  si no, se ha de mostrar un cuadro de texto que indique que el usuario tiene productos en el carrito
  y que no puede salir del local hasta que los haya pagado o bien conservar los productos del carrito y
  pagar después.
  */
  let cart = JSON.parse(localStorage.getItem("cart"));
  if (cart === null || Object.keys(cart).length === 0){
    alert("Ud. ha salido del local.");
  } else {
    const exitPopUp = document.getElementById("exit-popup");
    exitPopUp.style.display = "flex";
  }
}

// las coordenadas tienen formato [latitud, longitud]
// latitud + es hacia el norte
// longitud + es hacia el oeste
// el centro es [250, 200]
let locations = {
  "Papelería" : {
    coords: [222, 142],
    area: [23,27],
    color: "red"
  },
  "Supermercado" : {
    coords: [450, 210],
    area: [35,180],
    color: "blue"
  },
  "Infantil" : {
    coords: [320, 142],
    area: [40,27],
    color: "green"
  },
  "Moda" : {
    coords: [39, 355],
    area: [30,30],
    color: "yellow"
  },
  "Electrónica" : {
    coords: [364, 280],
    area: [49,32],
    color: "orange"
  },
  "Hogar" : {
    coords: [103, 157],
    area: [27,40],
    color: "purple"
  },
  "Deportes" : {
    coords: [255, 279],
    area: [55,33],
    color: "brown"
  },
  "Juguetes y videojuegos" : {
    coords: [102, 258],
    area: [28,55],
    color: "pink"
  },
  "Libros" : {
    coords: [262, 142],
    area: [16,27],
    color: "black"
  }
};

function focusSection(section) {
    // trace route to the section
    // move the user to the section
    const sectionCoords = locations[section].coords;
    // draw the section
    drawSection(section);

    // open the marker popup
    userMarker.bindPopup(section).openPopup();
    
}

function drawSection(section) {
    // draw the marker
    let loc = locations[section].coords;
    let marker = L.marker(loc).addTo(map);

    // draw a rectangle of the area of the section
    // with the same center as the marker
    // and color color
    let area = locations[section].area;
    let rectangle = L.rectangle([
        [loc[0] - area[0], loc[1] - area[1]],
        [loc[0] + area[0], loc[1] + area[1]]
    ], {color: locations[section].color}).addTo(map);

    // add a tag to the marker
    marker.bindPopup(section)
    // add a tag to the rectangle
}

section = obtainProductSection();

if (section !== null) {
    focusSection(section);
}
else{
    for (let key in locations) {
        drawSection(key); 
    }
}


