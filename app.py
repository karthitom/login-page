from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kaithi.db'
app.config['JWT_SECRET_KEY'] = 'kaithi-network-private-key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Security Logger Function
def log_security_event(email, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_addr = request.remote_addr
    with open("security_logs.txt", "a") as f:
        f.write(f"[{timestamp}] IP: {ip_addr} | USER: {email} | STATUS: {status}\n")

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Identity already exists in database"}), 400
    
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    log_security_event(data['email'], "REGISTERED_SUCCESS")
    return jsonify({"msg": "Identity Created"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.email)
        log_security_event(data['email'], "LOGIN_SUCCESS")
        return jsonify(access_token=token), 200
    
    # Failed Attempt Log Pandrom
    log_security_event(data.get('email', 'UNKNOWN'), "FAILED_ATTEMPT_ALERT")
    return jsonify({"msg": "Access Denied: Invalid Credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)