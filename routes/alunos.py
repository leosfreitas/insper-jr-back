from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify
from config import alunos, tokens, users

alunos_bp = Blueprint('alunos_bp', __name__)

@alunos_bp.route('/aluno', methods=['GET'])
@jwt_required()
def getAlunos():
    try:
        token = request.headers.get('Authorization')[7:]
        user = tokens.find_one({'token': token})
        email = user['email']
        user1 = users.find_one({'email': email})
        permission = user1['permissao']
        if permission != "GESTAO":
            return {"error": "Permissão negada"}, 401
        lista_alunos = []
        for aluno in alunos.find():
            aluno['_id'] = str(aluno['_id'])
            lista_alunos.append(aluno)
        return {"alunos": lista_alunos}, 200
    except Exception as e:
        return {"error": str(e)}, 500

@alunos_bp.route('/aluno/<cpf>', methods=['GET'])
def getAluno(cpf):
    try:
        token = request.headers.get('Authorization')[7:]
        user = tokens.find_one({'token': token})
        email = user['email']
        user1 = users.find_one({'email': email})
        permission = user1['permissao']
        
        if permission != "GESTAO":
            return {"error": "Permissão negada"}, 401
        
        aluno = alunos.find_one({'cpf': cpf})
        
        if aluno is None:
            return {"error": "Aluno não encontrado"}, 404
        
        aluno['_id'] = str(aluno['_id']) 
        
        return jsonify(aluno), 200  
    except Exception as e:
        return {"error": str(e)}, 500


        