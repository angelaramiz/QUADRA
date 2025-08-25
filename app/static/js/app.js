// Archivo JavaScript principal para Quadra

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    initializeRatingStars();
    initializeFileUpload();
    initializeGeolocation();
    initializeTooltips();
});

// Sistema de calificación con estrellas
function initializeRatingStars() {
    const ratingContainers = document.querySelectorAll('.rating-input');
    
    ratingContainers.forEach(container => {
        const stars = container.querySelectorAll('.rating-star');
        const input = container.querySelector('input[type="hidden"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const rating = index + 1;
                input.value = rating;
                
                // Actualizar visualización de estrellas
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('text-warning');
                        s.classList.remove('text-muted');
                    } else {
                        s.classList.remove('text-warning');
                        s.classList.add('text-muted');
                    }
                });
            });
            
            star.addEventListener('mouseenter', function() {
                const rating = index + 1;
                
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('text-warning');
                        s.classList.remove('text-muted');
                    } else {
                        s.classList.remove('text-warning');
                        s.classList.add('text-muted');
                    }
                });
            });
        });
        
        container.addEventListener('mouseleave', function() {
            const currentRating = parseInt(input.value) || 0;
            
            stars.forEach((s, i) => {
                if (i < currentRating) {
                    s.classList.add('text-warning');
                    s.classList.remove('text-muted');
                } else {
                    s.classList.remove('text-warning');
                    s.classList.add('text-muted');
                }
            });
        });
    });
}

// Upload de archivos con drag and drop
function initializeFileUpload() {
    const uploadAreas = document.querySelectorAll('.file-upload-area');
    
    uploadAreas.forEach(area => {
        const input = area.querySelector('input[type="file"]');
        
        area.addEventListener('click', () => input.click());
        
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', () => {
            area.classList.remove('dragover');
        });
        
        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                handleFileSelect(files[0], area);
            }
        });
        
        input.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0], area);
            }
        });
    });
}

function handleFileSelect(file, area) {
    const preview = area.querySelector('.file-preview');
    
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            if (preview) {
                preview.innerHTML = `<img src="${e.target.result}" class="img-fluid rounded" style="max-height: 200px;">`;
            }
        };
        reader.readAsDataURL(file);
    }
}

// Geolocalización
function initializeGeolocation() {
    const getLocationBtn = document.getElementById('getLocationBtn');
    const latInput = document.getElementById('latitude');
    const lngInput = document.getElementById('longitude');
    
    if (getLocationBtn && latInput && lngInput) {
        getLocationBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                showSpinner();
                
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        hideSpinner();
                        latInput.value = position.coords.latitude.toFixed(6);
                        lngInput.value = position.coords.longitude.toFixed(6);
                        
                        showAlert('Ubicación obtenida exitosamente', 'success');
                    },
                    function(error) {
                        hideSpinner();
                        let message = 'Error al obtener la ubicación';
                        
                        switch(error.code) {
                            case error.PERMISSION_DENIED:
                                message = 'Permiso de ubicación denegado';
                                break;
                            case error.POSITION_UNAVAILABLE:
                                message = 'Ubicación no disponible';
                                break;
                            case error.TIMEOUT:
                                message = 'Tiempo de espera agotado';
                                break;
                        }
                        
                        showAlert(message, 'danger');
                    }
                );
            } else {
                showAlert('Geolocalización no compatible con este navegador', 'warning');
            }
        });
    }
}

// Tooltips de Bootstrap
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Utilidades
function showSpinner() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-overlay';
    spinner.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Cargando...</span>
        </div>
    `;
    document.body.appendChild(spinner);
}

function hideSpinner() {
    const spinner = document.querySelector('.spinner-overlay');
    if (spinner) {
        spinner.remove();
    }
}

function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertContainer.style.cssText = 'top: 20px; right: 20px; z-index: 10000; min-width: 300px;';
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertContainer);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Función para formatear fechas
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Función para validar formularios
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Event listeners globales
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.classList.contains('needs-validation')) {
        if (!validateForm(form)) {
            e.preventDefault();
            e.stopPropagation();
        }
    }
});

// Smooth scroll para enlaces internos
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});
