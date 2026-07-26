// static/js/form_ajax.js
// Intercepta el envío de formularios marcados con data-ajax y los envía por fetch,
// mostrando los errores (422 u otros) en un modal superpuesto en vez de navegar a otra página.

function mostrarModalErrorAjax(mensaje, errores) {
    cerrarModalErrorAjax();

    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    overlay.id = 'ajax-error-overlay';

    const modal = document.createElement('div');
    modal.className = 'error-modal';

    const listaErrores = (errores || []).map(error => `<li>${error}</li>`).join('');

    modal.innerHTML = `
        <button type="button" class="btn-cerrar-esquina" id="ajax-error-cerrar">&times;</button>
        <div class="error-icon">⚠️</div>
        <h2 class="error-title warning">Errores de validación</h2>
        <p class="error-msg">${mensaje}</p>
        ${listaErrores ? `<ul class="error-list">${listaErrores}</ul>` : ''}
    `;

    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    document.getElementById('ajax-error-cerrar').addEventListener('click', cerrarModalErrorAjax);
    overlay.addEventListener('click', (evento) => {
        if (evento.target === overlay) cerrarModalErrorAjax();
    });
}

function cerrarModalErrorAjax() {
    const overlay = document.getElementById('ajax-error-overlay');
    if (overlay) overlay.remove();
}

async function manejarEnvioFormularioAjax(evento) {
    evento.preventDefault();

    const formulario = evento.currentTarget;

    const confirmacion = formulario.getAttribute('data-confirm');
    if (confirmacion && !confirm(confirmacion)) {
        return;
    }

    const datosFormulario = new FormData(formulario);

    try {
        const respuesta = await fetch(formulario.action, {
            method: formulario.method || 'POST',
            body: datosFormulario,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        if (respuesta.ok) {
            const redireccion = formulario.getAttribute('data-redirect');
            window.location.href = redireccion || window.location.pathname;
            return;
        }

        const tipoContenido = respuesta.headers.get('content-type') || '';
        let mensaje = 'Ocurrió un error al procesar la solicitud.';
        let errores = [];

        if (tipoContenido.includes('application/json')) {
            const datos = await respuesta.json();
            mensaje = datos.mensaje || datos.detail || mensaje;
            errores = datos.errores || [];
        } else {
            const texto = await respuesta.text();
            if (texto) mensaje = texto;
        }

        mostrarModalErrorAjax(mensaje, errores);
    } catch (error) {
        console.error('Error al enviar el formulario:', error);
        mostrarModalErrorAjax('No se pudo conectar con el servidor.', []);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form[data-ajax]').forEach((formulario) => {
        formulario.addEventListener('submit', manejarEnvioFormularioAjax);
    });
});
