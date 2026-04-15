from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# Database Connection (Supabase/Postgres URI vainga)
# Local-la test panna: 'sqlite:///kaithi.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///kaithi.db")
app.config['JWT_SECRET_KEY'] = 'kaithi-network-secret-777'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Increased size for hash

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Identity already exists"}), 400

    # PASSWORD ENCRYPTION (HASHING)
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_pw)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Identity Encrypted & Saved!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.email)
        return jsonify(access_token=token), 200
    
    return jsonify({"msg": "Access Denied"}), 401

# Vercel-ku idhu thaan entry point
app = app