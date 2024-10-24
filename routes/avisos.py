from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from models.avisos import Aviso
from database import avisos_collection, user_collection
from utils.token import verify_token

router = APIRouter()

@router.post("/create")
async def post_avisos(aviso: Aviso, user: dict = Depends(verify_token)):
    try:
        email = user['email']
        user1 = await user_collection.find_one({'email': email})
        permission = user1['permissao']

        if permission == 'GESTAO':
            await avisos_collection.insert_one({
                'titulo': aviso.titulo,
                'mensagem': aviso.mensagem,
                'tipo': aviso.tipo,
                'autor': email
            })
            return JSONResponse(content={'message': 'Aviso criado com sucesso'}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get")
async def get_avisos(user: dict = Depends(verify_token)):
    try:
        lista_avisos = []
        async for aviso in avisos_collection.find({}):
            aviso['_id'] = str(aviso['_id'])
            lista_avisos.append(aviso)

        return JSONResponse(content={'avisos': lista_avisos}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/get/{tipo}")
async def get_avisos(tipo: str = "", user: dict = Depends(verify_token)):
    try:
        lista_avisos = []
        
        if tipo:
            async for aviso in avisos_collection.find({'tipo': tipo}):
                aviso['_id'] = str(aviso['_id'])
                lista_avisos.append(aviso)
        else:
            async for aviso in avisos_collection.find({}):
                aviso['_id'] = str(aviso['_id'])
                lista_avisos.append(aviso)

        return JSONResponse(content={'avisos': lista_avisos}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

