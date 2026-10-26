import { CENTRO_INICIAL, TILES } from './config.js'; // Importa la configuración del mapa OpenStreetMap France (HOT) y el centro inicial
import { estado } from './estado.js'; // Importa el estado compartido de la aplicación

export const mapa = L.map('map', { zoomControl: false }).setView(CENTRO_INICIAL, 12);
L.control.zoom({ position: 'bottomright' }).addTo(mapa);
L.tileLayer(TILES.url, TILES.opciones).addTo(mapa);

const ICONO_CASA = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/></svg>';

const iconoAlmacen = L.divIcon({
    className: '', html: `<div class="pin pin-almacen">${ICONO_CASA}</div>`,
    iconSize: [40, 40], iconAnchor: [20, 20],
});
const iconoEntrega = n => L.divIcon({
    className: '', html: `<div class="pin pin-entrega">${n}</div>`,
    iconSize: [32, 32], iconAnchor: [16, 16],
});

export function colocarAlmacen(lat, lng) {
    estado.puntos[0] = [lng, lat];
    if (estado.marcadores[0]) {
        estado.marcadores[0].setLatLng([lat, lng]);
    } else {
        estado.marcadores[0] = L.marker([lat, lng], { icon: iconoAlmacen })
            .bindTooltip('Tu negocio', { direction: 'top' }).addTo(mapa);
    }
}

export function distanciaAlAlmacen(lat, lng) {
    return mapa.distance(estado.marcadores[0].getLatLng(), [lat, lng]);
}

export function agregarEntrega(lat, lng, alHacerClic) {
    estado.puntos.push([lng, lat]);
    const n = estado.puntos.length - 1;
    const marcador = L.marker([lat, lng], { icon: iconoEntrega(n) })
        .bindTooltip(`Entrega #${n} · toca para eliminar`, { direction: 'top' })
        .on('click', () => alHacerClic(marcador))
        .addTo(mapa);
    estado.marcadores.push(marcador);
}

// Quita una entrega y renumera las otras.
export function quitarEntrega(marcador) {
    const i = estado.marcadores.indexOf(marcador);
    if (i < 1) return false;
    mapa.removeLayer(marcador);
    estado.marcadores.splice(i, 1);
    estado.puntos.splice(i, 1);
    estado.marcadores.forEach((m, k) => {
        if (k === 0) return;
        m.setIcon(iconoEntrega(k));
        m.setTooltipContent(`Entrega #${k} · toca para eliminar`);
    });
    return true;
}

// Numera los marcadores según el orden óptimo de visita.
export function numerarSegunOrden(orden) {
    orden.forEach((indice, posicion) => {
        const m = estado.marcadores[indice];
        m.setIcon(iconoEntrega(posicion + 1));
        m.setTooltipContent(`Parada ${posicion + 1}`);
    });
}

export function dibujarRuta(geometry) {
    quitarRuta();
    const opciones = { lineCap: 'round', lineJoin: 'round' };
    const borde = L.geoJSON(geometry, { style: { ...opciones, color: '#fff', weight: 9, opacity: .95 } });
    const linea = L.geoJSON(geometry, { style: { ...opciones, color: '#007aff', weight: 5 } });
    estado.capaRuta = L.layerGroup([borde, linea]).addTo(mapa);
    mapa.fitBounds(linea.getBounds(), { paddingTopLeft: [380, 50], paddingBottomRight: [50, 50] });
}

function quitarRuta() {
    if (estado.capaRuta) mapa.removeLayer(estado.capaRuta);
    estado.capaRuta = null;
}

export function limpiarMapa() {
    estado.marcadores.forEach(m => mapa.removeLayer(m));
    estado.marcadores = [];
    estado.puntos = [];
    quitarRuta();
}
