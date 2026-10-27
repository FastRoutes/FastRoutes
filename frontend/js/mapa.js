import { CENTRO_INICIAL, TILES } from './config.js'; // Importa la configuración del mapa OpenStreetMap France (HOT) y el centro inicial
import { estado } from './estado.js'; // Importa el estado compartido de la aplicación

export const mapa = L.map('map', { zoomControl: false }).setView(CENTRO_INICIAL, 12); // Crea un mapa Leaflet centrado con zoom 12. Es un elemento HTML con id="map".
L.control.zoom({ position: 'bottomright' }).addTo(mapa); // Implementación de un zoom-controller en la esquina inferior derecha del mapa
L.tileLayer(TILES.url, TILES.opciones).addTo(mapa); // Carga los tiles desde OSM France (HOT) y los añade al mapa

// Marcadores de almacén y puntos de entrega: Casa es un SVG para el marcador de negocio. Se usa divIcon para poder personalizar el contenido HTML y el estilo CSS.
const ICONO_CASA = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/></svg>';
const iconoAlmacen = L.divIcon({
    className: '', html: `<div class="pin pin-almacen">${ICONO_CASA}</div>`,
    iconSize: [40, 40], iconAnchor: [20, 20],
});
const iconoEntrega = n => L.divIcon({ //
    className: '', html: `<div class="pin pin-entrega">${n}</div>`, // Con n se enumeran los puntos de entrega
    iconSize: [32, 32], iconAnchor: [16, 16],
});

// Colocador del marcador de negocio en el mapa Leaflet.
export function colocarAlmacen(lat, lng) {
    estado.puntos[0] = [lng, lat]; //Guarda la posición como el índice 0 del array puntos del estado compartido.
    if (estado.marcadores[0]) {
        estado.marcadores[0].setLatLng([lat, lng]); // Si ya existe un marcador de negocio, actualiza su posición.
    } else {
        estado.marcadores[0] = L.marker([lat, lng], { icon: iconoAlmacen }) // Creación en el mapa con su icono
            .bindTooltip('Tu negocio', { direction: 'top' }).addTo(mapa);
    }
}

// Función que calcula la distancia en m desde una posición hacia el almacén (útil para validación de radio).
export function distanciaAlAlmacen(lat, lng) {
    return mapa.distance(estado.marcadores[0].getLatLng(), [lat, lng]);
}

// Agrega un marcador de entrega en el mapa y lo guarda en el estado compartido. Parámetro alHacerClic: función ejecutada al hacer clic sobre el marcador.
export function agregarEntrega(lat, lng, alHacerClic) {
    estado.puntos.push([lng, lat]); // Lo añade como el siguiente índice del array puntos del estado compartido.
    const n = estado.puntos.length - 1; // Número de entrega = índice del array puntos menos 1 (el almacén).
    const marcador = L.marker([lat, lng], { icon: iconoEntrega(n) }) // Crea el marcador de entrega enumerada y , si se clickea, sucede algo (la función que la utilice lo define).
        .bindTooltip(`Entrega #${n} · toca para eliminar`, { direction: 'top' })
        .on('click', () => alHacerClic(marcador))
        .addTo(mapa);
    estado.marcadores.push(marcador); // Añade el marcador como el siguiente índice del array marcadores del estado compartido.
}

export function quitarEntrega(marcador) {
    const i = estado.marcadores.indexOf(marcador); // Devuelve el índex del marcador
    if (i < 1) return false; // No permite quitar el marcador de negocio
    mapa.removeLayer(marcador); // Quita el marcador del mapa

    // Quita el marcador y el punto del estado compartido
    estado.marcadores.splice(i, 1);
    estado.puntos.splice(i, 1);
    estado.marcadores.forEach((m, k) => { // Reenumerar los marcadores de entrega restantes. k es el índice del marcador en el array marcadores.
        if (k === 0) return;
        m.setIcon(iconoEntrega(k));
        m.setTooltipContent(`Entrega #${k} · toca para eliminar`);
    });
    return true;
}

// Numera los marcadores según el orden óptimo de visita.
export function numerarSegunOrden(orden) {
    orden.forEach((indice, posicion) => { // Recorrido del array orden de índices de marcadores
        const m = estado.marcadores[indice]; // Obtiene el marcador correspondiente al índice
        m.setIcon(iconoEntrega(posicion + 1)); // Actualiza el icono del marcador con el nuevo número de parada
        m.setTooltipContent(`Parada ${posicion + 1}`); // Actualiza el contenido del tooltip del marcador
    });
}

export function dibujarRuta(geometry) {
    quitarRuta(); // Empezar de 0

    // Se definen los estilos para trazar la ruta. L.geoJSON para crear capas a partir de la geometría GeoJSON devuelta por el servidor.
    const opciones = { lineCap: 'round', lineJoin: 'round' };
    const borde = L.geoJSON(geometry, { style: { ...opciones, color: '#fff', weight: 9, opacity: .95 } });
    const linea = L.geoJSON(geometry, { style: { ...opciones, color: '#007aff', weight: 5 } });
    estado.capaRuta = L.layerGroup([borde, linea]).addTo(mapa); // Añade la capa de la ruta al mapa
    mapa.fitBounds(linea.getBounds(), { paddingTopLeft: [380, 50], paddingBottomRight: [50, 50] }); // Ajusta el mapa para visualizar la ruta
}

// Si hay una ruta en el estado, se elimina y se reestablece a null.
function quitarRuta() {
    if (estado.capaRuta) mapa.removeLayer(estado.capaRuta);
    estado.capaRuta = null;
}

// Se borran todos los marcadores y puntos del estado compartido: reinicio. Se borra la ruta existente.
export function limpiarMapa() {
    estado.marcadores.forEach(m => mapa.removeLayer(m));
    // Reinicia ambos arrays
    estado.marcadores = []; 
    estado.puntos = [];
    quitarRuta();
}
