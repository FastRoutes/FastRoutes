import { API_URL, MARGEN_BUSQUEDA_GRADOS, NOMINATIM_URL } from './config.js';

export async function calcularRuta(ciudad, puntos) {
    const respuesta = await fetch(`${API_URL}/ruta`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ciudad, puntos }),
    });
    const datos = await respuesta.json().catch(() => ({}));
    if (!respuesta.ok) throw new Error(datos.error || 'Error desconocido');
    return datos;
}

/** Pide al servidor que vaya descargando el mapa del almacén mientras el usuario sigue eligiendo. */
export function precargarMapa(punto) {
    fetch(`${API_URL}/precargar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ punto }),
    }).catch(() => {});
}

/** Devuelve { lat, lng } o null si no hay resultado dentro de la ciudad. */
export async function geocodificar(texto, ciudad) {
    const o = MARGEN_BUSQUEDA_GRADOS;
    const caja = [ciudad.lng - o, ciudad.lat + o, ciudad.lng + o, ciudad.lat - o].join(',');
    const consulta = encodeURIComponent(`${texto}, ${ciudad.nombre}, Perú`);
    const url = `${NOMINATIM_URL}?format=json&q=${consulta}&viewbox=${caja}&bounded=1&limit=1`;
    const datos = await (await fetch(url)).json();
    return datos.length ? { lat: parseFloat(datos[0].lat), lng: parseFloat(datos[0].lon) } : null;
}
