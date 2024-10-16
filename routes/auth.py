from flask_jwt_extended import create_access_token, jwt_required
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from flask import Blueprint, request
from config import users, tokens
from flask_bcrypt import Bcrypt
import datetime

auth_bp = Blueprint('auth_bp', __name__)

bcrypt = Bcrypt()

def remove_expired_tokens():
    now = datetime.datetime.utcnow()
    tokens.delete_many({"expira_em": {"$lt": now}})

scheduler = BackgroundScheduler()
scheduler.add_job(func=remove_expired_tokens, trigger="interval", minutes=60)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = users.find_one({'email': data["email"]})
        if user and bcrypt.check_password_hash(user['password'], data['password']):
            expires = datetime.timedelta(days=10)
            access_token = create_access_token(identity=str(user['_id']), expires_delta=expires)
            expira_em = datetime.datetime.utcnow() + expires
            tokens.insert_one({
                "email": data["email"], 
                "token": access_token, 
                "permissao": user["permissao"], 
                "expira_em": expira_em
            })
            return {"token": access_token}, 200
        else:
            return {"error": "Invalid email or password"}, 401
    except Exception as e:
        return {"error": str(e)}, 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        data = request.get_json()
        token = data['token']
        user = tokens.find_one({"token": token})
        if user:
            tokens.delete_one({"token": token})
            return {"message": "Logout successfully"}, 200
        else:
            return {"error": "Invalid token"}, 401
    except Exception as e:
        return {"error": str(e)}, 500

@auth_bp.route('/verify-token', methods=['POST'])
@jwt_required()
def verifyToken():
    try:
        data = request.get_json()
        token = data["token"]
        user = tokens.find_one({'token': token })
        if user:
            return {"message": "Usuário encontrado"}, 200
        else:
            return {"message": "Usuário não encontrado"}, 404
    except Exception as e:
        return {"mensagem": str(e)}, 500