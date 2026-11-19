// Archivo central JavaScript del FrontEnd. Encargada de la interacción usuario-servidor. Importa funciones y constantes del resto de módulos .js. Se ejecuta al cargar la página.
import { calcularRuta, geocodificar, precargarMapa } from './api.js';
<<<<<<< HEAD
import { DURACION_SPLASH_MS, EXTENSION_MAX_GRADOS, LIMITE_DISTANCIA_METROS, MAX_PARADAS } from './config.js';
import { estado } from './estado.js';
import {
    agregarEntrega, colocarAlmacen, detenerSeguimiento, dibujarRuta, distanciaAlAlmacen,
    iniciarSeguimiento, limpiarMapa, mapa, numerarSegunOrden, obtenerUbicacion, quitarEntrega, siguiendo,
=======
import { DURACION_SPLASH_MS, EXTENSION_MAX_GRADOS, LIMITE_DISTANCIA_METROS, MAX_PARADAS, UMBRAL_LLEGADA_M } from './config.js';
import { estado } from './estado.js';
import {
    agregarEntrega, avanzarParada, colocarAlmacen, detenerSeguimiento, dibujarRuta, distanciaAlAlmacen,
    distanciaAMarcador, iniciarSeguimiento, limpiarMapa, mapa, numerarSegunOrden, obtenerUbicacion,
    quitarEntrega, siguiendo,
>>>>>>> a6b004a (Cambios para ubicacion)
} from './mapa.js';
import {
    $, actualizarContador, avisar, irAPaso, iniciarAutocompletado, iniciarSplash, mostrarMetricas, mostrarSiguiente,
} from './panel.js';

<<<<<<< HEAD
=======
const TEXTO_SEGUIR = 'Seguir mi ubicación';
const TEXTO_DETENER = 'Detener seguimiento';

>>>>>>> a6b004a (Cambios para ubicacion)
let calculando=false; // Variable de control para evitar que se ejecute varias veces la función de cálculo de ruta a la vez

function navegar(paso) {
    if (calculando) return; // Evita que se ejecute varias veces a la vez
    // Si el negocio ha sido confirmado (paso 2 en estado), se inicia la precarga del mapa alrededor de este.
    if (paso === 3 && estado.paso === 2) precargarMapa(estado.puntos[0], estado.ciudad.nombre);
    irAPaso(paso); // Se actualiza el estado a paso 3 (confirmación de entregas).
}

function vaciarPuntos() {
    limpiarMapa(); // Limpieza total del mapa
    actualizarContador(); // Se reinicia el contador de entregas
    $('btnConfirmaNegocio').disabled = true; // Se deshabilita el botón de confirmación del negocio
}

// Reinicio total de la aplicación: limpieza y vuelta al paso 1
<<<<<<< HEAD
function reiniciar() { vaciarPuntos(); $('btnNavegar').textContent = 'Iniciar navegación'; irAPaso(1); }
=======
function reiniciar() { vaciarPuntos(); $('btnNavegar').textContent = TEXTO_SEGUIR; mostrarSiguiente('-'); irAPaso(1); }
>>>>>>> a6b004a (Cambios para ubicacion)

// Interacción con marcadores de entrega (paso 3): si se quita uno, se actualiza el contador
function alQuitarEntrega(marcador) {
    if (calculando) return;
    if (estado.paso === 3 && quitarEntrega(marcador)) actualizarContador();
}


const fueraDeCiudad = (lat, lng) =>
    mapa.distance([lat, lng], [estado.ciudad.lat, estado.ciudad.lng]) > estado.ciudad.radio_km * 1000;

function superaExtension(lat, lng) {
    const lngs = [...estado.puntos.map(p => p[0]), lng];
    const lats = [...estado.puntos.map(p => p[1]), lat];
    return Math.max(...lngs) - Math.min(...lngs) > EXTENSION_MAX_GRADOS
        || Math.max(...lats) - Math.min(...lats) > EXTENSION_MAX_GRADOS;
}

// Aplica clic/dirección buscada según el paso actual (negocio / entrega).
function colocarPunto(lat, lng) {
    if (calculando) return false;
    if ((estado.paso === 2 || estado.paso === 3) && fueraDeCiudad(lat, lng)) {
        avisar(`Fuera de ${estado.ciudad.nombre}: el límite es ${estado.ciudad.radio_km} km desde el centro.`);
        return false;
    }
    if (superaExtension(lat, lng)) { avisar('Las entregas quedarían demasiado separadas entre sí.'); return false; }

    if (estado.paso === 2) {
        const fuera = estado.puntos.slice(1)
            .some(([ln, lt]) => mapa.distance([lat, lng], [lt, ln]) > LIMITE_DISTANCIA_METROS);
        if (fuera) { avisar('Algunas entregas quedarían a más de 30 km del nuevo negocio.'); return false; }
        colocarAlmacen(lat, lng); // Coloca el marcador de negocio
        $('btnConfirmaNegocio').disabled = false; // Permite confirmar
        return true;
    } else if (estado.paso === 3) {
        if (estado.puntos.length - 1 >= MAX_PARADAS) { avisar(`Máximo ${MAX_PARADAS} paradas por viaje.`); return false; }
        const metros = distanciaAlAlmacen(lat, lng); // Calcula distancia hasta el almacén
        if (metros > LIMITE_DISTANCIA_METROS) { // Fuera del rango permitido
            avisar(`Fuera de cobertura: ${(metros / 1000).toFixed(1)} km en línea recta. El máximo es ${LIMITE_DISTANCIA_METROS / 1000} km.`);
            return false;
        }
        agregarEntrega(lat, lng, alQuitarEntrega); // Agrega el marcador de entrega y le asigna la función de callback al quitarlo
        actualizarContador(); // Se actualiza el contador de entregas
        return true;
    }
}

// Función asíncrona: Busca una dirección ingresada y coloca el marcador en el mapa.
let buscando = false;
async function buscarDireccion(idInput) {
    if (buscando) return; // Evita que se ejecute varias veces a la vez
    const entrada = $(idInput); // Obtiene el input según el id
    const texto = entrada.value.trim(); // Elimina espacios al inicio y final del texto ingresado
    if (!texto) return; // Si el campo está vacío no hace nada
    buscando=true; // Bloquea la función hasta que termine la búsqueda
    try {
        let lugar;
        try {
            lugar = await geocodificar(texto, estado.ciudad); // Espera la respuesta de geocodificación de la dirección ingresada en el input.
        } catch {
            avisar('No se pudo consultar la dirección. Revisa tu conexión e inténtalo de nuevo.');
            return;
        }

        if (!lugar) { // Si no hay resultado...
            avisar(`No encontramos esa dirección en ${estado.ciudad.nombre}. Agrega el distrito.`);
            return;
        }
        if (!colocarPunto(lugar.lat, lugar.lng)) return;// Coloca el marcador según el paso actual (negocio / entrega)
        mapa.flyTo([lugar.lat, lugar.lng], 16); // Centra el mapa en la dirección encontrada
        entrada.value = ''; // Limpia el input
    } finally {
        buscando=false; // Desbloquea la función
    }
}

// Función asíncrona: Usa el GPS del dispositivo para colocar el negocio (paso 2).
let ubicando = false;
async function usarMiUbicacion() {
    if (ubicando) return; // Evita que se ejecute varias veces a la vez
    ubicando = true;
    try {
        const { lat, lng, precision } = await obtenerUbicacion(); // Pide la posición al navegador
        if (!colocarPunto(lat, lng)) return; // Reutiliza todas las validaciones (ciudad, radio, extensión)
        mapa.flyTo([lat, lng], 16); // Centra el mapa en la ubicación
        if (precision > 150) avisar(`Precisión baja (±${Math.round(precision)} m). Puedes tocar el mapa para ajustar el punto.`);
    } catch (error) {
        avisar(error.message);
    } finally {
        ubicando = false;
    }
}

// Función asíncrona: Pide al servidor la ruta (Dijkstra -> grafo artificial -> Greedy + Or-opt),
// la dibuja sobre las calles reales, muestra sus métricas y pasa al paso 4.
async function alCalcularRuta() {
    if (calculando) return; // Evita que se ejecute varias veces a la vez
    calculando = true; // Marca que se está calculando la ruta
    const boton = $('btnCalcularRuta'); // Captura el botón de calcular ruta
    boton.disabled = true; // Lo deshabilita mientras procesa
    boton.textContent = 'Trazando ruta…'; // Texto temporal
    try { // Solicitud exitosa
        const datos = await calcularRuta(estado.ciudad.nombre, estado.puntos); // Espera la respuesta del cálculo de ruta
        dibujarRuta(datos.geometry); // Dibuja en el mapa
        numerarSegunOrden(datos.orden); // Numera los marcadores según el orden de la ruta
        mostrarMetricas(datos); // Muestra las métricas de la ruta (distancia, tiempos, etc.)
<<<<<<< HEAD
=======
        actualizarSiguiente(null); // Muestra "Parada 1 de N"
>>>>>>> a6b004a (Cambios para ubicacion)
        irAPaso(4); // Continúa al paso 4: ruta calculada y mostrada.
    } catch (error) {
        avisar(error.message); // Muestra el error en la interfaz
    } finally { // Se ejecuta SIEMPRE
        calculando = false; // Desmarca que se está calculando la ruta
        boton.textContent = 'Calcular ruta óptima'; // Restaura el texto del botón
        actualizarContador(); // Actualiza el contador de entregas
    }
}

// ---------- Seguimiento de paradas (paso 4) ----------
const formatearDistancia = m => (m < 1000 ? `${Math.round(m)} m` : `${(m / 1000).toFixed(1)} km`);

// Indice de marcador al que toca ir ahora: la siguiente parada o, si ya no quedan, el negocio (0).
const objetivoActual = () => (estado.siguiente < estado.orden.length ? estado.orden[estado.siguiente] : 0);

// Actualiza la fila "Siguiente" del panel. `metros` es null si aún no hay lectura de GPS.
function actualizarSiguiente(metros) {
    const dist = metros === null ? '' : ` · a ${formatearDistancia(metros)}`;
    if (estado.siguiente < estado.orden.length) {
        mostrarSiguiente(`Parada ${estado.siguiente + 1} de ${estado.orden.length}${dist}`);
    } else {
        mostrarSiguiente(`Regresa al negocio${dist}`);
    }
}

// Se llama con cada lectura del GPS: detecta la llegada a la parada actual y avanza a la siguiente.
function alPosicion(lat, lng) {
    const metros = distanciaAMarcador(objetivoActual(), lat, lng);
    if (metros > UMBRAL_LLEGADA_M) { actualizarSiguiente(metros); return; }

    if (estado.siguiente < estado.orden.length) {
        avanzarParada();
        avisar(`Parada ${estado.siguiente} entregada.`);
        actualizarSiguiente(null);
    } else {
        // Ya se entregó todo y llegó de vuelta al negocio
        detenerSeguimiento();
        $('btnNavegar').textContent = TEXTO_SEGUIR;
        mostrarSiguiente('Ruta completada');
        avisar('¡Ruta completada! Llegaste al negocio.');
    }
}

iniciarSplash(DURACION_SPLASH_MS); // Splash inicial con duración
iniciarAutocompletado(ciudad => { // Activación del buscador de ciudades (paso 1) con función callback
    if (ciudad.nombre !== estado.ciudad.nombre) vaciarPuntos(); // Nueva ciudad no necesita los puntos anteriores
    estado.ciudad = ciudad; // Cuando el usuario elija, la guarda en el estado
    mapa.flyTo([ciudad.lat, ciudad.lng], ciudad.z); // Centra el mapa en dicha ciudad
});

// Busca todos los elementos HTML con atributo data-ir y les asigna un controlador de clic.
// Pulsación -> conversión del valor de data-ir en un número y lo pasa a navegar, cambiando la interfaz al paso indicado.
document.querySelectorAll('[data-ir]').forEach(b => b.addEventListener('click', () => navegar(Number(b.dataset.ir))));

// Clic en el mapa: remite la latitud y longitud al método colocarPunto.
mapa.on('click', e => colocarPunto(e.latlng.lat, e.latlng.lng));

// Asignación de eventos a 2 maneras de iniciar la búsqueda: botones o Enter a input (texto de dirección) (tanto para negocio como para despacho)
[['dirNegocio', 'btnBuscarNegocio'], ['dirDespacho', 'btnBuscarDespacho']].forEach(([idInput, idBoton]) => {
    $(idBoton).addEventListener('click', () => buscarDireccion(idInput));
    $(idInput).addEventListener('keydown', e => { if (e.key === 'Enter') buscarDireccion(idInput); });
});

// Asignación de eventos a botones de acción.
$('btnCalcularRuta').addEventListener('click', alCalcularRuta);
$('btnReiniciar').addEventListener('click', reiniciar);
$('btnUbicacionNegocio').addEventListener('click', usarMiUbicacion);
<<<<<<< HEAD

// Paso 4: activa/desactiva el seguimiento GPS en vivo sobre la ruta.
$('btnNavegar').addEventListener('click', () => {
    const boton = $('btnNavegar');
    if (siguiendo()) {
        detenerSeguimiento();
        boton.textContent = 'Iniciar navegación';
    } else {
        iniciarSeguimiento(msg => { avisar(msg); boton.textContent = 'Iniciar navegación'; });
        boton.textContent = 'Detener seguimiento';
    }
});
=======
>>>>>>> a6b004a (Cambios para ubicacion)

// Paso 4: activa/desactiva el seguimiento GPS en vivo sobre la ruta.
$('btnNavegar').addEventListener('click', () => {
    const boton = $('btnNavegar');
    if (siguiendo()) {
        detenerSeguimiento();
        boton.textContent = TEXTO_SEGUIR;
    } else {
        iniciarSeguimiento(msg => { avisar(msg); boton.textContent = TEXTO_SEGUIR; }, alPosicion);
        boton.textContent = TEXTO_DETENER;
    }
});

irAPaso(1); // Inicialización de la interfaz en paso 1.