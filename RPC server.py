from flask import Flask, request, jsonify
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
CORS(app)

# Helper to extract x and y from request (works with JSON, form-data, or query string)
def get_params():
    data = {}

    # Try JSON first
    if request.is_json:
        data = request.get_json(silent=True) or {}

    # If JSON is not present, try form data
    elif request.form:
        data = request.form.to_dict()

    # If raw body sent as text, try parsing manually
    elif request.data:
        try:
            import json
            data = json.loads(request.data.decode("utf-8"))
        except Exception:
            pass

    # Finally, check query params (?x=5&y=10)
    if not data:
        data = request.args.to_dict()

    # Extract numbers
    x = data.get("x")
    y = data.get("y")

    # Convert to int/float if possible
    try:
        if x is not None: 
            x = float(x)
        if y is not None: 
            y = float(y)
    except ValueError:
        return None, None

    return x, y

# Homepage route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the RPC server!",
        "endpoints": {
            "add": "POST /add",
            "multiply": "POST /multiply",
            
        }
    })

# Add endpoint
@app.route("/add", methods=["POST"])
def add():
    x, y = get_params()
    if x is None or y is None:
        return jsonify({"error": "Missing or invalid x or y"}), 400
    return jsonify({"result": x + y})

# Multiply endpoint
@app.route("/multiply", methods=["POST"])
def multiply():
    x, y = get_params()
    if x is None or y is None:
        return jsonify({"error": "Missing or invalid x or y"}), 400
    return jsonify({"result": x * y})

# Health check endpoint
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "Server is running!"})

# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
