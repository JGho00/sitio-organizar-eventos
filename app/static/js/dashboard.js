// ===== DASHBOARD NAVIGATION =====
document.addEventListener('DOMContentLoaded', function() {
    // Manejo de enlaces del menú
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Remover la clase active de todos los links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Agregar clase active al link clickeado
            this.classList.add('active');
        });
    });

    // Inicializar el primer link como activo
    if (navLinks.length > 0) {
        navLinks[0].classList.add('active');
    }

    // Manejo de cerrar sesión
    const logoutLink = document.querySelector('.nav-link.logout');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('¿Está seguro de que desea cerrar sesión?')) {
                window.location.href = '/login/logout';
            }
        });
    }

    // Manejo de los enlaces "Ver más" en las tarjetas
    const cardLinks = document.querySelectorAll('.card-link');
    cardLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            // Aquí se puede agregar la lógica para navegar a páginas específicas
            console.log('Ver más:', this);
        });
    });
});

// ===== FUNCIONES AUXILIARES =====

/**
 * Formato de moneda
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

/**
 * Formato de fecha
 */
function formatDate(date) {
    return new Intl.DateTimeFormat('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }).format(new Date(date));
}

/**
 * Mostrar notificación
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}
