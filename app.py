from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import traceback

# Importar el sistema de recomendaciones
try:
    from recommender import get_recommendations
    RECOMMENDER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: No se pudo importar recommender.py: {e}")
    RECOMMENDER_AVAILABLE = False

app = Flask(__name__)
CORS(app)
app.secret_key = 'tu_clave_secreta_aqui_cambiala_por_una_segura'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        # Aquí puedes agregar validación real de usuario/contraseña
        if username and password:
            session['logged_in'] = True
            session['username'] = username
            return jsonify({"success": True, "redirect": url_for("brands")})
        else:
            return jsonify({"success": False, "message": "Credenciales inválidas"})
    
    return render_template("login.html")

@app.route("/brands")
def brands():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("brands.html")

@app.route("/budget")
def budget():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if not session.get('selected_brands'):
        return redirect(url_for('brands'))
    return render_template("budget.html")

@app.route("/fuel")
def fuel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if not session.get('selected_budget'):
        return redirect(url_for('budget'))
    return render_template("fuel.html")

@app.route("/type")
def type_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if not session.get('selected_fuel'):
        return redirect(url_for('fuel'))
    return render_template("type.html")

@app.route("/transmission")
def transmission():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if not session.get('selected_types'):
        return redirect(url_for('type_page'))
    return render_template("transmission.html")

@app.route("/recommendations")
def recommendations():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if not session.get('selected_transmission'):
        return redirect(url_for('transmission'))
    return render_template("recommendations.html")

# API Endpoints para guardar selecciones
@app.route("/api/save-brands", methods=["POST"])
def save_brands():
    try:
        data = request.get_json()
        session['selected_brands'] = data.get('brands')
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/save-budget", methods=["POST"])
def save_budget():
    try:
        data = request.get_json()
        session['selected_budget'] = data.get('budget')
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/save-fuel", methods=["POST"])
def save_fuel():
    try:
        data = request.get_json()
        session['selected_fuel'] = data.get('fuel')
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/save-types", methods=["POST"])
def save_types():
    try:
        data = request.get_json()
        session['selected_types'] = data.get('types')
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/save-transmission", methods=["POST"])
def save_transmission():
    try:
        data = request.get_json()
        session['selected_transmission'] = data.get('transmission')
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/recommendations", methods=["GET"])
def api_recommendations():
    try:
        # Obtener datos de la sesión
        brands = session.get('selected_brands')
        budget = session.get('selected_budget')
        fuel = session.get('selected_fuel')
        types = session.get('selected_types')
        transmission = session.get('selected_transmission')
        
        # Debug: imprimir datos de sesión
        print("=== DEBUG: Datos de sesión ===")
        print(f"Brands: {brands}")
        print(f"Budget: {budget}")
        print(f"Fuel: {fuel}")
        print(f"Types: {types}")
        print(f"Transmission: {transmission}")
        print("============================")
        
        # Verificar que todos los datos estén presentes
        if not all([brands, budget, fuel, types, transmission]):
            missing_data = []
            if not brands: missing_data.append("brands")
            if not budget: missing_data.append("budget")
            if not fuel: missing_data.append("fuel")
            if not types: missing_data.append("types")
            if not transmission: missing_data.append("transmission")
            
            return jsonify({
                "error": f"Faltan datos de selección: {', '.join(missing_data)}",
                "session_data": {
                    "brands": brands,
                    "budget": budget,
                    "fuel": fuel,
                    "types": types,
                    "transmission": transmission
                }
            }), 400
        
        # Si el sistema de recomendaciones no está disponible, usar datos de ejemplo
        if not RECOMMENDER_AVAILABLE:
            print("Warning: Usando datos de ejemplo porque recommender.py no está disponible")
            sample_recommendations = [
                {
                    "name": "Toyota Corolla 2024",
                    "brand": "Toyota" if "Toyota" in brands else brands[0] if brands else "Toyota",
                    "price": 25000,
                    "type": types[0] if types else "Sedán",
                    "fuel": fuel[0] if isinstance(fuel, list) else fuel,
                    "transmission": transmission[0] if isinstance(transmission, list) else transmission,
                    "features": ["Aire acondicionado", "Sistema de sonido", "Cámara trasera", "Control crucero"],
                    "image": None
                },
                {
                    "name": "Honda Civic 2024",
                    "brand": "Honda" if "Honda" in brands else brands[0] if brands else "Honda",
                    "price": 28000,
                    "type": types[0] if types else "Sedán",
                    "fuel": fuel[0] if isinstance(fuel, list) else fuel,
                    "transmission": transmission[0] if isinstance(transmission, list) else transmission,
                    "features": ["Pantalla táctil", "Sensores de estacionamiento", "Sistema de navegación", "Asientos de cuero"],
                    "image": None
                },
                {
                    "name": "Nissan Sentra 2024",
                    "brand": "Nissan" if "Nissan" in brands else brands[0] if brands else "Nissan",
                    "price": 23000,
                    "type": types[0] if types else "Sedán",
                    "fuel": fuel[0] if isinstance(fuel, list) else fuel,
                    "transmission": transmission[0] if isinstance(transmission, list) else transmission,
                    "features": ["Bluetooth", "Control de estabilidad", "Frenos ABS", "Airbags múltiples"],
                    "image": None
                }
            ]
            return jsonify(sample_recommendations)
        
        # Usar el sistema de recomendaciones real
        result = get_recommendations(brands, budget, fuel, types, transmission)
        
        # Asegurar que el resultado sea una lista
        if not isinstance(result, list):
            print(f"Warning: get_recommendations devolvió {type(result)}, esperaba lista")
            return jsonify([])
        
        return jsonify(result)
        
    except Exception as e:
        # Log completo del error
        error_traceback = traceback.format_exc()
        print(f"Error en api_recommendations: {error_traceback}")
        
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}",
            "details": "Revisa la consola del servidor para más información"
        }), 500

# Endpoint adicional para debug
@app.route("/api/debug/session", methods=["GET"])
def debug_session():
    return jsonify({
        "session_data": dict(session),
        "recommender_available": RECOMMENDER_AVAILABLE
    })

# Endpoint para limpiar la sesión (útil para testing)
@app.route("/api/debug/clear-session", methods=["POST"])
def clear_session():
    session.clear()
    return jsonify({"success": True, "message": "Sesión limpiada"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# Manejador de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == "__main__":
    print("=== Iniciando aplicación Flask ===")
    print(f"Recommender disponible: {RECOMMENDER_AVAILABLE}")
    print("Endpoints disponibles:")
    print("  GET  / -> index")
    print("  GET  /brands -> selección de marcas")
    print("  GET  /budget -> selección de presupuesto")
    print("  GET  /fuel -> selección de combustible")
    print("  GET  /type -> selección de tipo")
    print("  GET  /transmission -> selección de transmisión")
    print("  GET  /recommendations -> página de recomendaciones")
    print("  GET  /api/recommendations -> obtener recomendaciones JSON")
    print("  GET  /api/debug/session -> ver datos de sesión")
    print("================================")
    app.run(debug=True)