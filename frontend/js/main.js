import { calcularRuta, geocodificar, precargarMapa } from './api.js';
import { DURACION_SPLASH_MS, LIMITE_DISTANCIA_METROS } from './config.js';
import { estado } from './estado.js';
import {
    agregarEntrega, colocarAlmacen, dibujarRuta, distanciaAlAlmacen,
    limpiarMapa, mapa, numerarSegunOrden, quitarEntrega,
} from './mapa.js';
import {
    $, actualizarContador, avisar, irAPaso, iniciarAutocompletado, iniciarSplash, mostrarMetricas,
} from './panel.js';

// ---------------------------------------------------------------- Navegación
function navegar(paso) {
    // Al confirmar el negocio, el servidor empieza a bajar el mapa mientras se eligen las entregas
    if (paso === 3 && estado.paso === 2) precargarMapa(estado.puntos[0]);
    irAPaso(paso);
}

function reiniciar() {
    limpiarMapa();
    actualizarContador();
    $('btnConfirmaNegocio').disabled = true;
    irAPaso(1);
}

// ------------------------------------------------------------ Puntos en el mapa
function alQuitarEntrega(marcador) {
    if (estado.paso === 3 && quitarEntrega(marcador)) actualizarContador();
}

/** Aplica el clic (o la dirección buscada) según el paso actual. */
function colocarPunto(lat, lng) {
    if (estado.paso === 2) {
        colocarAlmacen(lat, lng);
        $('btnConfirmaNegocio').disabled = false;
    } else if (estado.paso === 3) {
        const metros = distanciaAlAlmacen(lat, lng);
        if (metros > LIMITE_DISTANCIA_METROS) {
            avisar(`Fuera de cobertura: ${(metros / 1000).toFixed(1)} km en línea recta. El máximo es ${LIMITE_DISTANCIA_METROS / 1000} km.`);
            return;
        }
        agregarEntrega(lat, lng, alQuitarEntrega);
        actualizarContador();
    }
}

async function buscarDireccion(idInput) {
    const entrada = $(idInput);
    const texto = entrada.value.trim();
    if (!texto) return;
    try {
        const lugar = await geocodificar(texto, estado.ciudad);
        if (!lugar) {
            avisar(`No encontramos esa dirección en ${estado.ciudad.nombre}. Agrega el distrito.`);
            return;
        }
        colocarPunto(lugar.lat, lugar.lng);
        mapa.flyTo([lugar.lat, lugar.lng], 16);
        entrada.value = '';
    } catch {
        avisar('Sin conexión al buscar la dirección. Inténtalo de nuevo.');
    }
}

// ------------------------------------------------------------------ Ruta
async function alCalcularRuta() {
    const boton = $('btnCalcularRuta');
    boton.disabled = true;
    boton.textContent = 'Trazando ruta…';
    try {
        const datos = await calcularRuta(estado.ciudad.nombre, estado.puntos);
        dibujarRuta(datos.geometry);
        numerarSegunOrden(datos.orden);
        mostrarMetricas(datos);
        irAPaso(4);
    } catch (error) {
        avisar(error.message);
    } finally {
        boton.textContent = 'Calcular ruta óptima';
        actualizarContador();
    }
}

// ---------------------------------------------------------------- Arranque
iniciarSplash(DURACION_SPLASH_MS);
iniciarAutocompletado(ciudad => {
    estado.ciudad = ciudad;
    mapa.flyTo([ciudad.lat, ciudad.lng], ciudad.z);
});

document.querySelectorAll('[data-ir]').forEach(b => b.addEventListener('click', () => navegar(Number(b.dataset.ir))));
mapa.on('click', e => colocarPunto(e.latlng.lat, e.latlng.lng));

[['dirNegocio', 'btnBuscarNegocio'], ['dirDespacho', 'btnBuscarDespacho']].forEach(([idInput, idBoton]) => {
    $(idBoton).addEventListener('click', () => buscarDireccion(idInput));
    $(idInput).addEventListener('keydown', e => { if (e.key === 'Enter') buscarDireccion(idInput); });
});

$('btnCalcularRuta').addEventListener('click', alCalcularRuta);
$('btnReiniciar').addEventListener('click', reiniciar);
$('btnNavegar').addEventListener('click', () =>
    avisar('La navegación paso a paso llegará en la siguiente versión.'));

irAPaso(1);
