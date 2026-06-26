document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.getElementById('formulario-login');
    const cartelError = document.getElementById('cartel-error');

    if (!formulario) return;

    formulario.addEventListener('submit', async (event) => {
        event.preventDefault(); 
        cartelError.style.display = 'none';

        const formData = new URLSearchParams(new FormData(formulario));

        try {
            const respuesta = await fetch('/auth/token', {
                method: 'POST',
                body: formData
            });

            // Si hay un error (Credenciales incorrectas), JS muestra el cartel sin recargar
            if (respuesta.status === 401) {
                const datosError = await respuesta.json();
                cartelError.innerText = datosError.detail;
                cartelError.style.display = 'block';
            } 
            // Si el login es correcto, el navegador ya guardó la cookie por debajo.
            // Solo nos queda mover al usuario de pantalla.
            else if (respuesta.ok) {
                window.location.href = '/dashboard'; 
            }
        } catch (error) {
            cartelError.innerText = "Error de conexión con el servidor.";
            cartelError.style.display = 'block';
        }
    });
});