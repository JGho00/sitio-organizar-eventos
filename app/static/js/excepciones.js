let seconds = 11;
const timerDisplay = document.getElementById('timer');
const targetUrl = "{{ url_redireccion }}";
// Actualiza el contador visual cada segundo
const countdownInterval = setInterval(() => {
    seconds--;
    timerDisplay.textContent = seconds;
    if (seconds <= 0) {
        clearInterval(countdownInterval);
        }
    }, 1000);

    // Ejecuta la redirección a los 30 segundos exactos
    setTimeout(() => {
    window.location.href = targetUrl;
    }, 30000);