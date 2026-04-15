from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        u = data.get('username')
        p = data.get('password')

        if u == "admin" and p == "kaithi777":
            return jsonify({
                "status": "SUCCESS",
                "message": "Auth OK. Payload injected.",
                "hint": "Check F12 Console. ROT13 -> Base64 is the key!"
            }), 200
        
        return jsonify({"status": "FAILED", "message": "Invalid Key"}), 401
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

# VERY IMPORTANT: app.run() use panna koodathu
app = app