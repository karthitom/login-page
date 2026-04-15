from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import codecs

app = Flask(__name__)
# Vercel deployment-la cookies work aaga credentials support kandippa venum
CORS(app, supports_credentials=True)

# Double Encoded Blob: [Base64 + ROT13]
# Original: "Ahh Valthukal Valthukal"
# Yaraachum code-ai paartha idhu dhaan theriyum
HIDDEN_FLAG_BLOB = "Quib VZbsgu bxbcl BZbsgu bxbcl="

def rot13(text):
    return codecs.encode(text, 'rot_13')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Challenge Credentials
    if email == "admin@kaithi.net" and password == "pentest123":
        resp = make_response(jsonify({
            "status": "SUCCESS",
            "message": "Access Granted. Hidden data injected into session.",
            "hint": "Analyze your cookies for 'ctf_vault' and decode it twice (ROT13 then Base64)!"
        }))
        
        # Cookie-la encrypted blob-ai set panrom
        resp.set_cookie('ctf_vault', HIDDEN_FLAG_BLOB, httponly=False, samesite='Lax')
        return resp
    
    return jsonify({"status": "FAILED", "message": "Invalid Identity"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)