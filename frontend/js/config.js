import { ciudadInicial } from './ciudades.js'; // Importa la ciudad inicial definida

export const API_URL = '/api'; // URL ruta base para las llamadas a la API
export const LIMITE_DISTANCIA_METROS = 30000;   // Para no ir más allá de 30km alrededor del negocio (Regla de negocio)
export const CENTRO_INICIAL = [ciudadInicial.lat, ciudadInicial.lng]; // Coordenadas de la ciudad inicial: inicia ahí por defecto
export const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'; // Motor de geocodificación de OpenStreetMap (Sin API-key)
export const MARGEN_BUSQUEDA_GRADOS = 0.15; // Caja de búsqueda alrededor de la ciudad
export const DURACION_SPLASH_MS = 3000; // Tiempo que dura lo que sale al inicio en ms

// Para crear el mapa sin depender de API-key, se utilizó OpenStreetMap France (HOT)
export const TILES = {
    url: 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
    opciones: { maxZoom: 19, attribution: '© OpenStreetMap contributors' },
};
