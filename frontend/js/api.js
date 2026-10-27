import { API_URL, MARGEN_BUSQUEDA_GRADOS, NOMINATIM_URL } from './config.js'; // Importa ruta de la API, el motor de geocodificación y el margen de búsqueda alrededor de la ciudad

// Función asíncrona: Envía la ciudad y los puntos; recibe un objeto con las métricas de la ruta óptima calculada por el servidor.
export async function calcularRuta(ciudad, puntos) {

    // Solicitud POST a la API que envía un JSON con la ciudad y los puntos.
    const respuesta = await fetch(`${API_URL}/ruta`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ciudad, puntos }),
    });
    const datos = await respuesta.json().catch(() => ({})); //  Espera e intenta obtener un JSON con las métricas de la ruta óptima
    if (!respuesta.ok) throw new Error(datos.error || 'Error desconocido'); // Si hay error, lanza una excepción.
    return datos; 
}

// Petición al servidor para que vaya descargando el mapa del almacén mientras el usuario sigue eligiendo.
export function precargarMapa(punto) {

    // Intenta enviar la solicitud POST a la API (que envía un JSON con el punto del negocio) para que se realice en 2do plano
    fetch(`${API_URL}/precargar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ punto }),
    }).catch(() => {});
}

// Función asíncrona: Busca en Norminatim las coordenadas de la dirección ingresada restringida a la ciudad. Devuelve { lat, lng } o null si no hay resultado dentro de la ciudad.
export async function geocodificar(texto, ciudad) {
    const o = MARGEN_BUSQUEDA_GRADOS; // Zona de búsqueda alrededor de la ciudad (grados decimales)
    const caja = [ciudad.lng - o, ciudad.lat + o, ciudad.lng + o, ciudad.lat - o].join(','); // Limites de la zona (longitud y latitud máximas y mínimas)
    const consulta = encodeURIComponent(`${texto}, ${ciudad.nombre}, Perú`); // Construye la consulta
    const url = `${NOMINATIM_URL}?format=json&q=${consulta}&viewbox=${caja}&bounded=1&limit=1`; // Se arma la URL de la API de Nominatim con los parámetros de búsqueda
    const datos = await (await fetch(url)).json(); // Se esperan resultados JSON de la solicitud.
    return datos.length ? { lat: parseFloat(datos[0].lat), lng: parseFloat(datos[0].lon) } : null; // Convierte coordenadas (texto->numero).
}
