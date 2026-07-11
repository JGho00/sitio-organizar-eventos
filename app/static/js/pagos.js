// static/js/cuotas.js

// 1. Capturar clics en los botones de la tabla para ABRIR el formulario
const botones = document.querySelectorAll('.btn_registrar_pago_cuota');

botones.forEach(boton => {
    boton.addEventListener('click', async (evento) => {
        const idCuota = evento.currentTarget.getAttribute('data-idcuota');
        console.log("ID capturado para abrir formulario:", idCuota); 
        await abrirFormularioPago(idCuota);
    });
});

// 2. Función para obtener el HTML de la API e inyectarlo en el modal
async function abrirFormularioPago(idcuota) {
    try {
        // Hacemos un GET a tu API pidiendo la plantilla HTML del formulario
        const respuesta = await fetch(`/pagos/cuotas/${idcuota}/formulario-pago`);
        
        if (!respuesta.ok) {
            throw new Error(`Error en el servidor: ${respuesta.status}`);
        }

        // Leemos la respuesta como texto plano (HTML) en lugar de JSON
        const htmlFormulario = await respuesta.text();
        
        const modal = document.getElementById("modal-base");
        if (modal) {
            modal.innerHTML = htmlFormulario; // Inyectamos el HTML recibido
            modal.classList.add("mostrar");    // Mostramos la ventana flotante en el centro
            
            // Una vez inyectado el formulario, configuramos el evento para cuando se envíe
            configurarEnvioPago(idcuota);
        }
    } catch (error) {
        console.error("Error al obtener el formulario:", error);
        alert("No se pudo cargar el formulario de pago.");
    }
}

// 3. Función para capturar el envío (SUBMIT) del formulario inyectado
function configurarEnvioPago(idcuota) {
    const formulario = document.querySelector("#modal-base form");
    if (!formulario) return;

    formulario.addEventListener("submit", async (evento) => {
        evento.preventDefault(); // Evitamos que la página se recargue completamente

        // Capturamos el input de la cantidad a pagar
        const inputMonto = document.getElementById("monto_pagar");
        const monto = inputMonto ? inputMonto.value : 0;

        try {
            // Creamos un FormData para simular el envío de un formulario tradicional que entienda FastAPI Form(...)
            const datosFormulario = new FormData();
            datosFormulario.append("monto_pagar", monto);

            // Hacemos el POST real para procesar el pago en la base de datos
            const respuesta = await fetch(`/pagos/registrar-pago/${idcuota}`, {
                method: 'POST',
                body: datosFormulario // Enviamos el monto encapsulado
            });

            const divResultado = document.getElementById("mensaje-resultado");

            if (respuesta.ok) {
                const datos = await respuesta.json();
                console.log("Respuesta exitosa de la API:", datos);
                
                if (divResultado) {
                    divResultado.innerHTML = `<p style="color: green;">¡Pago de $${monto} registrado con éxito!</p>`;
                }
                
                // Esperamos 3 segundos y cerramos la ventana flotante de forma automática
                setTimeout(cerrarModal, 3000);

                //Redireccionar
                const dniEgresado = datos.dni
                window.location.href = `/egresados/dni/${dniEgresado}`;
            } else {
                // Si la API arroja un error controlado
                const textoError = await respuesta.text();
                if (divResultado) {
                    divResultado.innerHTML = `<p style="color: red;">Error: ${textoError}</p>`;
                }
            }
        } catch (error) {
            console.error("Error al procesar el pago:", error);
        }
    });
}

// 4. Función global para cerrar el modal de forma limpia
function cerrarModal() {
    const modal = document.getElementById("modal-base");
    if (modal) {
        modal.classList.remove("mostrar");
        modal.innerHTML = ""; // Vaciamos para liberar memoria
    }
}

// Cerrar si el usuario hace clic en el fondo oscuro exterior
document.addEventListener("click", function(evento) {
    const modal = document.getElementById("modal-base");
    if (evento.target === modal) {
        cerrarModal();
    }
});