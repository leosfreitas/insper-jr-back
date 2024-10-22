from flask import Blueprint, request
from config import users, tokens, avisos
from flask_jwt_extended import jwt_required

avisos_bp = Blueprint('avisos_bp', __name__)

@avisos_bp.route('/aviso', methods=['GET'])
@jwt_required()
def get_avisos():
    lista_avisos = []
    for aviso in avisos.find():
        aviso['_id'] = str(aviso['_id'])
        lista_avisos.append(aviso)
    return {'avisos': lista_avisos}, 200


@avisos_bp.route('/aviso', methods=['POST'])
@jwt_required()
def post_avisos():
    token = request.headers.get('Authorization')[7:]
    user = tokens.find_one({'token': token})
    email = user['email']
    user1 = users.find_one({'email': email})
    permission = user1['permissao']
    if permission == 'GESTAO':
        data = request.get_json()
        avisos.insert_one({
            'titulo': data['titulo'],
            'mensagem': data['mensagem'],
            'autor': email
        })
        return {'message': 'Aviso criado com sucesso'}, 200
    else:
        return {'error': 'Não é possível fazer a requisição'}, 401

