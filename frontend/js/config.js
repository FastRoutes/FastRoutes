export const API_URL = '/api';
export const LIMITE_DISTANCIA_METROS = 30000;   // regla de negocio: 30 km desde el almacén
export const CENTRO_INICIAL = [-12.0464, -77.0428];
export const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search';
export const MARGEN_BUSQUEDA_GRADOS = 0.15;     // caja de búsqueda alrededor de la ciudad
export const DURACION_SPLASH_MS = 3000;
export const TILES = {
    url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    opciones: {
        maxZoom: 19, subdomains: 'abcd',
        attribution: '© OpenStreetMap contributors © CARTO',
    },
};
