from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    u = data.get('username')
    p = data.get('password')

    # CTF Credentials
    if u == "admin" and p == "kaithi777":
        return jsonify({
            "status": "SUCCESS",
            "message": "Authentication Successful. Payload injected into console.",
            "hint": "F12 amukki Console-ah check pannunga. ROT13 -> Base64 is the way!"
        }), 200
    
    return jsonify({"status": "FAILED", "message": "Invalid Credentials"}), 401

app = app