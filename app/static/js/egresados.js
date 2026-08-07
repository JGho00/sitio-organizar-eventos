const EGRESADOS_POR_PAGINA = 20;
let paginaActualEgresados = 1;

function filterTable() {
    paginaActualEgresados = 1;
    renderizarTablaEgresados();
}

function obtenerFilasFiltradas() {
    const nombreInput = document.getElementById('searchInput').value.toLowerCase();
    const dniInput = document.getElementById('dniInput').value.toLowerCase();
    const escuelaInput = document.getElementById('escuelaInput').value.toLowerCase();
    const anioInput = document.getElementById('anioInput').value.toLowerCase();
    const tableRows = Array.from(document.querySelectorAll('#egresadosTableBody .table-row'));

    return tableRows.filter(row => {
        const searchData = row.getAttribute('data-search');

        const nombreMatch = searchData.includes(nombreInput) || nombreInput === '';
        const dniMatch = row.querySelector('.cell-dni').textContent.toLowerCase().includes(dniInput) || dniInput === '';
        const escuelaMatch = row.querySelector('.cell-escuela').textContent.toLowerCase().includes(escuelaInput) || escuelaInput === '';
        const anioMatch = row.querySelector('.cell-anio').textContent.toLowerCase().includes(anioInput) || anioInput === '';

        return nombreMatch && dniMatch && escuelaMatch && anioMatch;
    });
}

function renderizarTablaEgresados() {
    const todasLasFilas = Array.from(document.querySelectorAll('#egresadosTableBody .table-row'));
    const filasFiltradas = obtenerFilasFiltradas();

    const totalPaginas = Math.max(1, Math.ceil(filasFiltradas.length / EGRESADOS_POR_PAGINA));
    if (paginaActualEgresados > totalPaginas) paginaActualEgresados = totalPaginas;

    const inicio = (paginaActualEgresados - 1) * EGRESADOS_POR_PAGINA;
    const fin = inicio + EGRESADOS_POR_PAGINA;
    const filasVisibles = new Set(filasFiltradas.slice(inicio, fin));

    todasLasFilas.forEach(row => {
        row.style.display = filasVisibles.has(row) ? '' : 'none';
    });

    renderizarPaginacion(totalPaginas, filasFiltradas.length);
}

function renderizarPaginacion(totalPaginas, totalRegistros) {
    const contenedor = document.getElementById('egresadosPagination');
    if (!contenedor) return;

    if (totalRegistros === 0) {
        contenedor.innerHTML = '';
        return;
    }

    let html = `<span class="pagination-info">Página ${paginaActualEgresados} de ${totalPaginas} (${totalRegistros} egresados)</span>`;
    html += `<button type="button" class="btn-small" ${paginaActualEgresados === 1 ? 'disabled' : ''} onclick="irAPaginaEgresados(${paginaActualEgresados - 1})">‹ Anterior</button>`;

    for (let pagina = 1; pagina <= totalPaginas; pagina++) {
        html += `<button type="button" class="btn-small ${pagina === paginaActualEgresados ? 'btn-primary' : ''}" onclick="irAPaginaEgresados(${pagina})">${pagina}</button>`;
    }

    html += `<button type="button" class="btn-small" ${paginaActualEgresados === totalPaginas ? 'disabled' : ''} onclick="irAPaginaEgresados(${paginaActualEgresados + 1})">Siguiente ›</button>`;

    contenedor.innerHTML = html;
}

function irAPaginaEgresados(pagina) {
    paginaActualEgresados = pagina;
    renderizarTablaEgresados();
}

document.addEventListener('DOMContentLoaded', renderizarTablaEgresados);

function openAddModal() {
    document.getElementById('modalTitle').textContent = 'Agregar Nuevo Egresado';
    document.getElementById('egresadoForm').reset();
    document.getElementById('egresadoModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('egresadoModal').style.display = 'none';
}


function deleteEgresado(id) {
    if (confirm('¿Está seguro de que desea eliminar este egresado?')) {
        //alert('Función de eliminación en desarrollo: Egresado ID ' + id);
        // TODO: Implementar eliminación de egresado
    }
}

// Cerrar modal al hacer clic fuera de él
window.onclick = function(event) {
    const modal = document.getElementById('egresadoModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Enviar formulario
document.getElementById('egresadoForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Formulario en desarrollo');
    // TODO: Enviar datos al servidor
});
