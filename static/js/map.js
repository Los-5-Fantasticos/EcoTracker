/**
 * map.js
 * * - Permite al usuario elegir un Origen y un Destino.
 * - 1er clic = Origen
 * - 2do clic = Destino (y calcula ruta)
 * - 3er clic = Reinicia
 * - El botón "Usar mi ubicación" solo establece el Origen.
 */

// Variables globales
let map;
let directionsService;
let directionsRenderer;
let originMarker;      // Marcador para el Origen
let destinationMarker; // Marcador para el Destino
let mapHelperText;     // El elemento <small> del HTML

/**
 * Función principal llamada por la API de Google
 */
function initMap() {
    // 1. Inicializa los servicios de rutas
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();

    // 2. Ubicación por defecto
    const santiago = { lat: -33.45694, lng: -70.64827 };

    // 3. Crea el mapa
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: santiago,
        clickableIcons: true,
    });

    // 4. Conecta el "lápiz" al mapa
    directionsRenderer.setMap(map);

    // 5. Conecta el texto de ayuda
    mapHelperText = document.getElementById('map-helper-text');

    // 6. Conecta el listener de Clic del Mapa
    map.addListener('click', (event) => {
        handleMapClick(event.latLng);
    });

    // 7. Conecta el botón "Usar mi ubicación"
    document.getElementById("find-me-btn").addEventListener('click', findMeAsOrigin);

    // 8. Centrar en la ubicación del usuario al cargar
    centerMapOnUserLocation();
}

/**
 * Maneja todos los clics en el mapa
 * @param {google.maps.LatLng} location - Coordenadas del clic
 */
function handleMapClick(location) {
    const clicLocation = {
        lat: location.lat(),
        lng: location.lng(),
    };
    if (!originMarker) {
        // 1. ESTADO: No hay Origen. Este clic ES el Origen.
        setOrigin(clicLocation);
    } else if (!destinationMarker) {
        // 2. ESTADO: Hay Origen, pero no Destino. Este clic ES el Destino.
        setDestination(clicLocation);
    } else {
        // 3. ESTADO: Hay ambos. Este clic REINICIA.
        clearMap(); // Borra todo
        setOrigin(clicLocation); // Y pone el nuevo origen
    }
}

/**
 * Pone el marcador de Origen y actualiza la UI
 * @param {google.maps.LatLng} location - Coordenadas
 */
function setOrigin(location) {
    clearMap(); // Limpia el mapa por si acaso

    const lat = document.getElementById('start-lat');
    const lon = document.getElementById('start-lng');
    lat.value = location.lat;
    lon.value = location.lng;

    originMarker = new google.maps.Marker({
        position: location,
        map: map,
        animation: google.maps.Animation.DROP,
        icon: {
            url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png" // Marcador verde
        }
    });
    map.panTo(location);
    mapHelperText.innerHTML = "¡Genial! Ahora haz clic para elegir un **destino**.";
}

/**
 * Pone el marcador de Destino y calcula la ruta
 * @param {google.maps.LatLng} location - Coordenadas
 */
function setDestination(location) {
    const lat = document.getElementById('end-lat');
    const lon = document.getElementById('end-lng');
    lat.value = location.lat;
    lon.value = location.lng;

    destinationMarker = new google.maps.Marker({
        position: location,
        map: map,
        animation: google.maps.Animation.DROP,
        icon: {
            url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png" // Marcador rojo
        }
    });
    mapHelperText.innerHTML = "Calculando ruta... Haz clic de nuevo para reiniciar.";

    // Llama a calcular la ruta con las posiciones de ambos marcadores
    calculateAndDisplayEcoRoute(originMarker.getPosition(), destinationMarker.getPosition());
}

/**
 * Botón "Usar mi ubicación" -> Llama a esto.
 */
function findMeAsOrigin() {
    if (navigator.geolocation) {
        const lat = document.getElementById('start-lat');
        const lon = document.getElementById('start-lng');

        navigator.geolocation.getCurrentPosition(
            (position) => {
                lat.value = position.coords.latitude;
                lon.value = position.coords.longitude;
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                setOrigin(userLocation); // Llama a la misma función 'setOrigin'
            },
            () => {
                handleLocationError(true);
            }
        );
    } else {
        handleLocationError(false);
    }
}
/**
 * Solo centra el mapa en la ubicación del usuario sin poner marcador
 */
function centerMapOnUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                map.panTo(userLocation); // Centra el mapa en la ubicación del usuario
            },
            () => {
                handleLocationError(true);
            }
        );
    } else {
        handleLocationError(false);
    }
}

/**
 * Calcula y dibuja la ruta entre dos puntos
 * @param {google.maps.LatLng} origin - Punto de inicio
 * @param {google.maps.LatLng} destination - Punto final
 */
function calculateAndDisplayEcoRoute(origin, destination) {
    const request = {
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.BICYCLING // Ruta ecológica
    };

    directionsService.route(request, (response, status) => {
        if (status == 'OK') {
            directionsRenderer.setDirections(response);
        } else {
            window.alert('Error al calcular la ruta: ' + status);
            mapHelperText.innerHTML = "Error al calcular. Haz clic para reiniciar.";
        }
    });


    const km = haversineKm(
        origin.lat(), origin.lng(),
        destination.lat(), destination.lng()
    );

    const distanceInput = document.getElementById('distance-km');
    if (distanceInput) {
        distanceInput.value = km.toFixed(2);
    }

    // Recalcular huella si la función global existe
    if (typeof window.updateHuella === 'function') {
        window.updateHuella();
    }
}

/**
 * Función de ayuda para limpiar el mapa
 */
function clearMap() {

    if (originMarker) {

        originMarker.setMap(null);
        originMarker = null;
    }
    if (destinationMarker) {
        destinationMarker.setMap(null);
        destinationMarker = null;
    }
    directionsRenderer.setDirections(null); // Borra la línea de la ruta
    mapHelperText.innerHTML = "Haz clic en el mapa para elegir un punto de **inicio**.";

    document.getElementById('start-lat').value = '0';
    document.getElementById('start-lng').value = '0';
    document.getElementById('end-lat').value = '0';
    document.getElementById('end-lng').value = '0';

}

/**
 * Manejador de errores de geolocalización
 */
function handleLocationError(browserHasGeolocation) {
    alert(browserHasGeolocation
        ? 'Error: El servicio de geolocalización falló. ¿Diste permiso?'
        : 'Error: Tu navegador no soporta geolocalización.');
}


function updateHuella() {
    const itemSelect    = document.getElementById('item-select');
    const distanceInput = document.getElementById('distance-km');
    const timeInput     = document.getElementById('time-sec');

    const huellaDistDisplay = document.getElementById('huella-dist-display');
    const huellaTimeDisplay = document.getElementById('huella-time-display');

    const huellaDistInput   = document.getElementById('huella-kg-dist');
    const huellaTimeInput   = document.getElementById('huella-kg-time');

    if (!itemSelect || !distanceInput || !timeInput ||
        !huellaDistDisplay || !huellaTimeDisplay) {
        return;
    }

    if (itemSelect.selectedIndex <= 0) {
        huellaDistDisplay.textContent = '–';
        huellaTimeDisplay.textContent = '–';
        if (huellaDistInput) huellaDistInput.value = '';
        if (huellaTimeInput) huellaTimeInput.value = '';
        return;
    }

    const option = itemSelect.options[itemSelect.selectedIndex];

    // Factores desde los data-*
    const factorDistStr = option.getAttribute('data-factor-dist')
                       || option.getAttribute('data-factor')
                       || '0';
    const factorTimeStr = option.getAttribute('data-factor-time') || '0';

    let factorDist = parseFloat(String(factorDistStr).replace(',', '.')) || 0; // kg CO₂ / km
    let factorTime = parseFloat(String(factorTimeStr).replace(',', '.')) || 0; // kg CO₂ / hora
    if(factorTime === 0 && factorDist === 0) {
        huellaDistDisplay.textContent = '–';
        huellaTimeDisplay.textContent = '–';
        if (huellaDistInput) huellaDistInput.value = '';
        if (huellaTimeInput) huellaTimeInput.value = '';
        return;
    }
    if(factorDist === 0 && factorTime !== 0) {
        factorDist = factorTime; // Si no hay factor por distancia, usar el de tiempo
    
    }

    if(factorTime === 0 && factorDist !== 0) {
        factorTime = factorDist; // Si no hay factor por tiempo, usar el de distancia
    }

    const distanceKm = parseFloat(distanceInput.value || '0');
    const timeSec    = parseFloat(timeInput.value || '0');
    const timeHours  = timeSec / 3600;

    const huellaDist = factorDist * distanceKm;
    const huellaTime = factorTime * timeHours;

    // Mostrar en el card
    huellaDistDisplay.textContent = huellaDist > 0 ? huellaDist.toFixed(2) : '–';
    huellaTimeDisplay.textContent = huellaTime > 0 ? huellaTime.toFixed(2) : '–';

    // Guardar en inputs ocultos si se van a enviar al backend
    if (huellaDistInput) huellaDistInput.value = huellaDist > 0 ? huellaDist.toFixed(4) : '';
    if (huellaTimeInput) huellaTimeInput.value = huellaTime > 0 ? huellaTime.toFixed(4) : '';
}


/**
 * Haversine: calcula distancia (en km) entre dos puntos lat/lng
 */
function haversineKm(lat1, lng1, lat2, lng2) {
    const R = 6371e3; // radio de la Tierra en metros
    const toRad = (deg) => deg * Math.PI / 180;

    const φ1 = toRad(lat1);
    const φ2 = toRad(lat2);
    const Δφ = toRad(lat2 - lat1);
    const Δλ = toRad(lng2 - lng1);

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
        Math.cos(φ1) * Math.cos(φ2) *
        Math.sin(Δλ / 2) * Math.sin(Δλ / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    const meters = R * c;
    return meters / 1000.0; // km
}


document.addEventListener('DOMContentLoaded', function () {
    const itemSelect    = document.getElementById('item-select');
    const distanceInput = document.getElementById('distance-km');
    const timeInput     = document.getElementById('time-sec');
    const clearBtn      = document.getElementById('clear-form-btn');

    if (itemSelect) {
        itemSelect.addEventListener('change', updateHuella);
    }
    if (distanceInput) {
        distanceInput.addEventListener('input', updateHuella);
    }
    if (timeInput) {
        timeInput.addEventListener('input', updateHuella);
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', function () {
            const form = document.querySelector('form');
            if (form) form.reset();

            const huellaDistDisplay = document.getElementById('huella-dist-display');
            const huellaTimeDisplay = document.getElementById('huella-time-display');
            if (huellaDistDisplay) huellaDistDisplay.textContent = '–';
            if (huellaTimeDisplay) huellaTimeDisplay.textContent = '–';

            if (window.clearMapRoute) {
                window.clearMapRoute();
            }
        });
    }
});

// Para que map.js pueda llamar si hace falta
window.updateHuella = updateHuella;
