import { CIUDADES } from './ciudades.js';
import { estado } from './estado.js';

export const $ = id => document.getElementById(id);
const normalizar = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();

export function irAPaso(paso) {
    document.querySelectorAll('.paso-contenedor').forEach(el => el.classList.remove('activo'));
    $(`paso${paso}`).classList.add('activo');
    document.querySelectorAll('#progreso span').forEach((punto, i) => {
        punto.classList.toggle('activo', i < paso);
        punto.classList.toggle('actual', i === paso - 1);
    });
    estado.paso = paso;
}

export function actualizarContador() {
    const entregas = Math.max(0, estado.puntos.length - 1);
    $('contador').textContent = entregas;
    $('btnCalcularRuta').disabled = entregas === 0;
}

export function mostrarMetricas(datos) {
    $('textoMetodo').textContent = `Orden ${datos.metodo}.`;
    $('rDistancia').textContent = `${(datos.distancia_m / 1000).toFixed(2)} km`;
    $('rParadas').textContent = datos.paradas;
    $('rMovimiento').textContent = `${datos.duracion_movimiento_min} min`;
    $('rServicio').textContent = `${datos.tiempo_servicio_min} min`;
    $('rTotal').textContent = `${datos.tiempo_total_min} min`;
}

let temporizadorAviso;
export function avisar(mensaje) {
    const aviso = $('aviso');
    aviso.textContent = mensaje;
    aviso.classList.add('visible');
    clearTimeout(temporizadorAviso);
    temporizadorAviso = setTimeout(() => aviso.classList.remove('visible'), 4000);
}

export function iniciarAutocompletado(alElegir) {
    const entrada = $('buscadorCiudad');
    const lista = $('listaCiudades');
    const continuar = $('btnContinuarPaso1');

    entrada.addEventListener('input', () => {
        const texto = normalizar(entrada.value);
        lista.replaceChildren();
        continuar.disabled = true;
        const coincidencias = texto ? CIUDADES.filter(c => normalizar(c.nombre).includes(texto)) : [];
        lista.style.display = coincidencias.length ? 'block' : 'none';

        coincidencias.forEach(ciudad => {
            const item = document.createElement('div');
            item.className = 'lista-item';
            item.textContent = ciudad.nombre;
            item.addEventListener('click', () => {
                entrada.value = ciudad.nombre;
                lista.style.display = 'none';
                continuar.disabled = false;
                alElegir(ciudad);
            });
            lista.appendChild(item);
        });
    });
    document.addEventListener('click', e => { if (!e.target.closest('.campo')) lista.style.display = 'none'; });
}

export function iniciarSplash(duracionMs) {
    setTimeout(() => {
        const splash = $('splash');
        splash.style.opacity = '0';
        setTimeout(() => {
            splash.style.display = 'none';
            $('panel').style.display = 'block';
            requestAnimationFrame(() => requestAnimationFrame(() => $('panel').classList.add('visible')));
        }, 600);
    }, duracionMs);
}
