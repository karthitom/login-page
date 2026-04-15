from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    return jsonify({"status": "SUCCESS", "payload": "Quib VZbsgu bxbcl BZbsgu bxbcl="})

# Vercel entry point
app = app