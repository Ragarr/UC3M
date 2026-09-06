/*
INICIALIZACIÓN DEL MAPA Y UBICACIÓN DEL USUARIO
*/
var map = L.map("map");
// Crear un marcador con un icono personalizado
var userIcon = L.icon({
    iconUrl: "media/current-location-1.svg",
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -40],
});

var userMarker;
var markers = []; // Array para almacenar los marcadores creados

var zoom = 15; // Nivel de zoom inicial del mapa

function initializeMap(position) {
    map.setView([position.coords.latitude, position.coords.longitude], zoom);

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution:
            '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
}

function onPositionError(error) {
    console.error("Error getting position: ", error, error.message);
}

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(initializeMap, onPositionError, {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0,
    });
} else {
    alert("Geolocation is not supported by this browser.");
}


/*
CONTROL DEL ZOOM
para que no se reinicie el zoom al cambiar de ubicación
*/
map.on("zoomend", function () {
    zoom = map.getZoom();
});

/*
DESHABILITAR ZOOM CON DOBLE CLIC
*/
map.doubleClickZoom.disable();

/*

AÑADIR Y ELIMINAR MARCADORES
FUNCIONAMIENTO:
1. Al hacer doble clic en el mapa, se añade un marcador en la ubicación seleccionada.
2. Se crea un circulo alrededor del marcador
2. Al hacer clic en el radio exterior del circulo permite cambiar el radio del círculo con un popup 
4. se añade un evento de clic al marcador para eliminarlo
*/

// constantes
const DEFAULT_RADIUS = 500; // radio por defecto del círculo
var circle_selected = false; // variable para saber si el círculo está seleccionado
var circle_count = 0; // variable para saber cuantos círculos hay en el mapa

// detectar dobleclic en el mapa
map.on("dblclick", function (event) {
    let lat = event.latlng.lat;
    let lon = event.latlng.lng;

    let marker = L.marker([lat, lon]).addTo(map);
    // Crear un círculo alrededor del marcador
    let circle = L.circle([lat, lon], {
        color: "red",
        fillColor: "#f03",
        fillOpacity: 0.5,
        radius: DEFAULT_RADIUS,
    }).addTo(map);
    circle.id = circle_count++;
    circle.muted = false;
    console.log("circulo " + circle.id + " creado");

    // Guardar la estructura {marker: marker, circle: circle} en la lista markers
    markers.push({ marker: marker, circle: circle });

    // Añadir evento de clic al marcador para eliminarlo
    marker.on("click", function () {
        map.removeLayer(marker);
        map.removeLayer(circle);
        markers = markers.filter(function (m) {
            return m.marker !== marker;
        });
    });

    circle.on("click", function () {
        console.log("circulo "+ circle.id + " seleccionado");
        const getMuteStatus = (circle) => (!circle.muted ? "Mute" : "Unmute");
        let popup = L.popup()
            .setLatLng([lat, lon])
            .setContent(
                '<input type="range" id="radius' + circle.id + '" value="' +
                    inverseLogslider(circle.getRadius()) +
                    '" min="0" max="100"><label for="radius' + circle.id + '">Radius: </label><span id="radius-value'+ circle.id+'">' +
                    getDistanceUnits(circle.getRadius()) +
                    '</span><div style="display: flex; justify-content: space-between;"><button id="muteButton' + circle.id + '" style="flex: 1;">' + getMuteStatus(circle) + '</button><button id="deleteButton' + circle.id + '" style="flex: 1;">Eliminar</button></div>' // Agrega el botón de eliminar
            )
            .openOn(map);
        // Añadir evento de click al botón de mute/unmute
        document.getElementById('muteButton' + circle.id).addEventListener('click', function () {
            circle.muted = !circle.muted;
            this.innerText = getMuteStatus(circle);
            console.log("circulo "+ circle.id + " " + getMuteStatus(circle));
        });
        // Añadir evento de click al botón de eliminar
        document.getElementById('deleteButton' + circle.id).addEventListener('click', function () {
            map.removeLayer(marker);
            map.removeLayer(circle);
            markers = markers.filter(function (m) {
                return m.marker !== marker;
            });
            popup.remove();
            // Aquí debes agregar el código para eliminar el marcador correspondiente
            console.log("circulo "+ circle.id + " eliminado");
        });
        // Añadir evento de input al selector de rango del popup
        document
            .getElementById("radius"+ circle.id)
            .addEventListener("input", function () {
                let inputValue = document.getElementById("radius"+circle.id).value;
                let newRadius = parseInt(logslider(inputValue));
                document.getElementById("radius-value"+circle.id).innerText =
                    getDistanceUnits(newRadius);
                circle.setRadius(newRadius);
            });
    });
});
// Funciones para convertir el valor del rango a un valor logarítmico y viceversa
function logslider(position) {
    // position will be between 0 and 100
    let minp = 0;
    let maxp = 100;

    // The result should be between 100 an 100.000
    let minv = Math.log(100);
    let maxv = Math.log(100000);

    // calculate adjustment factor
    let scale = (maxv - minv) / (maxp - minp);

    return Math.exp(minv + scale * (position - minp));
}

function inverseLogslider(value) {
    // Los valores min y max son los mismos que en la función logslider
    let minp = 0;
    let maxp = 100;
    let minv = Math.log(100);
    let maxv = Math.log(10000);
    let scale = (maxv - minv) / (maxp - minp);

    // Calcular la posición inversa
    let position = (Math.log(value) - minv) / scale + minp;

    return position;
}
// Función para convertir la distancia a km si es mayor a 1000m
function getDistanceUnits(value) {
    if (value < 1000) {
        return value + "m";
    } else {
        return (value / 1000).toFixed(2) + "km";
    }
}

/*
DETECTAR SI EL USUARIO ESTA DENRO DE UN CIRCULO
*/

// Función para detectar si el usuario está dentro de un círculo
function isUserInsideCircle(userPosition, circle) {
    /* userPosition es un objeto LatLng con las coordenadas del usuario
    circle es un objeto Circle con las propiedades del círculo */
    let circleCenter = circle.getLatLng(); // Coordenadas del centro del círculo
    let circleRadius = circle.getRadius(); // Radio del círculo
    return userPosition.distanceTo(circleCenter) < circleRadius;

}


/* 
DIBUJO DEL ICONO DEL USUARIO Y TRACK DE SU UBICACIÓN
*/

function drawUserIcon(position) {
    let lat = position.coords.latitude;
    let lon = position.coords.longitude;

    // Si el marcador ya existe, actualiza su ubicación
    if (userMarker) {
        userMarker.setLatLng([lat, lon]);
    } else {
        // Si no, crea un nuevo marcador y añádelo al mapa
        userMarker = L.marker([lat, lon], { icon: userIcon }).addTo(map);
    }

    // Centrar el mapa en la nueva ubicación
    map.setView([lat, lon], zoom);
}



function trackUser(position) {
    // console.log(position.coords.latitude, position.coords.longitude);
    drawUserIcon(position);
    for (let i = 0; i < markers.length; i++) {
        let circle = markers[i].circle;
        if (isUserInsideCircle(userMarker.getLatLng(), circle)) {
            // console.log("Estás dentro del círculo " + circle.id);
            vibrate(circle, userMarker.getLatLng());

        }
    }
}



// Usar la función drawUserIcon en watchPosition
watchPositionId = navigator.geolocation.watchPosition(
    trackUser,
    onPositionError,
    { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
);


// funcion de vibracion si el usuario esta dentro de un circulo

function vibrate(circle, userPosition) {

    if (circle.muted) {
        console.log("circulo " + circle.id + " silenciado");
        return;
    }
    // vibra cada vez mas en funcion de la distancia al centro del circulo
    // vibracion minima cuando el usuario esta en el borde del circulo
    // vibracion maxima cuando el usuario esta a un 90% el centro del circulo
    vibratePatterns = {
        far: [50, 200],
        medium: [50, 100, 50, 100],
        close: [100, 100, 100, 100],
        veryClose: [200, 50, 200, 50],

    };

    let distance = Math.abs(userPosition.distanceTo(circle.getLatLng()));
    let maxDistance = circle.getRadius() * 0.9;
    let minDistance = circle.getRadius() * 0.1;
    let relDistance = distance / circle.getRadius();
    // console.log("distancia al circulo: " + distance);
    console.log("distancia relativa al circulo: " + relDistance);

    if (relDistance < 0.25) {
        vibration = vibratePatterns.veryClose;
    }
    else if (relDistance < 0.5) {
        vibration = vibratePatterns.close;
    }
    else if (relDistance < 0.75) {
        vibration = vibratePatterns.medium;
    }
    else {
        vibration = vibratePatterns.far;
    }
    navigator.vibrate(vibration);
}



/*
HELP BUTTON
*/
var helpMenu = document.getElementById("help-menu");
var helpBtn = document.getElementById("help-btn");
var closeBtn = document.getElementById("close-help");
var isHelpMenuOpen = false;

helpBtn.addEventListener("click", function () {
    if (isHelpMenuOpen) {
        helpMenu.style.display = "none";
    } else {
        helpMenu.style.display = "block";
    }
    isHelpMenuOpen = !isHelpMenuOpen;
});

closeBtn.addEventListener("click", function () {
    helpMenu.style.display = "none";
    isHelpMenuOpen = false;
});


/* TODO:
Change map to dark mode with 
 L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.{ext}', {
	minZoom: 0,
	maxZoom: 20,
	attribution: '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	ext: 'png'
})

    TODO
*/
