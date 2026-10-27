// Ubicaciones de todas las ciudades del Perú en coordenadas Latitud-Longitud y nivel de zoom para el mapa

export const CIUDADES = await (await fetch('/ciudades.json')).json();

let n_ciudadInicial = 'Lima'; // Ciudad inicial por defecto

export const ciudadInicial = CIUDADES.find(ciudad => ciudad.nombre === n_ciudadInicial); // Dict que guarda los datos de la ciudad inicial
