import { API_URL, MARGEN_BUSQUEDA_GRADOS, NOMINATIM_URL } from './config.js'; // Importa ruta de la API, el motor de geocodificación y el margen de búsqueda alrededor de la ciudad


async function postJSON(ruta, cuerpo, { timeoutMs = 120000 } = {}) {
    const control = new AbortController();
    const temporizador = setTimeout(() => control.abort(), timeoutMs);
    try {
        const respuesta = await fetch(`${API_URL}${ruta}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(cuerpo),
            signal: control.signal,
        });
        const datos = await respuesta.json().catch(() => ({}));
        if (!respuesta.ok) throw new Error(datos.error || `Error del servidor (${respuesta.status})`);
        return datos;
    } catch (e) {
        if (e.name === 'AbortError') throw new Error('El servidor tardó demasiado. Inténtalo de nuevo.');
        if (e instanceof TypeError) throw new Error('No hay conexión con el servidor.');
        throw e;
    } finally {
        clearTimeout(temporizador);
    }
}


// Función asíncrona: Envía la ciudad y los puntos; recibe un objeto con las métricas de la ruta óptima calculada por el servidor.
export const calcularRuta = (ciudad, puntos) => postJSON('/ruta', { ciudad, puntos });

// Petición al servidor para que vaya descargando el mapa del almacén mientras el usuario sigue eligiendo.
export function precargarMapa(punto, ciudad) {
    postJSON('/precargar', { punto, ciudad }, { timeoutMs: 10000 }).catch(() => {});
}

// Función asíncrona: Busca en Norminatim las coordenadas de la dirección ingresada restringida a la ciudad. Devuelve { lat, lng } o null si no hay resultado dentro de la ciudad.
export async function geocodificar(texto, ciudad) {
    const o = MARGEN_BUSQUEDA_GRADOS; // Zona de búsqueda alrededor de la ciudad (grados decimales)
    const caja = [ciudad.lng - o, ciudad.lat + o, ciudad.lng + o, ciudad.lat - o].join(','); // Limites de la zona (longitud y latitud máximas y mínimas)
    const consulta = encodeURIComponent(`${texto}, ${ciudad.nombre}, Perú`); // Construye la consulta
    const url = `${NOMINATIM_URL}?format=json&q=${consulta}&viewbox=${caja}&bounded=1&limit=1`; // Se arma la URL de la API de Nominatim con los parámetros de búsqueda
    const respuesta = await fetch(url);
    if (!respuesta.ok) throw new Error(`Nominatim respondió ${respuesta.status}`);
    const datos = await respuesta.json(); // Se esperan resultados JSON de la solicitud.
    return datos.length ? { lat: parseFloat(datos[0].lat), lng: parseFloat(datos[0].lon) } : null; // Convierte coordenadas (texto->numero).
}
