// Ubicaciones de todas las ciudades del Perú en coordenadas Latitud-Longitud y nivel de zoom para el mapa

export const CIUDADES = [
    { nombre: 'Lima', lat: -12.0464, lng: -77.0428, z: 12 },
    { nombre: 'Arequipa', lat: -16.4090, lng: -71.5375, z: 13 },
    { nombre: 'Cusco', lat: -13.5320, lng: -71.9675, z: 14 },
    { nombre: 'Trujillo', lat: -8.1091, lng: -79.0215, z: 13 },
    { nombre: 'Chiclayo', lat: -6.7714, lng: -79.8409, z: 13 },
    { nombre: 'Piura', lat: -5.1945, lng: -80.6328, z: 13 },
    { nombre: 'Iquitos', lat: -3.7491, lng: -73.2538, z: 13 },
    { nombre: 'Huancayo', lat: -12.0651, lng: -75.2049, z: 13 },
    { nombre: 'Pucallpa', lat: -8.3791, lng: -74.5539, z: 13 },
    { nombre: 'Tacna', lat: -18.0146, lng: -70.2536, z: 13 },
    { nombre: 'Ica', lat: -14.0678, lng: -75.7286, z: 13 },
    { nombre: 'Juliaca', lat: -15.4931, lng: -70.1336, z: 13 },
    { nombre: 'Puno', lat: -15.8402, lng: -70.0219, z: 14 },
    { nombre: 'Tarapoto', lat: -6.4878, lng: -76.3597, z: 13 },
    { nombre: 'Huaraz', lat: -9.5278, lng: -77.5278, z: 14 },
    { nombre: 'Cajamarca', lat: -7.1638, lng: -78.5003, z: 13 },
    { nombre: 'Ayacucho', lat: -13.1588, lng: -74.2239, z: 14 },
    { nombre: 'Huánuco', lat: -9.9306, lng: -76.2422, z: 14 },
    { nombre: 'Cerro de Pasco', lat: -10.6675, lng: -76.2567, z: 14 },
    { nombre: 'Chimbote', lat: -9.0763, lng: -78.5936, z: 13 },
    { nombre: 'Tumbes', lat: -3.5669, lng: -80.4515, z: 14 },
    { nombre: 'Puerto Maldonado', lat: -12.5933, lng: -69.1836, z: 14 },
    { nombre: 'Moquegua', lat: -17.1983, lng: -70.9357, z: 14 },
    { nombre: 'Abancay', lat: -13.6339, lng: -72.8814, z: 14 },
    { nombre: 'Chachapoyas', lat: -6.2294, lng: -77.8728, z: 14 },
    { nombre: 'Moyobamba', lat: -6.0342, lng: -76.9723, z: 14 },
    { nombre: 'Huancavelica', lat: -12.7826, lng: -74.9727, z: 14 },
];

let n_ciudadInicial = 'Lima'; // Ciudad inicial por defecto

export const ciudadInicial = CIUDADES.find(ciudad => ciudad.nombre === n_ciudadInicial); // Dict que guarda los datos de la ciudad inicial
