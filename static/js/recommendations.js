// Variables globales
let debugMode = false;

// Función para toggle del debug
function toggleDebug() {
  debugMode = !debugMode;
  const debugInfo = document.getElementById('debug-info');
  if (debugInfo) {
    debugInfo.style.display = debugMode ? 'block' : 'none';
  }
}

// Función para formatear precio
function formatPrice(price) {
  if (typeof price === 'number') {
    return `$${price.toLocaleString('es-GT')}`;
  }
  return price || 'Precio no disponible';
}

// Función para crear una tarjeta de auto
function createCarCard(car) {
  const card = document.createElement('div');
  card.className = 'car-card';
  
  const imageHtml = car.image ? 
    `<div class="car-image"><img src="${car.image}" alt="${car.name}"></div>` :
    `<div class="car-image"><div class="no-image">📷 Imagen no disponible</div></div>`;
  
  const featuresHtml = car.features && Array.isArray(car.features) && car.features.length > 0 ? 
    `<div class="car-features">
       <h4>Características:</h4>
       <ul>
         ${car.features.map(feature => `<li>${feature}</li>`).join('')}
       </ul>
     </div>` : '';
  
  card.innerHTML = `
    ${imageHtml}
    <div class="car-name">${car.name || 'Nombre no disponible'}</div>
    <div class="car-brand">${car.brand || 'Marca no disponible'}</div>
    <div class="car-price">${formatPrice(car.price)}</div>
    <div class="car-details">
      <div class="detail"><strong>Tipo:</strong> ${car.type || 'No especificado'}</div>
      <div class="detail"><strong>Combustible:</strong> ${car.fuel || 'No especificado'}</div>
      <div class="detail"><strong>Transmisión:</strong> ${car.transmission || 'No especificado'}</div>
      <div class="detail"><strong>Año:</strong> ${car.year || 'No especificado'}</div>
    </div>
    ${featuresHtml}
  `;
  
  return card;
}

// Función para mostrar las recomendaciones
function displayRecommendations(recommendations) {
  const container = document.getElementById('recommendations-container');
  
  if (!Array.isArray(recommendations) || recommendations.length === 0) {
    container.innerHTML = `
      <div class="no-recommendations">
        <h3>No se encontraron recomendaciones</h3>
        <p>Lo sentimos, no pudimos encontrar autos que coincidan con tus preferencias.</p>
        <p>Intenta modificar tus criterios de búsqueda.</p>
      </div>
    `;
    return;
  }
  
  const grid = document.createElement('div');
  grid.className = 'recommendations-grid';
  
  recommendations.forEach(car => {
    const card = createCarCard(car);
    grid.appendChild(card);
  });
  
  container.innerHTML = '';
  container.appendChild(grid);
}

// Función para mostrar errores
function showError(errorMessage, details = null) {
  const errorContainer = document.getElementById('error-container');
  const loadingElement = document.getElementById('loading');
  
  if (loadingElement) {
    loadingElement.style.display = 'none';
  }
  
  let errorHtml = `
    <div class="error-message">
      <h3>❌ Error al cargar las recomendaciones</h3>
      <p><strong>Mensaje:</strong> ${errorMessage}</p>
  `;
  
  if (details) {
    errorHtml += `
      <p><strong>Detalles:</strong></p>
      <ul>
        <li>Verifica que hayas completado todos los pasos anteriores</li>
        <li>Intenta recargar la página</li>
        <li>Si el problema persiste, reinicia el proceso</li>
      </ul>
    `;
    
    if (details.session_data) {
      errorHtml += `
        <p><strong>Estado de la sesión:</strong></p>
        <ul>
          <li>Marcas: ${details.session_data.selected_brands ? '✓' : '❌'}</li>
          <li>Presupuesto: ${details.session_data.selected_budget ? '✓' : '❌'}</li>
          <li>Combustible: ${details.session_data.selected_fuel ? '✓' : '❌'}</li>
          <li>Tipo: ${details.session_data.selected_types ? '✓' : '❌'}</li>
          <li>Transmisión: ${details.session_data.selected_transmission ? '✓' : '❌'}</li>
        </ul>
      `;
    }
  }
  
  errorHtml += `</div>`;
  
  errorContainer.innerHTML = errorHtml;
  errorContainer.style.display = 'block';
}

// Función para verificar el estado de la sesión
async function checkSessionStatus() {
  try {
    const response = await fetch('/api/debug/session');
    const data = await response.json();
    
    if (debugMode) {
      const sessionStatus = document.getElementById('session-status');
      if (sessionStatus) {
        const hasAllData = data.session_data.selected_brands && 
                          data.session_data.selected_budget && 
                          data.session_data.selected_fuel && 
                          data.session_data.selected_types && 
                          data.session_data.selected_transmission;
        
        sessionStatus.textContent = hasAllData ? '✓ Completa' : '⚠️ Incompleta';
        
        // Log de debug
        console.log('Estado de la sesión:', data.session_data);
        console.log('Recommender disponible:', data.recommender_available);
      }
    }
    
    return data;
  } catch (error) {
    console.error('Error verificando sesión:', error);
    if (debugMode) {
      const sessionStatus = document.getElementById('session-status');
      if (sessionStatus) {
        sessionStatus.textContent = '❌ Error';
      }
    }
    return null;
  }
}

// Función para cargar las recomendaciones
async function loadRecommendations() {
  const loadingElement = document.getElementById('loading');
  const recommendationsContainer = document.getElementById('recommendations-container');
  const errorContainer = document.getElementById('error-container');
  const actionButtons = document.getElementById('action-buttons');
  
  try {
    // Mostrar loading y ocultar otros elementos
    if (loadingElement) loadingElement.style.display = 'block';
    if (recommendationsContainer) recommendationsContainer.style.display = 'none';
    if (errorContainer) errorContainer.style.display = 'none';
    if (actionButtons) actionButtons.style.display = 'none';

    // Verificar estado de la sesión
    await checkSessionStatus();

    // Obtener recomendaciones del servidor
    console.log('Intentando conectar con /api/recommendations...');
    const apiStatus = document.getElementById('api-status');
    if (apiStatus) {
      apiStatus.textContent = '⏳ Conectando...';
    }
    
    const response = await fetch('/api/recommendations');
    
    console.log('Respuesta recibida:', response.status, response.statusText);
    
    if (!response.ok) {
      if (apiStatus) {
        apiStatus.textContent = `❌ Error ${response.status}`;
      }
      
      // Intentar obtener el mensaje de error del servidor
      let errorMessage = `Error ${response.status}: ${response.statusText}`;
      let errorDetails = null;
      
      try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorMessage;
        errorDetails = errorData;
        
        // Si hay detalles de sesión, mostrarlos
        if (errorData.session_data) {
          console.log('Datos de sesión del servidor:', errorData.session_data);
        }
      } catch (e) {
        console.log('No se pudo parsear el error JSON');
      }
      
      showError(errorMessage, errorDetails);
      return;
    }
    
    const recommendations = await response.json();
    console.log('Recomendaciones recibidas:', recommendations);
    
    if (apiStatus) {
      apiStatus.textContent = '✓ Conectado';
    }
    
    // Ocultar loading y mostrar recomendaciones
    if (loadingElement) loadingElement.style.display = 'none';
    if (recommendationsContainer) recommendationsContainer.style.display = 'block';
    if (actionButtons) actionButtons.style.display = 'flex';
    
    // Verificar que las recomendaciones sean válidas
    if (!Array.isArray(recommendations)) {
      console.error('Las recomendaciones no son un array:', recommendations);
      showError('Formato de datos inválido recibido del servidor');
      return;
    }
    
    // Mostrar las recomendaciones
    displayRecommendations(recommendations);
    
  } catch (error) {
    console.error('Error cargando recomendaciones:', error);
    
    const apiStatus = document.getElementById('api-status');
    if (apiStatus) {
      apiStatus.textContent = '❌ Error de conexión';
    }
    
    showError(`Error de conexión: ${error.message}`, {
      suggestion: 'Verifica que el servidor esté funcionando correctamente'
    });
    
    // Mostrar botones de acción para que el usuario pueda reintentar
    if (actionButtons) actionButtons.style.display = 'flex';
  }
}

// Función para reiniciar el proceso
function restartProcess() {
  if (confirm('¿Estás seguro de que quieres reiniciar el proceso? Se perderán todas tus selecciones.')) {
    window.location.href = '/brands';
  }
}

// Función principal que se ejecuta cuando carga la página
document.addEventListener('DOMContentLoaded', async () => {
  // Marcar JavaScript como cargado
  const jsStatus = document.getElementById('js-status');
  if (jsStatus) {
    jsStatus.textContent = '✓ Cargado';
  }

  // Cargar las recomendaciones automáticamente
  await loadRecommendations();
});

// Hacer las funciones disponibles globalmente para los botones
window.toggleDebug = toggleDebug;
window.loadRecommendations = loadRecommendations;
window.restartProcess = restartProcess;