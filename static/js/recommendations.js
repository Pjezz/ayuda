document.addEventListener('DOMContentLoaded', async () => {
  const loadingElement = document.getElementById('loading');
  const recommendationsContainer = document.getElementById('recommendations-container');
  const errorContainer = document.getElementById('error-container');

  try {
    // Mostrar loading
    if (loadingElement) {
      loadingElement.style.display = 'block';
    }

    // Obtener recomendaciones del servidor
    const response = await fetch('/api/recommendations');
    
    if (!response.ok) {
      throw new Error('Error al obtener recomendaciones');
    }
    
    const recommendations = await response.json();
    
    // Ocultar loading
    if (loadingElement) {
      loadingElement.style.display = 'none';
    }
    
    // Mostrar recomendaciones
    displayRecommendations(recommendations);
    
  } catch (error) {
    console.error('Error:', error);
    
    // Ocultar loading
    if (loadingElement) {
      loadingElement.style.display = 'none';
    }
    
    // Mostrar error
    if (errorContainer) {
      errorContainer.style.display = 'block';
      errorContainer.innerHTML = `
        <div class="error-message">
          <h3>Error al cargar recomendaciones</h3>
          <p>${error.message}</p>
          <button onclick="window.location.reload()" class="retry-btn">
            Intentar de nuevo
          </button>
        </div>
      `;
    }
  }
});

function displayRecommendations(recommendations) {
  const container = document.getElementById('recommendations-container');
  
  if (!container || !recommendations || recommendations.length === 0) {
    container.innerHTML = `
      <div class="no-recommendations">
        <h3>No se encontraron recomendaciones</h3>
        <p>Intenta ajustar tus criterios de búsqueda.</p>
        <button onclick="window.location.href='/brands'" class="restart-btn">
          Empezar de nuevo
        </button>
      </div>
    `;
    return;
  }

  let html = '<div class="recommendations-grid">';
  
  recommendations.forEach(car => {
    html += `
      <div class="car-card">
        <div class="car-image">
          ${car.image ? `<img src="${car.image}" alt="${car.name}">` : '<div class="no-image">Sin imagen</div>'}
        </div>
        <div class="car-info">
          <h3 class="car-name">${car.name}</h3>
          <p class="car-brand">${car.brand}</p>
          <p class="car-price">$${car.price?.toLocaleString() || 'Precio no disponible'}</p>
          <div class="car-details">
            <span class="detail"><strong>Tipo:</strong> ${car.type}</span>
            <span class="detail"><strong>Combustible:</strong> ${car.fuel}</span>
            <span class="detail"><strong>Transmisión:</strong> ${car.transmission}</span>
          </div>
          ${car.features ? `
            <div class="car-features">
              <h4>Características:</h4>
              <ul>
                ${car.features.map(feature => `<li>${feature}</li>`).join('')}
              </ul>
            </div>
          ` : ''}
        </div>
      </div>
    `;
  });
  
  html += '</div>';
  
  // Agregar botones de acción
  html += `
    <div class="action-buttons">
      <button onclick="window.location.href='/brands'" class="restart-btn">
        Empezar de nuevo
      </button>
      <button onclick="window.print()" class="print-btn">
        Imprimir recomendaciones
      </button>
    </div>
  `;
  
  container.innerHTML = html;
}