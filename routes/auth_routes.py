from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import mongo

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data["username"]
    password = generate_password_hash(data["password"])
    role = data["role"]

    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "User exists"}), 400

    mongo.db.users.insert_one({"username": username, "password": password, "role": role})
    return jsonify({"msg": "Registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({"username": data["username"]})
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity={"username": user["username"], "role": user["role"]})
    return jsonify({"token": token}), 200
