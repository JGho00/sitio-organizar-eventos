const LOGS_POR_PAGINA = 20;
let paginaActualLogs = 1;

function filterTable() {
    paginaActualLogs = 1;
    renderizarTablaLogs();
}

function obtenerFilasFiltradas() {
    const fechaInput = document.getElementById('searchDateInput').value;
    const accionInput = document.getElementById('searchAccionInput').value.toLowerCase();
    const tableRows = Array.from(document.querySelectorAll('#logsTableBody .table-row'));

    return tableRows.filter(row => {
        const fecha = row.getAttribute('data-fecha') || '';
        const accion = row.getAttribute('data-accion') || '';

        const fechaMatch = fecha === fechaInput || fechaInput === '';
        const accionMatch = accion.includes(accionInput) || accionInput === '';

        return fechaMatch && accionMatch;
    });
}

function renderizarTablaLogs() {
    const todasLasFilas = Array.from(document.querySelectorAll('#logsTableBody .table-row'));
    const filasFiltradas = obtenerFilasFiltradas();

    const totalPaginas = Math.max(1, Math.ceil(filasFiltradas.length / LOGS_POR_PAGINA));
    if (paginaActualLogs > totalPaginas) paginaActualLogs = totalPaginas;

    const inicio = (paginaActualLogs - 1) * LOGS_POR_PAGINA;
    const fin = inicio + LOGS_POR_PAGINA;
    const filasVisibles = new Set(filasFiltradas.slice(inicio, fin));

    todasLasFilas.forEach(row => {
        row.style.display = filasVisibles.has(row) ? '' : 'none';
    });

    renderizarPaginacionLogs(totalPaginas, filasFiltradas.length);
}

function renderizarPaginacionLogs(totalPaginas, totalRegistros) {
    const contenedor = document.getElementById('logsPagination');
    if (!contenedor) return;

    if (totalRegistros === 0) {
        contenedor.innerHTML = '';
        return;
    }

    let html = `<span class="pagination-info">Página ${paginaActualLogs} de ${totalPaginas} (${totalRegistros} registros)</span>`;
    html += `<button type="button" class="btn-small" ${paginaActualLogs === 1 ? 'disabled' : ''} onclick="irAPaginaLogs(${paginaActualLogs - 1})">‹ Anterior</button>`;

    for (let pagina = 1; pagina <= totalPaginas; pagina++) {
        html += `<button type="button" class="btn-small ${pagina === paginaActualLogs ? 'btn-primary' : ''}" onclick="irAPaginaLogs(${pagina})">${pagina}</button>`;
    }

    html += `<button type="button" class="btn-small" ${paginaActualLogs === totalPaginas ? 'disabled' : ''} onclick="irAPaginaLogs(${paginaActualLogs + 1})">Siguiente ›</button>`;

    contenedor.innerHTML = html;
}

function irAPaginaLogs(pagina) {
    paginaActualLogs = pagina;
    renderizarTablaLogs();
}

document.addEventListener('DOMContentLoaded', renderizarTablaLogs);
