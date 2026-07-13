/**
 * Lanza un pop-up de error completamente parametrizable y centrado.
 * Se cierra automáticamente después de 11 segundos.
 * @param {string} titulo - El título que aparecerá en el encabezado.
 * @param {string} mensaje - El texto informativo o cuerpo del error.
 */
function lanzarPopupError(titulo, mensaje) {
    const contenedorGlobal = document.getElementById('contenedor-popups-global');
    const plantilla = document.getElementById('plantilla-popup-error');

    if (!contenedorGlobal || !plantilla) {
        console.error('No se encontraron los elementos HTML del pop-up en el DOM.');
        return;
    }

    const clon = plantilla.content.cloneNode(true);
    clon.querySelector('.popup-titulo').textContent = titulo;
    clon.querySelector('.popup-mensaje').textContent = mensaje;

    const elementoPopupReal = clon.querySelector('.popup-fondo-bloqueo');
    const botonCerrar = clon.querySelector('.popup-boton-cerrar');

    const destruirPopup = () => {
        if (elementoPopupReal && elementoPopupReal.parentNode) {
            elementoPopupReal.remove();
        }
    };

    const temporizadorAutoCierre = setTimeout(destruirPopup, 5000);

    botonCerrar.addEventListener('click', () => {
        clearTimeout(temporizadorAutoCierre);
        destruirPopup();
    });

    contenedorGlobal.appendChild(elementoPopupReal);
}

/**
 * Consulta una escuela a la API de forma asíncrona.
 * Si no existe, muestra el pop-up de error y mantiene al usuario en la misma pantalla.
 * @param {number|string} idEscuela - El identificador de la escuela a consultar.
 */
async function consultarEscuelaPorId(idEscuela) {
    try {
        if (!idEscuela) {
            lanzarPopupError('Error de Aplicación', 'No se pudo determinar la escuela a buscar.');
            return;
        }

        const url = `/escuelas/${idEscuela}`;
        const respuesta = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'text/html'
            }
        });

        if (respuesta.status === 404) {
            let mensaje = 'La escuela que estás buscando no existe en el sistema.';
            try {
                const json = await respuesta.json();
                mensaje = json.detail || mensaje;
            } catch (e) {
                // Si no viene JSON, usar mensaje por defecto.
            }
            lanzarPopupError('Error de Aplicación', mensaje);
            return;
        }

        if (respuesta.status === 403) {
            let mensaje = 'No tienes permisos para modificar este recurso.';
            try {
                const json = await respuesta.json();
                mensaje = json.detail || mensaje;
            } catch (e) {
            }
            lanzarPopupError('Acceso Restringido', mensaje);
            return;
        }

        if (!respuesta.ok) {
            let mensaje = 'Ocurrió un problema al procesar la solicitud en el servidor.';
            try {
                const json = await respuesta.json();
                mensaje = json.detail || mensaje;
            } catch (e) {
            }
            lanzarPopupError('Error Interno', mensaje);
            return;
        }

        window.location.href = url;
    } catch (error) {
        console.error('Error de conexión:', error);
        lanzarPopupError('Error de Conexión', 'No se pudo establecer comunicación con el servidor.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-edit[data-id]').forEach(boton => {
        boton.addEventListener('click', async (evento) => {
            evento.preventDefault();
            const idEscuela = evento.currentTarget.getAttribute('data-id');
            await consultarEscuelaPorId(idEscuela);
        });
    });
});

