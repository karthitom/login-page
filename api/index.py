from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import codecs
import os

app = Flask(__name__)
CORS(app)

# Vercel temporary storage fix
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kaithi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

# ROT13 Function
def rot13(text):
    return codecs.encode(text, 'rot_13')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({"msg": "Identity already exists"}), 400

        # ROT13 Obfuscation
        encrypted_pw = rot13(password)
        new_user = User(email=email, password=encrypted_pw)
        
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Identity ROT13 Encrypted!"}), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if user and user.password == rot13(data['password']):
            return jsonify({"msg": "Access Granted"}), 200
        
        return jsonify({"msg": "Access Denied"}), 401
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

# Entry point for Vercel
app = app