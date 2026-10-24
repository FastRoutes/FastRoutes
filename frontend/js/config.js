export const API_URL = '/api';
export const LIMITE_DISTANCIA_METROS = 30000;   // Regla de negocio (30 km desde el negocio)
export const CENTRO_INICIAL = [-12.0464, -77.0428]; // Por defecto empieza en Lima
export const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search';
export const MARGEN_BUSQUEDA_GRADOS = 0.15;     // Caja de búsqueda alrededor de la ciudad
export const DURACION_SPLASH_MS = 3000;

// Para el mapa original del proyecto se utiliza OpenStreetMap France (HOT) (sin API key)
export const TILES = {
    url: 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
    opciones: { maxZoom: 19, attribution: '© OpenStreetMap contributors' },
};
