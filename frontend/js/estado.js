// Estado compartido de la aplicación. puntos[i] = [lng, lat]; marcadores[i] es su marcador de Leaflet. Índice 0 = almacén.
export const estado = {
    paso: 1,
    ciudad: { nombre: 'Lima', lat: -12.0464, lng: -77.0428 },
    puntos: [],
    marcadores: [],
    capaRuta: null,
};
