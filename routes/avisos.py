from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from schemas.avisos import AvisoCreate
from database import avisos_collection, user_collection
from utils.token import verify_token
from bson import ObjectId

router = APIRouter()

@router.post("/create")
async def post_avisos(aviso: AvisoCreate, user: dict = Depends(verify_token)):
    """
    Cria um novo aviso.

    Esta função é responsável por inserir um novo aviso na coleção de avisos do banco de dados.
    Apenas usuários com permissões de 'GESTAO' ou 'PROFESSOR' podem criar avisos.

    Parâmetros:
    - aviso: Um objeto do tipo AvisoCreate que contém os detalhes do aviso a ser criado.
    - user: Um dicionário que representa o usuário autenticado, obtido através da verificação do token.

    Retorna:
    - JSONResponse: Uma resposta JSON com uma mensagem de sucesso ou erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO' or permission == 'PROFESSOR':
            await avisos_collection.insert_one({
                'titulo': aviso.titulo,
                'mensagem': aviso.mensagem,
                'tipo': aviso.tipo,
                'autor': user['nome']
            })
            return JSONResponse(content={'message': 'Aviso criado com sucesso'}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{id}")
async def delete_avisos(id: str, user: dict = Depends(verify_token)):
    """
    Deleta um aviso existente.

    Esta função remove um aviso da coleção de avisos do banco de dados, dado seu ID.
    Apenas usuários com permissões de 'GESTAO' ou 'PROFESSOR' podem deletar avisos.

    Parâmetros:
    - id: O ID do aviso a ser deletado, passado na URL.
    - user: Um dicionário que representa o usuário autenticado, obtido através da verificação do token.

    Retorna:
    - JSONResponse: Uma resposta JSON com uma mensagem de sucesso ou erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        
        if permission == 'GESTAO' or permission == 'PROFESSOR':
            await avisos_collection.delete_one({'_id': ObjectId(id)})
            return JSONResponse(content={'message': 'Aviso deletado com sucesso'}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get")
async def get_avisos(user: dict = Depends(verify_token)):
    """
    Obtém a lista de avisos.

    Esta função retorna todos os avisos armazenados no banco de dados. Dependendo do tipo de
    permissão do usuário, pode retornar todos os avisos ou apenas os avisos gerais e os
    avisos específicos da sala do usuário.

    Parâmetros:
    - user: Um dicionário que representa o usuário autenticado, obtido através da verificação do token.

    Retorna:
    - JSONResponse: Uma resposta JSON contendo a lista de avisos.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO' or permission == 'PROFESSOR':
            lista_avisos = []
            async for aviso in avisos_collection.find({}):
                aviso['_id'] = str(aviso['_id'])
                lista_avisos.append(aviso)
            return JSONResponse(content={'avisos': lista_avisos}, status_code=200)

        sala = user.get('sala')
        if not sala:
            raise HTTPException(status_code=401, detail='Usuário não possui sala')
        avisos_geral = []
        avisos_sala = []
        async for aviso in avisos_collection.find({}):
            aviso['_id'] = str(aviso['_id'])
            if aviso['tipo'] == 'Geral':
                avisos_geral.append(aviso)
            elif aviso['tipo'] == sala:
                avisos_sala.append(aviso)
        return JSONResponse(content={'avisosGeral': avisos_geral, 'avisosSala': avisos_sala, 'sala': sala}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
