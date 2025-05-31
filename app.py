from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from recommender import get_recommendations

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/brands")
def brands():
    return render_template("brands.html")

@app.route("/budget")
def budget():
    return render_template("budget.html")

@app.route("/fuel")
def fuel():
    return render_template("fuel.html")

@app.route("/transmission")
def transmission():
    return render_template("transmission.html")

@app.route("/type")
def type_page():
    return render_template("type.html")

@app.route("/recommendations")
def recommendations():
    return render_template("recommendations.html")

@app.route("/api/recommendations", methods=["POST"])
def api_recommendations():
    data = request.get_json()
    brand = data.get("brand")
    budget = data.get("budget")
    transmission = data.get("transmission")
    types = data.get("types")
    result = get_recommendations(brand, budget, transmission, types)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)