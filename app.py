from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from recommender import get_recommendations

app = Flask(__name__)
CORS(app)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave segura

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
    data = request.get_json()
    session['selected_brands'] = data.get('brands')
    return jsonify({"success": True})

@app.route("/api/save-budget", methods=["POST"])
def save_budget():
    data = request.get_json()
    session['selected_budget'] = data.get('budget')
    return jsonify({"success": True})

@app.route("/api/save-fuel", methods=["POST"])
def save_fuel():
    data = request.get_json()
    session['selected_fuel'] = data.get('fuel')
    return jsonify({"success": True})

@app.route("/api/save-types", methods=["POST"])
def save_types():
    data = request.get_json()
    session['selected_types'] = data.get('types')
    return jsonify({"success": True})

@app.route("/api/save-transmission", methods=["POST"])
def save_transmission():
    data = request.get_json()
    session['selected_transmission'] = data.get('transmission')
    return jsonify({"success": True})

@app.route("/api/recommendations", methods=["GET"])
def api_recommendations():
    brands = session.get('selected_brands')
    budget = session.get('selected_budget')
    fuel = session.get('selected_fuel')
    types = session.get('selected_types')
    transmission = session.get('selected_transmission')
    
    if not all([brands, budget, fuel, types, transmission]):
        return jsonify({"error": "Faltan datos de selección"}), 400
    
    try:
        result = get_recommendations(brands, budget, fuel, types, transmission)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)