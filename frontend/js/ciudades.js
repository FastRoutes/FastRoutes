// Ubicaciones de todas las ciudades del Perú en coordenadas Latitud-Longitud y nivel de zoom para el mapa

async function cargarCiudades() {
    try {
        const respuesta = await fetch('/ciudades.json');
        if (!respuesta.ok) throw new Error(`HTTP ${respuesta.status}`);
        return await respuesta.json();
    } catch (error) {
        console.error('No se pudo cargar ciudades.json', error);
        document.body.textContent = 'No se pudo cargar la lista de ciudades. Recarga la página.';
        throw error;
    }
}

export const CIUDADES = await cargarCiudades();

const NOMBRE_CIUDAD_INICIAL = 'Lima'; // Ciudad inicial por defecto

export const ciudadInicial = CIUDADES.find(c => c.nombre === NOMBRE_CIUDAD_INICIAL) ?? CIUDADES[0]; // Dict que guarda los datos de la ciudad inicial
