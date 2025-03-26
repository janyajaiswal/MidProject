from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)
print("✅ auth_routes.py loaded")

@auth_bp.route('/register', methods=['POST'])
def register():
    print("⚡️ /register route hit")
    data = request.get_json()
    username = data["username"]
    password = generate_password_hash(data["password"])
    role = data["role"]

    db = current_app.db
    if db.users.find_one({"username": username}):
        return jsonify({"error": "User exists"}), 400

    db.users.insert_one({"username": username, "password": password, "role": role})
    return jsonify({"msg": "Registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db = current_app.db
    user = db.users.find_one({"username": data["username"]})
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity={"username": user["username"], "role": user["role"]})
    return jsonify({"token": token}), 200
