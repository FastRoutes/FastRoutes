import { CIUDADES } from './ciudades.js'; // Importa la lista de ciudades con coordenadas
import { estado } from './estado.js'; // Importa el estado compartido de la aplicación

export const $ = id => document.getElementById(id); // Función para obtener elementos por ID
const normalizar = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim(); // Función que normaliza strings a solo minúsculas normales

// Navegación entre pasos del flujo de la aplciación
export function irAPaso(paso) {
    document.querySelectorAll('.paso-contenedor').forEach(el => el.classList.remove('activo')); // Desactiva todos los pasos
    $(`paso${paso}`).classList.add('activo'); // Encuentra el id del paso y lo activa
    document.querySelectorAll('#progreso span').forEach((punto, i) => { // Recorrido sobre los puntos de progreso para actualizar su estado
        punto.classList.toggle('activo', i < paso); // Activa cualquier paso ya recorrido
        punto.classList.toggle('actual', i === paso - 1); // Define como actual el paso actual
    });
    estado.paso = paso; // Actualiza el paso del estado compartido
}

// Actualiza el contador de entregas y el estado del botón de calcular ruta
export function actualizarContador() {
    const entregas = Math.max(0, estado.puntos.length - 1); // Nº puntos de entrega (se resta el almacén)
    $('contador').textContent = entregas; // Actualiza el contador en la interfaz
    $('btnCalcularRuta').disabled = entregas === 0; // Desactiva el botón si no hay entregas
}

// Mostrar todas las métricas de la ruta generada: Distancia, paradas, tiempo de movimiento, tiempo de servicio y tiempo total.
export function mostrarMetricas(datos) {
    $('textoMetodo').textContent = `Orden ${datos.metodo}.`;
    $('rDistancia').textContent = `${(datos.distancia_m / 1000).toFixed(2)} km`;
    $('rParadas').textContent = datos.paradas;
    $('rMovimiento').textContent = `${datos.duracion_movimiento_min} min`;
    $('rServicio').textContent = `${datos.tiempo_servicio_min} min`;
    $('rTotal').textContent = `${datos.tiempo_total_min} min`;
}

let temporizadorAviso; // Guardará el temporizador
export function avisar(mensaje) {
    const aviso = $('aviso'); // Busca el elemento "aviso"
    aviso.textContent = mensaje; // Lo reemplaza con el mensaje
    aviso.classList.add('visible'); // Lo hace aparecer
    clearTimeout(temporizadorAviso); // Cancela cualquier temporizador previo
    temporizadorAviso = setTimeout(() => aviso.classList.remove('visible'), 4000); // Desaparición en 4s / 4000ms
}

export function iniciarAutocompletado(alElegir) { // Función invocada cuando se selecciona la ciudad
    const entrada = $('buscadorCiudad'); // Elemento donde se escribe la ciudad
    const lista = $('listaCiudades'); // Elemento de sugerencias
    const continuar = $('btnContinuarPaso1'); // Botón de continuar al paso 2

    // Cada vez que se teclea/borra...
    entrada.addEventListener('input', () => { 
        const texto = normalizar(entrada.value); // Se normaliza el texto del input
        lista.replaceChildren(); // Elimina las sugerencias anteriores
        continuar.disabled = true; // Hasta que no se seleccione una ciudad, no se puede pulsar el botón
        const coincidencias = texto ? CIUDADES.filter(c => normalizar(c.nombre).includes(texto)) : []; // Se filtra CIUDADES para que muestre sugerencias según lo escrito
        lista.style.display = coincidencias.length ? 'block' : 'none'; // Si hay coincidencias muestra la lista; si no, se oculta

        // Recorrido sobre ciudades encontradas para crear elementos de sugerencia
        coincidencias.forEach(ciudad => {
            const item = document.createElement('div');
            item.className = 'lista-item';
            item.textContent = ciudad.nombre;
            item.addEventListener('click', () => { // Si se clickea...
                entrada.value = ciudad.nombre; // Se coloca el nombre de la ciudad en el input
                lista.style.display = 'none'; // Se ocultan las sugerencias
                continuar.disabled = false; // El botón se habilita
                alElegir(ciudad); // Se invoca ya con la ciudad seleccionada
            });
            lista.appendChild(item); // Añade la sugerencia creada a la lista de sugerencias
        });
    });
    document.addEventListener('click', e => { if (!e.target.closest('.campo')) lista.style.display = 'none'; }); // Si se hace click fuera del input, se oculta la lista de sugerencias
}

// Lo que sale al inicio: transición entre logo y programa.
export function iniciarSplash(duracionMs) {
    $('splash-delivery').classList.add('andando');
    setTimeout(() => {
        const splash = $('splash'); // Busca el elemento "splash"
        splash.style.opacity = '0'; // Opacidad 0 = se desvanece al pasar duracionMs
        setTimeout(() => {
            splash.style.display = 'none'; // Se oculta el splash tras 600ms
            $('panel').style.display = 'block'; // Se muestra el panel
            requestAnimationFrame(() => requestAnimationFrame(() => $('panel').classList.add('visible'))); // Visibiliza el panel tras 2 frames (transición)
        }, 600);
    }, duracionMs);
}
