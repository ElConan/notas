const iconoCalendario = document.querySelector('.input-container .icon');
    const inputFecha = document.getElementById('fecha');

    iconoCalendario.addEventListener('click', () => {
        inputFecha.showPicker(); // Esto abre el selector de fecha
    });