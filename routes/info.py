from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from utils.token import verify_token
from database import user_collection
from bson import ObjectId

router = APIRouter()

@router.get("/getNumeroAlunos")
async def get_numero_alunos(user: dict = Depends(verify_token)):
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO':
            lista_alunos = await user_collection.find({'permissao': 'ALUNO'}).to_list(length=1000)
            numero_alunos = len(lista_alunos)
            return JSONResponse(content=numero_alunos, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/getNumeroProfessores")
async def get_numero_professores(user: dict = Depends(verify_token)):
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO':
            lista_professores = await user_collection.find({'permissao': 'PROFESSOR'}).to_list(length=1000)
            numero_professores = len(lista_professores)
            return JSONResponse(content=numero_professores, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/getNumeroGestao")
async def get_numero_gestao(user: dict = Depends(verify_token)):
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO':
            lista_gestao = await user_collection.find({'permissao': 'GESTAO'}).to_list(length=1000)
            numero_gestao = len(lista_gestao)
            return JSONResponse(content=numero_gestao, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    