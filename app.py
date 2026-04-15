from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import codecs

app = Flask(__name__)
CORS(app)

# Double Encoded: [Base64 + ROT13]
# Original: "Ahh Valthukal Valthukal"
# Code-la idhu mattum thaan irukkum
HIDDEN_FLAG = "Quib VZbsgu bxbcl BZbsgu bxbcl="

def rot13(text):
    return codecs.encode(text, 'rot_13')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Target Credentials
        if email == "admin@kaithi.net" and password == "pentest123":
            resp = make_response(jsonify({
                "status": "SUCCESS",
                "message": "Vault Unlocked.",
                "hint": "Flag hidden in Response Headers (X-Secret-Flag). Decode it twice!"
            }))
            
            # HEADER-LA FLAG-AI INJECT PANROM
            resp.headers['X-Secret-Flag'] = HIDDEN_FLAG
            # CORS issue varaama irukka indha line mukkiyam
            resp.headers['Access-Control-Expose-Headers'] = 'X-Secret-Flag'
            return resp
        
        return jsonify({"status": "FAILED", "message": "Invalid Key"}), 401
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

# Entry point for Vercel
app = app