async function registrar_pago(idcuota) {
    try {
        alert(idcuota)
        const respuesta = await fetch(`/pagos/registrar-pago/${idcuota}`, {
            method: 'POST'
        });
        
        const datos = await respuesta.json();
        console.log("Respuesta de la API:", datos);
        alert("Pago registrado con éxito");

    } catch (error) {
        console.error("Error al registrar el pago:", error);
    }
}

const botones = document.querySelectorAll('.btn_registrar_pago_cuota');

// Recorremos cada botón encontrado en la tabla y le agregamos el "escuchador"
botones.forEach(boton => {
    boton.addEventListener('click', (evento) => {
        // Obtenemos el ID de la cuota específico de ESTE botón
        const idCuota = evento.currentTarget.getAttribute('data-idcuota')
        console.log("ID capturado en JS:", idCuota); 
        // Ejecutamos la función pasando el ID correcto
        registrar_pago(idCuota);
    });
});