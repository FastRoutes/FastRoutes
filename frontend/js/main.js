// Archivo central JavaScript del FrontEnd. Encargada de la interacción usuario-servidor. Importa funciones y constantes del resto de módulos .js. Se ejecuta al cargar la página.
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

function navegar(paso) {
    // Si el negocio ha sido confirmado (paso 2 en estado), se inicia la precarga del mapa alrededor de este.
    if (paso === 3 && estado.paso === 2) precargarMapa(estado.puntos[0]);
    irAPaso(paso); // Se actualiza el estado a paso 3 (confirmación de entregas).
}

// Reinicio total de la aplicación
function reiniciar() {
    limpiarMapa(); // Limpieza total del mapa
    actualizarContador(); // Se reinicia el contador de entregas
    $('btnConfirmaNegocio').disabled = true; // Se deshabilita el botón de confirmación del negocio
    irAPaso(1); // Volvemos al paso 1: seleccionar ciudad.
}

// Interacción con marcadores de entrega (paso 3): si se quita uno, se actualiza el contador
function alQuitarEntrega(marcador) {
    if (estado.paso === 3 && quitarEntrega(marcador)) actualizarContador();
}

// Aplica clic/dirección buscada según el paso actual (negocio / entrega).
function colocarPunto(lat, lng) {
    if (estado.paso === 2) {
        colocarAlmacen(lat, lng); // Coloca el marcador de negocio
        $('btnConfirmaNegocio').disabled = false; // Permite confirmar
    } else if (estado.paso === 3) {
        const metros = distanciaAlAlmacen(lat, lng); // Calcula distancia hasta el almacén
        if (metros > LIMITE_DISTANCIA_METROS) { // Fuera del rango permitido
            avisar(`Fuera de cobertura: ${(metros / 1000).toFixed(1)} km en línea recta. El máximo es ${LIMITE_DISTANCIA_METROS / 1000} km.`);
            return;
        }
        agregarEntrega(lat, lng, alQuitarEntrega); // Agrega el marcador de entrega y le asigna la función de callback al quitarlo
        actualizarContador(); // Se actualiza el contador de entregas
    }
}

// Función asíncrona: Busca una dirección ingresada y coloca el marcador en el mapa.
async function buscarDireccion(idInput) {
    const entrada = $(idInput); // Obtiene el input según el id
    const texto = entrada.value.trim(); // Elimina espacios al inicio y final del texto ingresado
    if (!texto) return; // Si el campo está vacío no hace nada
    try {
        const lugar = await geocodificar(texto, estado.ciudad); // Espera la respuesta de geocodificación de la dirección ingresada en el input. 
        if (!lugar) { // Si no hay resultado...
            avisar(`No encontramos esa dirección en ${estado.ciudad.nombre}. Agrega el distrito.`);
            return;
        }
        colocarPunto(lugar.lat, lugar.lng); // Coloca el marcador según el paso actual (negocio / entrega)
        mapa.flyTo([lugar.lat, lugar.lng], 16); // Centra el mapa en la dirección encontrada
        entrada.value = ''; // Limpia el input
    } catch {
        avisar('Sin conexión al buscar la dirección. Inténtalo de nuevo.'); // Fallo de conexión al procesar la respuesta
    }
}

// Función asíncrona: Calcula y dibuja la ruta óptima, muestra sus métricas y pasa al paso 4.
async function alCalcularRuta() {
    const boton = $('btnCalcularRuta'); // Captura el botón de calcular ruta
    boton.disabled = true; // Lo deshabilita mientras procesa
    boton.textContent = 'Trazando ruta…'; // Texto temporal
    try { // Solicitud exitosa
        const datos = await calcularRuta(estado.ciudad.nombre, estado.puntos); // Espera la respuesta del cálculo de ruta óptima
        dibujarRuta(datos.geometry); // Dibuja en el mapa
        numerarSegunOrden(datos.orden); // Numera los marcadores según el orden de la ruta
        mostrarMetricas(datos); // Muestra las métricas de la ruta (distancia, tiempos, etc.)
        irAPaso(4); // Continúa al paso 4: ruta óptima calculada y mostrada.
    } catch (error) {
        avisar(error.message);
    } finally { // Se ejecuta SIEMPRE
        boton.textContent = 'Calcular ruta óptima'; // Restaura el texto del botón
        actualizarContador(); // Actualiza el contador de entregas
    }
}

iniciarSplash(DURACION_SPLASH_MS); // Splash inicial con duración
iniciarAutocompletado(ciudad => { // Activación del buscador de ciudades (paso 1) con función callback
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
$('btnCalcularRuta').addEventListener('click', alCalcularRuta); // 
$('btnReiniciar').addEventListener('click', reiniciar);
$('btnNavegar').addEventListener('click', () =>
    avisar('La navegación paso a paso llegará en la siguiente versión.'));

irAPaso(1); // Inicialización de la interfaz en paso 1.
