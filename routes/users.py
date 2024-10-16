from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from config import users, tokens
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt

users_bp = Blueprint('users_bp', __name__)

bcrypt = Bcrypt()

@users_bp.route('/user', methods=['POST'])
def register():
    try:
        data = request.get_json()
        encrypted_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = {
            "email": data["email"],
            "password": encrypted_password,
            "permissao": data["permissao"].upper(),
            "nome": data["nome"].capitalize()
        }
        if users.find_one({"email": data["email"]}):
            return {"error": "Email already registered"}, 400
        users.insert_one(user)
        return {"message": "User registered successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 500

@users_bp.route('/user-permission', methods=['POST'])
@jwt_required()
def getUserPermission():
    try:
        data = request.get_json()
        token = data["token"]
        user_token = tokens.find_one({'token': token})
        if not user_token:
            return jsonify({"permissao": None}), 200
        email = user_token["email"]
        user = users.find_one({"email": email})
        if not user:
            return jsonify({"permissao": None}), 200
        permissao = user["permissao"]
        return jsonify({"permissao": permissao}), 200
    except Exception as e:
        return jsonify({"permissao": None}), 500
