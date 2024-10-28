from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from schemas.avisos import AvisoCreate
from database import avisos_collection, user_collection
from utils.token import verify_token
from bson import ObjectId

router = APIRouter()

@router.post("/create")
async def post_avisos(aviso: AvisoCreate, user: dict = Depends(verify_token)):
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
