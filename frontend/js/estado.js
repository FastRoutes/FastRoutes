import { CIUDADES, ciudadInicial } from './ciudades.js'; // Importa todas las ciudades y la ciudad inicial definida

// Estado compartido de la aplicación que guarda los datos del mapa.
// puntos[i] = [lng, lat]; marcadores[i] es su marcador de Leaflet. Índice 0 = almacén.
export const estado = {
    paso: 1,
    ciudad: { nombre: ciudadInicial.nombre, lat: ciudadInicial.lat, lng: ciudadInicial.lng }, // ciudad inicial
    puntos: [], // Lista vacía que almacenará pares [longitud, latitud] de los puntos que se van agregando
    marcadores: [], // Lista vacía que almacenará los marcadores de Leaflet (librería de mapa interactivo) que se van agregando
    capaRuta: null, // No hay ruta inicial
};
