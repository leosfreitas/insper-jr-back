from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from database import user_collection
from utils.token import verify_token
from models.alunos import Aluno  
from schemas.alunos import AlunoCreate
from utils.hash import hash_password

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_aluno(aluno: AlunoCreate, user: dict = Depends(verify_token)):
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})
        
        if user_data is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        permission = user_data['permissao']
        
        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")

        existing_aluno = await user_collection.find_one({'cpf': aluno.cpf})
        if existing_aluno:
            raise HTTPException(status_code=400, detail="CPF já está registrado")

        aluno_dict = aluno.dict()  
        aluno_dict["nome"] = aluno_dict["nome"].capitalize()
        aluno_dict["permissao"] = "ALUNO"
        aluno_dict["password"] = hash_password(aluno_dict["password"])
        aluno_dict["notas"] = {}
        if await user_collection.find_one({"email": aluno_dict["email"]}):
            raise HTTPException(status_code=400, detail="Email já registrado")

        result = await user_collection.insert_one(aluno_dict)
        
        return JSONResponse(content={"message": "Aluno criado com sucesso", "id": str(result.inserted_id)}, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@router.get("/get")
async def get_alunos(user: dict = Depends(verify_token)):
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})

        if user_data is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        permission = user_data['permissao']
        
        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")

        lista_alunos = []
        async for aluno in user_collection.find({'permissao': 'ALUNO'}):
            aluno['_id'] = str(aluno['_id'])
            lista_alunos.append(aluno)

        return JSONResponse(content={'alunos': lista_alunos}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/{cpf}", response_model=Aluno)  
async def get_aluno(cpf: str, user: dict = Depends(verify_token)):
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})
        permission = user_data['permissao']
        
        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")
        
        aluno = await user_collection.find_one({'cpf': cpf})
        
        if aluno is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        
        return Aluno(**aluno)  

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
